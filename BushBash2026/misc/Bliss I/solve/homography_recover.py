#!/usr/bin/env python3
"""
Bliss I — recover soft Data Matrix by fitting L-finder + timing via homography,
then RS erase-decode (reuses rs_erase_decode helpers).

Strategy:
  1. Build score map (white fog modules = high).
  2. Multi-start 4-corner boxes over the cloud; score each by border match
     (solid left+bottom, alternating top+right).
  3. Locally refine corners (coordinate descent / small grid).
  4. Sample SIZE×SIZE soft values at module centers under perspective.
  5. Soft threshold + force border + RS erase-decode + zxing.

Usage:
  python solve/homography_recover.py
  python solve/homography_recover.py --size 18 --quick
  python solve/homography_recover.py --size 18 --refine-iters 40
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOLVE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SOLVE))

from rs_erase_decode import (  # noqa: E402
    CONFIGS,
    EVIDENCE,
    IMAGE,
    bits_and_conf,
    codewords_to_bits,
    dm_ascii_unwrap,
    matrix_to_codewords,
    placement,
    render_dm,
    score_map,
    try_rs_erase,
    zxing_text,
)

# cloud ROI (approx, full-res bliss.png)
ROI = dict(x0=920, x1=1450, y0=680, y1=1020)


def expected_border(size: int) -> np.ndarray:
    """1 = expect black (high score), 0 = expect white (low), -1 = data ignore."""
    exp = -np.ones((size, size), dtype=np.int8)
    exp[:, 0] = 1
    exp[-1, :] = 1
    for i in range(size):
        exp[0, i] = 1 if (i % 2 == 0) else 0
        exp[i, -1] = 1 if (i % 2 == 1) else 0
    return exp


def corners_to_centers(
    corners: np.ndarray, size: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    corners: 4x2 float32 TL, TR, BR, BL in image coords.
    Returns xx, yy arrays shape (size, size) of module centers.
    """
    src = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(src, corners.astype(np.float32))
    # module centers in unit square
    gs = (np.arange(size) + 0.5) / size
    uu, vv = np.meshgrid(gs, gs)  # u=col, v=row
    ones = np.ones_like(uu)
    pts = np.stack([uu.ravel(), vv.ravel(), ones.ravel()], axis=0)  # 3xN
    mapped = H @ pts
    mapped /= mapped[2:3, :]
    xx = mapped[0].reshape(size, size)
    yy = mapped[1].reshape(size, size)
    return xx, yy


def sample_at(
    full: np.ndarray, xx: np.ndarray, yy: np.ndarray, rad: int = 1
) -> np.ndarray | None:
    h, w = full.shape
    size = xx.shape[0]
    soft = np.zeros((size, size), dtype=np.float64)
    for r in range(size):
        for c in range(size):
            x, y = float(xx[r, c]), float(yy[r, c])
            xi, yi = int(round(x)), int(round(y))
            if xi < rad or yi < rad or xi + rad >= w or yi + rad >= h:
                return None
            soft[r, c] = full[yi - rad : yi + rad + 1, xi - rad : xi + rad + 1].mean()
    return soft


def border_score(soft: np.ndarray, exp: np.ndarray) -> float:
    """Higher = better match of soft scores to expected border polarity."""
    # z-score soft
    mu, sd = float(soft.mean()), float(soft.std()) + 1e-6
    z = (soft - mu) / sd
    mask = exp >= 0
    # expected black → high z; expected white → low z
    target = np.where(exp == 1, 1.0, -1.0)
    return float((z[mask] * target[mask]).mean())


def timing_score(soft: np.ndarray, size: int) -> float:
    """Extra: top/right should alternate; left/bottom solid."""
    mu, sd = float(soft.mean()), float(soft.std()) + 1e-6
    z = (soft - mu) / sd
    # solid left/bottom: high mean
    solid = 0.5 * (z[:, 0].mean() + z[-1, :].mean())
    # alternation: correlation with ±1 pattern
    top_pat = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(size)])
    right_pat = np.array([1.0 if i % 2 == 1 else -1.0 for i in range(size)])
    top = float(np.corrcoef(z[0, :], top_pat)[0, 1]) if z[0].std() > 1e-6 else 0.0
    right = (
        float(np.corrcoef(z[:, -1], right_pat)[0, 1]) if z[:, -1].std() > 1e-6 else 0.0
    )
    if np.isnan(top):
        top = 0.0
    if np.isnan(right):
        right = 0.0
    return solid + top + right


def total_score(full: np.ndarray, corners: np.ndarray, size: int, exp: np.ndarray) -> float:
    xx, yy = corners_to_centers(corners, size)
    soft = sample_at(full, xx, yy)
    if soft is None:
        return -1e9
    return border_score(soft, exp) + 0.35 * timing_score(soft, size)


