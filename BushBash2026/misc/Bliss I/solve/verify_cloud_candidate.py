#!/usr/bin/env python3
"""Correlate a candidate Data Matrix payload against the cloud modules."""

from __future__ import annotations

import cv2
import numpy as np
import zxingcpp
from scipy.optimize import minimize


IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"
CANDIDATE = "bushbash{atmospherically-questionable-runes}"


def variants(matrix: np.ndarray) -> list[tuple[str, np.ndarray]]:
    result = []
    for k in range(4):
        rotated = np.rot90(matrix, k)
        result.append((f"rot{k * 90}", rotated))
        result.append((f"rot{k * 90}_mirror", np.fliplr(rotated)))
    return result


def main() -> None:
    image = cv2.imread(IMAGE)
    saturation = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1].astype(float)

    barcode = zxingcpp.create_barcode(CANDIDATE, zxingcpp.BarcodeFormat.DataMatrix)
    rendered = np.asarray(
        zxingcpp.write_barcode_to_image(barcode, scale=1, add_quiet_zones=False)
    )
    modules = rendered < 128
    size = modules.shape[0]
    patterns = [(name, np.where(m, 1.0, -1.0).ravel()) for name, m in variants(modules)]

    rng = np.random.default_rng(20260801)
    total = 180_000
    params = np.column_stack(
        (
            rng.uniform(940, 1020, total),
            rng.uniform(700, 790, total),
            rng.uniform(16, 23, total),
            rng.uniform(-0.8, 1.8, total),
            rng.uniform(-2.5, 1.0, total),
            rng.uniform(8, 14, total),
            rng.uniform(-0.04, 0.04, total),
            rng.uniform(-0.04, 0.04, total),
        )
    )
    rr, cc = np.indices((size, size))
    rr = rr.ravel()
    cc = cc.ravel()
    best: list[tuple[float, str, int, np.ndarray]] = []

    for start in range(0, total, 1000):
        p = params[start : start + 1000]
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
        sampled = saturation[y, x]
        sampled -= sampled.mean(axis=1, keepdims=True)
        sampled /= np.sqrt((sampled * sampled).sum(axis=1, keepdims=True) + 1e-9)
        for name, pattern in patterns:
            score = sampled @ pattern / np.linalg.norm(pattern)
            for polarity in (1, -1):
                signed = polarity * score
                indexes = np.argpartition(signed, -2)[-2:]
                best.extend(
                    (float(signed[i]), name, polarity, p[i].copy()) for i in indexes
                )

    best.sort(key=lambda item: item[0], reverse=True)
    score, orientation, polarity, geometry = best[0]

    selected = dict(patterns)[orientation] * polarity

    def objective(p: np.ndarray) -> float:
        x = np.rint(p[0] + cc * p[2] + rr * p[4] + cc * rr * p[6]).astype(int)
        y = np.rint(p[1] + cc * p[3] + rr * p[5] + cc * rr * p[7]).astype(int)
        if x.min() < 0 or y.min() < 0 or x.max() >= saturation.shape[1] or y.max() >= saturation.shape[0]:
            return 1.0
        values = saturation[y, x]
        values -= values.mean()
        corr = values @ selected / (
            np.linalg.norm(values) * np.linalg.norm(selected) + 1e-9
        )
        return -float(corr)

    refined = minimize(
        objective,
        geometry,
        method="Nelder-Mead",
        options={"maxiter": 25_000, "xatol": 1e-4, "fatol": 1e-7},
    )
    if -refined.fun > score:
        score = -float(refined.fun)
        geometry = refined.x
    print(f"candidate={CANDIDATE}")
    print(f"matrix_size={size}x{size}")
    print(f"correlation={score:.6f}")
    print(f"orientation={orientation} polarity={polarity}")
    print("geometry=" + np.array2string(geometry, precision=4))


if __name__ == "__main__":
    main()
