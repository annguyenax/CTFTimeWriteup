#!/usr/bin/env python3
import cv2
import numpy as np

im = cv2.imread(r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png")
sat = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 1].astype(float)
size = 20
known = np.zeros((size, size), bool)
black = np.zeros((size, size), bool)
known[:, 0] = known[-1, :] = known[0, :] = known[:, -1] = True
black[:, 0] = black[-1, :] = True
black[0, :] = np.arange(size) % 2 == 0
black[:, -1] = np.arange(size) % 2 == 1
rr, cc = np.nonzero(known)
targets = []
for k in range(4):
    target = np.where(np.rot90(black, k)[rr, cc], -1.0, 1.0)
    target -= target.mean()
    target /= np.linalg.norm(target)
    targets.append(target)

rng = np.random.default_rng(20260801)
total = 1_000_000
params = np.column_stack((
    rng.uniform(930, 1030, total), rng.uniform(690, 800, total),
    rng.uniform(18, 25, total), rng.uniform(-2, 2, total),
    rng.uniform(-3, 2, total), rng.uniform(10, 17, total),
    rng.uniform(-.05, .05, total), rng.uniform(-.05, .05, total)))
best = [(-1.0, None) for _ in targets]
for start in range(0, total, 2000):
    p = params[start:start + 2000]
    x = np.rint(p[:, 0, None] + cc*p[:, 2, None] + rr*p[:, 4, None] + cc*rr*p[:, 6, None]).astype(int)
    y = np.rint(p[:, 1, None] + cc*p[:, 3, None] + rr*p[:, 5, None] + cc*rr*p[:, 7, None]).astype(int)
    values = sat[y, x]
    values -= values.mean(1, keepdims=True)
    values /= np.sqrt((values*values).sum(1, keepdims=True) + 1e-9)
    for k, target in enumerate(targets):
        scores = values @ target
        i = int(scores.argmax())
        if scores[i] > best[k][0]:
            best[k] = (float(scores[i]), p[i].copy())
for k, (score, geometry) in enumerate(best):
    print(k, score, geometry)