def init_corners_grid(
    size: int, quick: bool
) -> list[np.ndarray]:
    """Generate candidate TL-TR-BR-BL boxes over cloud ROI."""
    # Rough span of DM on sky ~ 420–480 px wide, 240–300 tall (anisotropic soft)
    if quick:
        widths = np.linspace(380, 500, 6)
        heights = np.linspace(230, 320, 6)
        x0s = np.linspace(ROI["x0"] + 20, ROI["x0"] + 120, 6)
        y0s = np.linspace(ROI["y0"] + 20, ROI["y0"] + 90, 6)
        shears = [0.0, 8.0, -8.0]
    else:
        widths = np.linspace(360, 520, 10)
        heights = np.linspace(220, 340, 10)
        x0s = np.linspace(ROI["x0"] + 10, ROI["x0"] + 140, 10)
        y0s = np.linspace(ROI["y0"] + 10, ROI["y0"] + 100, 10)
        shears = [0.0, 6.0, -6.0, 12.0, -12.0]

    boxes: list[np.ndarray] = []
    for w in widths:
        for h in heights:
            for x0 in x0s:
                for y0 in y0s:
                    for sh in shears:
                        # parallelogram-ish: top edge may shear
                        TL = (x0, y0)
                        TR = (x0 + w, y0 + sh * 0.3)
                        BR = (x0 + w + sh * 0.2, y0 + h)
                        BL = (x0 - sh * 0.15, y0 + h)
                        boxes.append(
                            np.array([TL, TR, BR, BL], dtype=np.float64)
                        )
    return boxes


def refine_corners(
    full: np.ndarray,
    corners: np.ndarray,
    size: int,
    exp: np.ndarray,
    iters: int = 25,
    step0: float = 6.0,
) -> tuple[np.ndarray, float]:
    """Coordinate-descent jitter of each corner."""
    best = corners.copy()
    best_s = total_score(full, best, size, exp)
    step = step0
    rng = np.random.default_rng(42)
    for it in range(iters):
        improved = False
        order = rng.permutation(4)
        for ci in order:
            for dx, dy in (
                (step, 0),
                (-step, 0),
                (0, step),
                (0, -step),
                (step, step),
                (step, -step),
                (-step, step),
                (-step, -step),
                (step * 0.5, 0),
                (-step * 0.5, 0),
                (0, step * 0.5),
                (0, -step * 0.5),
            ):
                trial = best.copy()
                trial[ci, 0] += dx
                trial[ci, 1] += dy
                # keep roughly convex / ordered
                if trial[1, 0] <= trial[0, 0] + 50:
                    continue
                if trial[2, 1] <= trial[0, 1] + 50:
                    continue
                s = total_score(full, trial, size, exp)
                if s > best_s:
                    best_s = s
                    best = trial
                    improved = True
        if not improved:
            step *= 0.6
            if step < 0.4:
                break
    return best, best_s


def detect_l_seed(full: np.ndarray) -> np.ndarray | None:
    """
    Rough seed: in ROI, find vertical high-score ridge (left L) and
    horizontal high-score ridge (bottom L), estimate bbox.
    """
    x0, x1, y0, y1 = ROI["x0"], ROI["x1"], ROI["y0"], ROI["y1"]
    crop = full[y0:y1, x0:x1].astype(np.float64)
    # normalize
    crop = (crop - crop.mean()) / (crop.std() + 1e-6)
    # vertical energy: max over columns of mean of top-k rows in column? 
    # left finder is solid vertical: mean along y high in a column
    col_mean = crop.mean(axis=0)
    # smooth
    k = 15
    ker = np.ones(k) / k
    col_s = np.convolve(col_mean, ker, mode="same")
    row_mean = crop.mean(axis=1)
    row_s = np.convolve(row_mean, ker, mode="same")

    # left edge candidate: first strong peak from left in upper-mid
    left_local = col_s[: int(0.45 * len(col_s))]
    if left_local.size == 0:
        return None
    lx = int(np.argmax(left_local))
    # bottom edge: strong peak from bottom
    bottom_local = row_s[int(0.4 * len(row_s)) :]
    by = int(0.4 * len(row_s)) + int(np.argmax(bottom_local))

    # right / top: assume aspect ~1.7 (wide cloud)
    width = 440
    height = 270
    # refine width using another high column further right for timing? skip
    TL = (x0 + lx - 5, y0 + by - height)
    TR = (x0 + lx - 5 + width, y0 + by - height + 10)
    BR = (x0 + lx - 5 + width + 15, y0 + by + 5)
    BL = (x0 + lx - 5 - 10, y0 + by + 5)
    return np.array([TL, TR, BR, BL], dtype=np.float64)


