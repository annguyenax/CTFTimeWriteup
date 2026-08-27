#!/usr/bin/env python3
"""Rank plausible ECC200 symbol sizes using their finder-border correlation."""

import cv2
import numpy as np


IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"


def borders(size: int) -> tuple[np.ndarray, np.ndarray]:
    known = np.zeros((size, size), bool)
    black = np.zeros((size, size), bool)
    region = 16 if size == 32 else size
    starts = range(0, size, region)
    for top in starts:
        for left in starts:
            known[top, left : left + region] = True
            known[top + region - 1, left : left + region] = True
            known[top : top + region, left] = True
            known[top : top + region, left + region - 1] = True
            black[top, left : left + region] = np.arange(region) % 2 == 0
            black[top + region - 1, left : left + region] = True
            black[top : top + region, left] = True
            black[top : top + region, left + region - 1] = np.arange(region) % 2 == 1
    return known, black


def main() -> None:
    im = cv2.imread(IMAGE)
    sat = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 1].astype(float)
    rng = np.random.default_rng(20260801)
    total = 250_000
    for size in (18, 20, 22, 24, 26, 32):
        known, black = borders(size)
        rr, cc = np.nonzero(known)
        target = np.where(black[rr, cc], -1.0, 1.0)
        target -= target.mean()
        target /= np.linalg.norm(target)
        p = np.column_stack((
            rng.uniform(930, 1030, total), rng.uniform(690, 800, total),
            rng.uniform(390/size, 540/size, total), rng.uniform(-1.5, 2.0, total),
            rng.uniform(-3.0, 1.5, total), rng.uniform(210/size, 330/size, total),
            rng.uniform(-.05, .05, total), rng.uniform(-.05, .05, total)))
        top = -1.0
        for start in range(0, total, 2000):
            q = p[start:start+2000]
            x = np.rint(q[:,0,None]+cc*q[:,2,None]+rr*q[:,4,None]+cc*rr*q[:,6,None]).astype(int)
            y = np.rint(q[:,1,None]+cc*q[:,3,None]+rr*q[:,5,None]+cc*rr*q[:,7,None]).astype(int)
            values = sat[y,x]
            values -= values.mean(axis=1,keepdims=True)
            values /= np.sqrt((values*values).sum(axis=1,keepdims=True)+1e-9)
            top = max(top, float((values @ target).max()))
        print(size, f"{top:.6f}")


if __name__ == "__main__":
    main()
