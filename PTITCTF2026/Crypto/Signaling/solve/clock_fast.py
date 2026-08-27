#!/usr/bin/env python3
"""Fast 8-ray hand + 8-sector extractor."""
from pathlib import Path
import json
import math
import cv2
import numpy as np

VID = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4")
OUT = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out")
OUT.mkdir(exist_ok=True)
NAMES = ["12", "1:30", "3", "4:30", "6", "7:30", "9", "10:30"]

c = cv2.VideoCapture(str(VID))
ok, fr = c.read()
h, w = fr.shape[:2]
cx, cy = w // 2, h // 2
g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
hub = g[cy-30:cy+30, cx-30:cx+30]
yy, xx = np.unravel_index(np.argmax(hub), hub.shape)
cy = cy - 30 + int(yy)
cx = cx - 30 + int(xx)
print("center", cx, cy, "size", w, h, flush=True)

def rayscores(g):
    hs = []
    ss = []
    for k in range(8):
        a = math.radians(k * 45)  # 0=up
        # clock: 0 up, clockwise: dx = sin, dy = -cos (y down)
        dx, dy = math.sin(a), -math.cos(a)
        hv = []
        sv = []
        for r in range(60, 170):
            x = int(round(cx + dx * r))
            y = int(round(cy + dy * r))
            if 0 <= x < w and 0 <= y < h:
                hv.append(int(g[y, x]))
        for r in range(220, 320):
            x = int(round(cx + dx * r))
            y = int(round(cy + dy * r))
            if 0 <= x < w and 0 <= y < h:
                sv.append(int(g[y, x]))
        hs.append(float(np.percentile(hv, 85)) if hv else 0)
        ss.append(float(np.mean(sv)) if sv else 0)
    return hs, ss

c.set(cv2.CAP_PROP_POS_FRAMES, 0)
seq = []
i = 0
while True:
    ok, fr = c.read()
    if not ok:
        break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    hs, ss = rayscores(g)
    order = list(np.argsort(hs)[::-1])
    p = (int(order[0]), int(order[1]))
    if hs[order[1]] < 200:  # white hands are ~230+
        p = (p[0], p[0])
    sarr = np.array(ss)
    th = (sarr.max() + sarr.min()) * 0.5 + 3
    lit = [j for j in range(8) if sarr[j] > th]
    seq.append((i, p, lit, [round(x) for x in hs], [round(x) for x in ss]))
    i += 1
print("frames", i, flush=True)

runs = []
cur = None
for i, p, lit, hs, ss in seq:
    key = (p, tuple(lit))
    if key != cur:
        runs.append([i, 1, p, lit])
        cur = key
    else:
        runs[-1][1] += 1

print("all runs", len(runs), "long>=5", sum(1 for r in runs if r[1] >= 5), flush=True)
stable = [r for r in runs if r[1] >= 5]
for st, n, p, lit in stable:
    print(f"f{st:3d}+{n:3d}  {NAMES[p[0]]:>5s} {NAMES[p[1]]:>5s}  lit={lit}  {p}", flush=True)

# Semaphore tables: two-arm positions as frozenset of 8 dirs (0=12 clockwise)
# From Wikipedia (signaller): I'll try a generated table later.
pairs = [r[2] for r in stable]
print("pair sequence:")
print(pairs)

(OUT/"clock_fast.json").write_text(json.dumps({"center":[cx,cy],"stable":stable,"pairs":pairs}, indent=1))
print("done")
