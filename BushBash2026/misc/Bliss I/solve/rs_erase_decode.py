#!/usr/bin/env python3
"""
Bliss I — soft Data Matrix recovery via Reed–Solomon erase-decode.

ECC200 square sizes used:
  18×18 full → interior 16×16 → 32 codewords (18 data + 14 ECC)
  20×20 full → interior 18×18 → 40 codewords (22 data + 18 ECC)

Timing on recovered.png confirms **18×18** (perfect alternation). Script still
tries 20×20 as fallback.

Pipeline:
  1. Score map (white modules vs blue sky).
  2. Sample SIZE×SIZE module centers.
  3. Soft threshold → bits; force L-finder + timing.
  4. Map interior → codewords; reliability = min |soft−thr| over bits of each CW.
  5. Erase least-reliable CWs; RS-decode; re-encode check on kept CWs.
  6. Re-render corrected matrix → zxing; naive ASCII unwrap.

Usage:
  python solve/rs_erase_decode.py --from-recovered
  python solve/rs_erase_decode.py --quick
  python solve/rs_erase_decode.py
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import reedsolo
import zxingcpp
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from solve_bliss import placement  # noqa: E402

IMAGE = ROOT / "bliss.png"
RECOVERED = ROOT / "recovered.png"
EVIDENCE = Path(__file__).resolve().parent / "evidence"

# ECC200: (symbol_size, nsym_ecc)
CONFIGS = (
    (18, 14),  # primary — matches recovered.png timing
    (20, 18),
)


@dataclass
class Hit:
    size: int
    nsym: int
    erased: int
    data: bytes
    full: bytes
    unwrap: str
    zxing: str | None
    agree: float
    params: str


def score_map(bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    B, G, R = cv2.split(bgr.astype(np.float32))
    V, S = hsv[:, :, 2], hsv[:, :, 1]
    return (V - 0.6 * S) + 0.35 * (R - B)


def sample_soft(
    full: np.ndarray, gx0: float, gy0: float, stepx: float, stepy: float, size: int
) -> np.ndarray | None:
    M = np.zeros((size, size), dtype=np.float64)
    h, w = full.shape
    for r in range(size):
        for c in range(size):
            cy = gy0 + (r + 0.5) * stepy
            cx = gx0 + (c + 0.5) * stepx
            x0i, y0i = int(round(cx)), int(round(cy))
            if x0i < 1 or y0i < 1 or x0i + 2 >= w or y0i + 2 >= h:
                return None
            M[r, c] = full[y0i - 1 : y0i + 2, x0i - 1 : x0i + 2].mean()
    return M


def enforce_border(bits: np.ndarray) -> np.ndarray:
    bits = bits.copy()
    n = bits.shape[0]
    bits[:, 0] = 1
    bits[-1, :] = 1
    for i in range(n):
        bits[0, i] = 1 if (i % 2 == 0) else 0
        bits[i, -1] = 1 if (i % 2 == 1) else 0
    return bits


def bits_and_conf(soft: np.ndarray, thr: float) -> tuple[np.ndarray, np.ndarray]:
    bits = (soft > thr).astype(np.uint8)
    conf = np.abs(soft - thr)
    bits = enforce_border(bits)
    conf[:, 0] = conf[-1, :] = conf[0, :] = conf[:, -1] = 1e6
    return bits, conf


def matrix_to_codewords(
    bits: np.ndarray, conf: np.ndarray, place: np.ndarray, n_cw: int
) -> tuple[np.ndarray, np.ndarray]:
    data = bits.shape[0] - 2
    cw = np.zeros(n_cw, dtype=np.uint8)
    rel = np.full(n_cw, 1e9, dtype=np.float64)
    ib, ic = bits[1:-1, 1:-1], conf[1:-1, 1:-1]
    for r in range(data):
        for c in range(data):
            pos, bit = int(place[r, c, 0]), int(place[r, c, 1])
            if pos < 0:
                continue
            if ib[r, c]:
                cw[pos] |= 1 << (8 - bit)
            rel[pos] = min(rel[pos], float(ic[r, c]))
    return cw, rel


def codewords_to_bits(cw: np.ndarray, place: np.ndarray, size: int) -> np.ndarray:
    data = size - 2
    bits = np.zeros((size, size), dtype=np.uint8)
    bits = enforce_border(bits)
    for r in range(data):
        for c in range(data):
            pos, bit = int(place[r, c, 0]), int(place[r, c, 1])
            if pos < 0:
                continue
            if (int(cw[pos]) >> (8 - bit)) & 1:
                bits[r + 1, c + 1] = 1
    return bits


def render_dm(bits: np.ndarray, scale: int = 12, quiet: int = 40) -> np.ndarray:
    img = np.where(np.kron(bits, np.ones((scale, scale))), 0, 255).astype(np.uint8)
    canvas = np.full(
        (img.shape[0] + 2 * quiet, img.shape[1] + 2 * quiet), 255, np.uint8
    )
    canvas[quiet:-quiet, quiet:-quiet] = img
    return canvas


def zxing_text(bits: np.ndarray) -> str | None:
    res = zxingcpp.read_barcodes(
        render_dm(bits), formats=zxingcpp.BarcodeFormat.DataMatrix
    )
    return res[0].text if res else None


def dm_ascii_unwrap(data: bytes) -> str:
    out: list[str] = []
    for v in data:
        if v == 0:
            break
        if 1 <= v <= 128:
            out.append(chr(v - 1))
        elif v == 129:
            break
        elif 130 <= v <= 229:
            out.append(f"{v - 130:02d}")
        else:
            out.append(f"\\x{v:02x}")
    return "".join(out)


def try_rs_erase(
    cw: np.ndarray, rel: np.ndarray, size: int, nsym: int, params: str
) -> list[Hit]:
    n_cw = len(cw)
    codec = reedsolo.RSCodec(nsym, fcr=1, prim=0x12d)
    place, n_place = placement(size - 2, size - 2)
    assert n_place == n_cw, (n_place, n_cw, size)
    order = np.argsort(rel)
    hits: list[Hit] = []
    seen: set[bytes] = set()

    for erased in range(0, nsym + 1):
        epos = order[:erased].tolist()
        epos_set = set(epos)
        try:
            out = codec.decode(bytes(cw), erase_pos=epos)
        except reedsolo.ReedSolomonError:
            continue
        decoded = bytes(out[0])
        full_b = bytes(out[1])
        if len(full_b) != n_cw:
            continue
        if decoded in seen:
            continue
        # Agreement on non-erased positions with *original* cw
        match = sum(
            1 for i in range(n_cw) if i not in epos_set and full_b[i] == int(cw[i])
        )
        kept = n_cw - erased
        agree = match / kept if kept else 0.0
        # Re-encode check: corrected data must produce same full
        try:
            reenc = bytes(codec.encode(decoded))
        except Exception:
            continue
        if reenc != full_b:
            continue
        # Require solid agreement on kept symbols (true erasures ok)
        if agree < 0.999 and erased < nsym:
            # allow tiny float noise only when many erasures
            if agree < 0.85:
                continue

        seen.add(decoded)
        bits = codewords_to_bits(np.frombuffer(full_b, dtype=np.uint8).copy(), place, size)
        ztxt = zxing_text(bits)
        unwrapped = dm_ascii_unwrap(decoded)
        hits.append(
            Hit(
                size=size,
                nsym=nsym,
                erased=erased,
                data=decoded,
                full=full_b,
                unwrap=unwrapped,
                zxing=ztxt,
                agree=agree,
                params=params,
            )
        )
    return hits


def soft_from_recovered(size: int) -> tuple[np.ndarray, float] | None:
    if not RECOVERED.exists():
        return None
    img = np.array(Image.open(RECOVERED).convert("L"), dtype=np.float64)
    b = (img < 128).astype(np.uint8)
    ys, xs = np.where(b > 0)
    if len(ys) == 0:
        return None
    y0, y1, x0, x1 = int(ys.min()), int(ys.max() + 1), int(xs.min()), int(xs.max() + 1)
    gray = img[y0:y1, x0:x1]
    H, W = gray.shape
    soft = np.zeros((size, size), dtype=np.float64)
    for r in range(size):
        for c in range(size):
            cy = int((r + 0.5) * H / size)
            cx = int((c + 0.5) * W / size)
            # black module in recovered → high score (DM black)
            soft[r, c] = 255.0 - float(gray[min(cy, H - 1), min(cx, W - 1)])
    thr = float(np.median(soft))
    return soft, thr


def from_recovered() -> list[Hit]:
    all_hits: list[Hit] = []
    for size, nsym in CONFIGS:
        got = soft_from_recovered(size)
        if got is None:
            continue
        soft, thr = got
        bits, conf = bits_and_conf(soft, thr)
        place, n_cw = placement(size - 2, size - 2)
        cw, rel = matrix_to_codewords(bits, conf, place, n_cw)
        print(
            f"[recovered] size={size} nsym={nsym} n_cw={n_cw} "
            f"interior_mean={bits[1:-1,1:-1].mean():.3f}",
            flush=True,
        )
        # dump matrix
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        ascii_m = "\n".join(
            "".join("#" if bits[r, c] else "." for c in range(size)) for r in range(size)
        )
        (EVIDENCE / f"matrix_{size}_from_recovered.txt").write_text(ascii_m + "\n")
        (EVIDENCE / f"cw_{size}_from_recovered.hex").write_text(bytes(cw).hex() + "\n")
        hits = try_rs_erase(cw, rel, size, nsym, params="recovered.png")
        for h in hits:
            print(
                f"  erased={h.erased} agree={h.agree:.3f} "
                f"zxing={h.zxing!r} unwrap={h.unwrap!r} data={h.data.hex()}",
                flush=True,
            )
        all_hits.extend(hits)
    return all_hits


def search_original(quick: bool = False) -> list[Hit]:
    bgr = cv2.imread(str(IMAGE))
    if bgr is None:
        raise SystemExit(f"cannot read {IMAGE}")
    full = score_map(bgr)
    # cloud approx
    if quick:
        gx0s = np.linspace(955, 1005, 6)
        gy0s = np.linspace(708, 742, 6)
        thr_pcts = (45, 50, 55)
    else:
        gx0s = np.linspace(948, 1012, 12)
        gy0s = np.linspace(700, 752, 12)
        thr_pcts = (40, 45, 50, 55, 60)

    all_hits: list[Hit] = []
    seen: set[tuple] = set()
    trials = 0

    for size, nsym in CONFIGS:
        place, n_cw = placement(size - 2, size - 2)
        # module pitch: recovered 144px / 18 ≈ 8; on original ~450×270 for wide cloud
        if size == 18:
            stepxs = np.linspace(22.0, 26.0, 6 if quick else 10)
            stepys = np.linspace(13.0, 16.5, 6 if quick else 10)
        else:
            stepxs = np.linspace(20.0, 24.5, 5 if quick else 9)
            stepys = np.linspace(12.5, 16.0, 5 if quick else 9)

        for gx0 in gx0s:
            for gy0 in gy0s:
                for stepx in stepxs:
                    for stepy in stepys:
                        soft = sample_soft(full, gx0, gy0, stepx, stepy, size)
                        if soft is None:
                            continue
                        for thr_pct in thr_pcts:
                            trials += 1
                            thr = float(np.percentile(soft, thr_pct))
                            bits, conf = bits_and_conf(soft, thr)
                            interior = bits[1:-1, 1:-1]
                            m = float(interior.mean())
                            if m < 0.12 or m > 0.88:
                                continue
                            cw, rel = matrix_to_codewords(bits, conf, place, n_cw)
                            params = (
                                f"size={size} gx0={gx0:.1f} gy0={gy0:.1f} "
                                f"sx={stepx:.2f} sy={stepy:.2f} p{thr_pct}"
                            )
                            for h in try_rs_erase(cw, rel, size, nsym, params):
                                key = (h.size, h.data, h.zxing, h.unwrap)
                                if key in seen:
                                    continue
                                # Trust only low-erasure (RS can invent garbage if erase≈nsym)
                                # t_err ≈ nsym/2; allow up to nsym//2 erasures as "honest"
                                max_erase = max(2, nsym // 2)
                                flagish = (
                                    "bushbash" in (h.unwrap or "").lower()
                                    or "bushbash" in (h.zxing or "").lower()
                                    or "http" in (h.unwrap or "").lower()
                                    or "http" in (h.zxing or "").lower()
                                )
                                ok = False
                                if flagish:
                                    ok = True
                                elif h.zxing and h.erased <= max_erase and h.agree >= 0.99:
                                    ok = True
                                elif h.erased == 0 and h.agree >= 0.99 and h.zxing:
                                    ok = True
                                if not ok:
                                    continue
                                seen.add(key)
                                all_hits.append(h)
                                print(
                                    f"[hit] {params} erased={h.erased} "
                                    f"zxing={h.zxing!r} unwrap={h.unwrap!r}",
                                    flush=True,
                                )
    print(f"trials={trials} hits={len(all_hits)}", flush=True)
    return all_hits


def summarize(results: list[Hit]) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    out = EVIDENCE / "rs_erase_results.txt"
    lines = []
    best: list[Hit] = []
    for h in results:
        lines.append(
            f"size={h.size} erased={h.erased} agree={h.agree:.3f} "
            f"zxing={h.zxing!r} unwrap={h.unwrap!r} data={h.data.hex()} | {h.params}"
        )
        if h.zxing or "bushbash" in h.unwrap.lower():
            best.append(h)
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"\nWrote {out} ({len(lines)} lines)", flush=True)
    if best:
        print("=== BEST ===", flush=True)
        for h in best:
            print(h.zxing or h.unwrap, flush=True)
            place, _ = placement(h.size - 2, h.size - 2)
            bits = codewords_to_bits(
                np.frombuffer(h.full, dtype=np.uint8).copy(), place, h.size
            )
            (EVIDENCE / "rs_corrected_matrix.txt").write_text(
                "\n".join(
                    "".join("#" if bits[r, c] else "." for c in range(h.size))
                    for r in range(h.size)
                )
                + "\n"
            )
            cv2.imwrite(str(EVIDENCE / "rs_corrected_dm.png"), render_dm(bits))
    else:
        print(
            "No trusted decode yet (need zxing text or bushbash unwrap). "
            "Module sampling still noisy — try phone Lens on a crisp export.",
            flush=True,
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--from-recovered", action="store_true")
    ap.add_argument("--no-search", action="store_true", help="skip bliss.png search")
    args = ap.parse_args()
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    results: list[Hit] = []
    print("=== recovered.png ===", flush=True)
    results.extend(from_recovered())
    if args.from_recovered:
        summarize(results)
        return
    if not args.no_search:
        print("=== bliss.png search ===", flush=True)
        results.extend(search_original(quick=args.quick))
    summarize(results)


if __name__ == "__main__":
    main()
