#!/usr/bin/env python3
"""Re-extract lighthouse signals from Signaling.mp4."""
from pathlib import Path
import json
import cv2
import numpy as np

VID = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4")
OUT = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out")
OUT.mkdir(exist_ok=True)

c = cv2.VideoCapture(str(VID))
frames = []
sky_max = []
lamp = []
means = []
hists = []
idx = 0
saved = []
while True:
    ok, fr = c.read()
    if not ok:
        break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    frames.append(g)
    sky_max.append(float(g[150:400, 350:750].max()))
    lamp.append(float(g[660:710, 500:560].mean()))
    means.append(float(g.mean()))
    if idx in (0, 20, 40, 45, 70, 90, 120, 200, 300, 400, 500, 552) or idx % 50 == 0:
        p = OUT / f"f{idx:04d}.png"
        cv2.imwrite(str(p), fr)
        saved.append(idx)
    idx += 1
print("nframes", idx, "saved", saved)
np.save(OUT / "sky_max.npy", np.array(sky_max))
np.save(OUT / "lamp.npy", np.array(lamp))
print("sky", min(sky_max), max(sky_max), "median", float(np.median(sky_max)))
print("lamp", min(lamp), max(lamp))

# difference between consecutive frames — beam motion
diffs = [0.0]
for i in range(1, len(frames)):
    diffs.append(float(np.mean(np.abs(frames[i].astype(np.int16) - frames[i - 1].astype(np.int16)))))
print("diff mean", float(np.mean(diffs)), "max", max(diffs))

# polar peak around lamp
cy, cx = 684, 530
ys, xs = np.ogrid[0:frames[0].shape[0], 0:frames[0].shape[1]]
dy = ys - cy
dx = xs - cx
ang = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
rad = np.sqrt(dy ** 2 + dx ** 2)
mask = (rad > 80) & (rad < 420)
dirs = []
for g in frames:
    roi = g.astype(np.float32)
    roi = np.where(mask, roi, 0)
    # brightest 0.3% in ring
    flat = roi[mask]
    th = np.percentile(flat, 99.7)
    ys2, xs2 = np.where(mask & (g >= th))
    if len(xs2) == 0:
        dirs.append(None)
        continue
    # vector mean of bright pixels
    vx = float((xs2 - cx).mean())
    vy = float((ys2 - cy).mean())
    a = (np.degrees(np.arctan2(vy, vx)) + 360) % 360
    dirs.append(a)

# quantize to 4 diagonals
centers = [51, 127, 232, 307]


def nearest(a):
    if a is None:
        return -1
    ds = [(min(abs(a - c), 360 - abs(a - c)), i) for i, c in enumerate(centers)]
    return min(ds)[1]


q = [nearest(a) for a in dirs]
# runs
runs = []
cur, st = q[0], 0
for i in range(1, len(q)):
    if q[i] != cur:
        runs.append((st, i - 1, cur, i - st))
        cur, st = q[i], i
runs.append((st, len(q) - 1, cur, len(q) - st))
print("dir runs", len(runs))
for r in runs:
    print(r)

# sky ON/OFF
s = np.array(sky_max)
th = float(np.median(s) + 5)
bits = (s > th).astype(int)
bruns = []
cur, st = bits[0], 0
for i in range(1, len(bits)):
    if bits[i] != cur:
        bruns.append((int(st), int(i - 1), int(cur), int(i - st)))
        cur, st = bits[i], i
bruns.append((int(st), int(len(bits) - 1), int(cur), int(len(bits) - st)))
print("sky runs")
for r in bruns:
    print(r)

(OUT / "dirs.json").write_text(json.dumps({"q": q, "runs": runs, "sky": bruns}, indent=1), encoding="utf-8")
print("wrote", OUT)
