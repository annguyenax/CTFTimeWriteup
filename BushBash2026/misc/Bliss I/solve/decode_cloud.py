#!/usr/bin/env python3
"""Recover the 24x24 Data Matrix hidden as a cloud in bliss.png."""

from __future__ import annotations

import cv2
import numpy as np
import reedsolo
import zxingcpp
from scipy.optimize import minimize
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from solve_bliss import placement


IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\difference_crop.jpg"
SIZE = 32
REGION = 16


def main() -> None:
    image = cv2.imread(IMAGE)
    sat = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(float)

    # 32x32 ECC200 has four 16x16 regions, each with a finder border.
    border_known = np.zeros((SIZE, SIZE), dtype=bool)
    border_black = np.zeros((SIZE, SIZE), dtype=bool)
    for top in (0, REGION):
        for left in (0, REGION):
            border_known[top, left:left+REGION] = True
            border_known[top+REGION-1, left:left+REGION] = True
            border_known[top:top+REGION, left] = True
            border_known[top:top+REGION, left+REGION-1] = True
            border_black[top, left:left+REGION] = np.arange(REGION) % 2 == 0
            border_black[top+REGION-1, left:left+REGION] = True
            border_black[top:top+REGION, left] = True
            border_black[top:top+REGION, left+REGION-1] = np.arange(REGION) % 2 == 1

    rr, cc = np.nonzero(border_known)
    target = np.where(border_black[rr, cc], 1.0, -1.0)
    target -= target.mean()
    target /= np.linalg.norm(target)

    rng = np.random.default_rng(20260801)
    total = 600_000
    params = np.column_stack(
        (
            rng.uniform(145, 190, total),
            rng.uniform(130, 165, total),
            rng.uniform(9, 14, total),
            rng.uniform(-0.5, 1.0, total),
            rng.uniform(-3.0, 1.5, total),
            rng.uniform(5, 8, total),
            rng.uniform(-0.012, 0.012, total),
            rng.uniform(-0.006, 0.006, total),
        )
    )
    best: list[tuple[float, np.ndarray]] = []
    for start in range(0, total, 2000):
        p = params[start : start + 2000]
        x = np.rint(
            p[:, 0, None]
            + cc * p[:, 2, None]
            + rr * p[:, 4, None]
            + cc * rr * p[:, 6, None]
        ).astype(int)
        y = np.rint(
            p[:, 1, None]
            + cc * p[:, 3, None]
            + rr * p[:, 5, None]
            + cc * rr * p[:, 7, None]
        ).astype(int)
        values = sat[y, x]
        values -= values.mean(axis=1, keepdims=True)
        values /= np.sqrt((values * values).sum(axis=1, keepdims=True) + 1e-9)
        scores = values @ target
        indexes = np.argpartition(scores, -20)[-20:]
        best.extend((float(scores[i]), p[i].copy()) for i in indexes)
    best.sort(key=lambda item: item[0], reverse=True)

    def border_objective(p: np.ndarray) -> float:
        x = p[0] + cc * p[2] + rr * p[4] + cc * rr * p[6]
        y = p[1] + cc * p[3] + rr * p[5] + cc * rr * p[7]
        if x.min() < 0 or y.min() < 0 or x.max() >= sat.shape[1] or y.max() >= sat.shape[0]:
            return 1.0
        values = cv2.remap(
            sat.astype(np.float32),
            x.astype(np.float32)[None, :],
            y.astype(np.float32)[None, :],
            cv2.INTER_LINEAR,
        ).ravel()
        values -= values.mean()
        values /= np.linalg.norm(values) + 1e-9
        return -float(values @ target)

    refined_best = []
    for _, seed in best[:20]:
        result = minimize(
            border_objective,
            seed,
            method="Nelder-Mead",
            options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-8},
        )
        refined_best.append((-float(result.fun), result.x))
    best = sorted(best + refined_best, key=lambda item: item[0], reverse=True)
    print(f"best_border_correlation={best[0][0]:.6f}")

    grid_r, grid_c = np.indices((SIZE, SIZE))
    data_indexes = np.array([*range(1, 15), *range(17, 31)])
    place, count = placement(28, 28)
    codec = reedsolo.RSCodec(36, fcr=1, prim=0x12D)
    for rank, (score, p) in enumerate(best[:100]):
        samples = []
        for dr in (-0.25, 0.0, 0.25):
            for dc in (-0.25, 0.0, 0.25):
                r = grid_r + dr
                c = grid_c + dc
                x = p[0] + c * p[2] + r * p[4] + c * r * p[6]
                y = p[1] + c * p[3] + r * p[5] + c * r * p[7]
                samples.append(
                    cv2.remap(
                        sat.astype(np.float32),
                        x.astype(np.float32),
                        y.astype(np.float32),
                        cv2.INTER_LINEAR,
                    )
                )
        raw = np.mean(samples, axis=0)
        otsu, _ = cv2.threshold(
            raw.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        for threshold in np.linspace(max(5, otsu - 45), min(230, otsu + 45), 91):
            black = raw > threshold
            black[border_known] = border_black[border_known]
            codewords = np.zeros(count, dtype=np.uint8)
            reliability = np.full(count, 1e9)
            for row in range(28):
                for col in range(28):
                    pos, bit = place[row, col]
                    if pos >= 0:
                        symbol_row = data_indexes[row]
                        symbol_col = data_indexes[col]
                        if black[symbol_row, symbol_col]:
                            codewords[pos] |= 1 << (8 - bit)
                        reliability[pos] = min(
                            reliability[pos], abs(raw[symbol_row, symbol_col] - threshold)
                        )
            corrected = None
            weak = np.argsort(reliability)
            for erased in range(0, 19):
                try:
                    _, corrected_bytes, _ = codec.decode(
                        bytes(codewords), erase_pos=weak[:erased].tolist()
                    )
                    corrected = np.frombuffer(bytes(corrected_bytes), dtype=np.uint8)
                    break
                except reedsolo.ReedSolomonError:
                    continue
            if corrected is None:
                continue
            for row in range(28):
                for col in range(28):
                    pos, bit = place[row, col]
                    if pos >= 0:
                        black[data_indexes[row], data_indexes[col]] = bool(
                            (corrected[pos] >> (8 - bit)) & 1
                        )
            modules = np.where(black, 0, 255).astype(np.uint8)
            rendered = cv2.copyMakeBorder(
                cv2.resize(modules, None, fx=12, fy=12, interpolation=cv2.INTER_NEAREST),
                24,
                24,
                24,
                24,
                cv2.BORDER_CONSTANT,
                value=255,
            )
            result = zxingcpp.read_barcode(rendered)
            if result and result.text and (
                "http" in result.text.lower() or "bushbash" in result.text.lower()
            ):
                print(f"rank={rank} score={score:.6f} threshold={threshold:.1f}")
                print(result.text)
                cv2.imwrite(
                    r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\solve\recovered_datamatrix.png",
                    rendered,
                )
                return
    print("No decode")


if __name__ == "__main__":
    main()