def decode_soft(soft: np.ndarray, size: int, nsym: int, params: str):
    place, n_cw = placement(size - 2, size - 2)
    hits_all = []
    for thr_pct in (35, 40, 45, 50, 55, 60, 65):
        thr = float(np.percentile(soft, thr_pct))
        bits, conf = bits_and_conf(soft, thr)
        interior = bits[1:-1, 1:-1]
        m = float(interior.mean())
        if m < 0.1 or m > 0.9:
            continue
        cw, rel = matrix_to_codewords(bits, conf, place, n_cw)
        for h in try_rs_erase(cw, rel, size, nsym, f"{params} p{thr_pct}"):
            hits_all.append(h)
    return hits_all


def dump_overlay(
    bgr: np.ndarray, corners: np.ndarray, xx: np.ndarray, yy: np.ndarray, path: Path
) -> None:
    vis = bgr.copy()
    pts = corners.astype(np.int32).reshape(-1, 1, 2)
    cv2.polylines(vis, [pts], True, (0, 255, 255), 2)
    for r in range(0, xx.shape[0], max(1, xx.shape[0] // 6)):
        for c in range(0, xx.shape[1], max(1, xx.shape[1] // 6)):
            cv2.circle(vis, (int(xx[r, c]), int(yy[r, c])), 2, (0, 0, 255), -1)
    # crop ROI
    x0, x1, y0, y1 = ROI["x0"], ROI["x1"], ROI["y0"], ROI["y1"]
    crop = vis[y0:y1, x0:x1]
    cv2.imwrite(str(path), crop)


def de_refine(
    full: np.ndarray,
    corners: np.ndarray,
    size: int,
    exp: np.ndarray,
    span: float = 40.0,
    maxiter: int = 30,
) -> tuple[np.ndarray, float]:
    """Differential evolution polish of 4 corners (±span px)."""
    from scipy.optimize import differential_evolution

    seed = corners.reshape(-1)

    def neg(v: np.ndarray) -> float:
        c = v.reshape(4, 2)
        if c[1, 0] < c[0, 0] + 80 or c[2, 1] < c[0, 1] + 50:
            return 1e3
        return -total_score(full, c, size, exp)

    bounds = [(float(x - span), float(x + span)) for x in seed]
    res = differential_evolution(
        neg,
        bounds,
        maxiter=maxiter,
        popsize=12,
        seed=1,
        polish=True,
        workers=1,
        updating="immediate",
    )
    return res.x.reshape(4, 2), float(-res.fun)


def main() -> None:
    ap = argparse.ArgumentParser(description="Homography L-finder DM recover")
    ap.add_argument("--size", type=int, default=18, choices=[18, 20])
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--refine-iters", type=int, default=30)
    ap.add_argument("--top-k", type=int, default=40, help="refine top-K coarse boxes")
    ap.add_argument(
        "--de",
        action="store_true",
        help="extra differential-evolution polish on best corner box",
    )
    args = ap.parse_args()

    size = args.size
    nsym = dict(CONFIGS)[size]
    exp = expected_border(size)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    bgr = cv2.imread(str(IMAGE))
    if bgr is None:
        raise SystemExit(f"cannot read {IMAGE}")
    full = score_map(bgr)
    # save score crop
    sc = full[ROI["y0"] : ROI["y1"], ROI["x0"] : ROI["x1"]]
    sc_u8 = cv2.normalize(sc, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite(str(EVIDENCE / "score_roi.png"), sc_u8)

    print(f"=== coarse box search size={size} nsym={nsym} ===", flush=True)
    boxes = init_corners_grid(size, quick=args.quick)
    seed = detect_l_seed(full)
    if seed is not None:
        boxes.insert(0, seed)
        print(f"L-seed corners:\n{seed}", flush=True)

    scored: list[tuple[float, np.ndarray]] = []
    for i, box in enumerate(boxes):
        s = total_score(full, box, size, exp)
        if s > -1e8:
            scored.append((s, box))
        if (i + 1) % 2000 == 0:
            print(f"  scored {i+1}/{len(boxes)} bestsofar={max(t[0] for t in scored):.3f}", flush=True)

    scored.sort(key=lambda t: t[0], reverse=True)
    print(f"coarse candidates: {len(scored)} best={scored[0][0]:.4f}", flush=True)

    print(f"=== refine top {args.top_k} ===", flush=True)
    refined: list[tuple[float, np.ndarray]] = []
    for s0, box in scored[: args.top_k]:
        b2, s2 = refine_corners(
            full, box, size, exp, iters=args.refine_iters, step0=8.0
        )
        refined.append((s2, b2))
        print(f"  {s0:.3f} -> {s2:.3f}", flush=True)
    refined.sort(key=lambda t: t[0], reverse=True)

    if args.de and refined:
        print("=== DE polish on best box ===", flush=True)
        c_de, s_de = de_refine(full, refined[0][1], size, exp, span=40, maxiter=35)
        print(f"  DE score {refined[0][0]:.3f} -> {s_de:.3f}", flush=True)
        refined.insert(0, (s_de, c_de))
        # sharpen score map for sampling later candidates
        blur = cv2.GaussianBlur(full, (0, 0), 2.0)
        full = cv2.addWeighted(full, 1.8, blur, -0.8, 0)

    # also multi-start refine from top coarse with smaller steps
    best_hits = []
    seen_data = set()
    report_lines = []

    for rank, (sc, corners) in enumerate(refined[:15]):
        xx, yy = corners_to_centers(corners, size)
        soft = sample_at(full, xx, yy, rad=1)
        if soft is None:
            continue
        # also try rad=2
        soft2 = sample_at(full, xx, yy, rad=2)
        for tag, soft_u in (("r1", soft), ("r2", soft2)):
            if soft_u is None:
                continue
            params = f"homo rank={rank} score={sc:.3f} {tag} corners={corners.round(1).tolist()}"
            hits = decode_soft(soft_u, size, nsym, params)
            for h in hits:
                max_erase = max(2, nsym // 2)
                flagish = "bushbash" in (h.unwrap or "").lower() or "bushbash" in (
                    h.zxing or ""
                ).lower()
                flagish = flagish or "http" in (h.unwrap or "").lower()
                trusted = flagish or (
                    h.zxing and h.erased <= max_erase and h.agree >= 0.99
                )
                if not trusted:
                    continue
                key = (h.data, h.zxing)
                if key in seen_data:
                    continue
                seen_data.add(key)
                best_hits.append(h)
                line = (
                    f"TRUSTED size={h.size} erased={h.erased} agree={h.agree:.3f} "
                    f"zxing={h.zxing!r} unwrap={h.unwrap!r} | {h.params}"
                )
                print(line, flush=True)
                report_lines.append(line)

        # always dump best rank's matrix for inspection
        if rank == 0:
            thr = float(np.percentile(soft, 50))
            bits, _ = bits_and_conf(soft, thr)
            ascii_m = "\n".join(
                "".join("#" if bits[r, c] else "." for c in range(size))
                for r in range(size)
            )
            (EVIDENCE / f"homo_best_matrix_{size}.txt").write_text(ascii_m + "\n")
            cv2.imwrite(
                str(EVIDENCE / f"homo_best_render_{size}.png"),
                render_dm(bits),
            )
            dump_overlay(
                bgr, corners, xx, yy, EVIDENCE / f"homo_overlay_{size}.png"
            )
            np.save(EVIDENCE / f"homo_corners_{size}.npy", corners)
            np.save(EVIDENCE / f"homo_soft_{size}.npy", soft)
            # try zxing direct on forced-border bits
            z = zxing_text(bits)
            print(f"best rank0 zxing(raw thr50)={z!r} border_score={sc:.3f}", flush=True)
            report_lines.append(f"rank0 raw zxing={z!r} score={sc:.3f}")
            # RS path dump all low-erase even without zxing for debug
            place, n_cw = placement(size - 2, size - 2)
            thr = float(np.percentile(soft, 50))
            bits, conf = bits_and_conf(soft, thr)
            cw, rel = matrix_to_codewords(bits, conf, place, n_cw)
            (EVIDENCE / f"homo_cw_{size}.hex").write_text(bytes(cw).hex() + "\n")
            for h in try_rs_erase(cw, rel, size, nsym, "rank0"):
                if h.erased <= nsym // 2:
                    report_lines.append(
                        f"rank0 RS erased={h.erased} zxing={h.zxing!r} "
                        f"unwrap={h.unwrap!r} data={h.data.hex()}"
                    )
                    print(
                        f"  RS erased={h.erased} zxing={h.zxing!r} unwrap={h.unwrap!r}",
                        flush=True,
                    )

    out = EVIDENCE / "homo_results.txt"
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out}", flush=True)
    if best_hits:
        print("=== FLAGISH / TRUSTED ===", flush=True)
        for h in best_hits:
            print(h.zxing or h.unwrap, flush=True)
            place, _ = placement(h.size - 2, h.size - 2)
            bits = codewords_to_bits(
                np.frombuffer(h.full, dtype=np.uint8).copy(), place, h.size
            )
            (EVIDENCE / "homo_corrected_matrix.txt").write_text(
                "\n".join(
                    "".join("#" if bits[r, c] else "." for c in range(h.size))
                    for r in range(h.size)
                )
                + "\n"
            )
            cv2.imwrite(str(EVIDENCE / "homo_corrected_dm.png"), render_dm(bits))
    else:
        print(
            "No trusted flag yet. Check evidence/homo_overlay_*.png and "
            "homo_best_matrix_*.txt — retune ROI or --refine-iters.",
            flush=True,
        )


if __name__ == "__main__":
    main()
