#!/usr/bin/env python3
"""Angular histogram of bright inner-ring pixels → two hand directions."""
from pathlib import Path
import json, math
import cv2
import numpy as np

VID = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4")
c = cv2.VideoCapture(str(VID))
ok, fr = c.read()
h, w = fr.shape[:2]
cx, cy = 553, 673
ys, xs = np.ogrid[0:h, 0:w]
dx = xs - cx
dy = cy - ys
ang = (np.degrees(np.arctan2(dx, dy)) + 360) % 360
rad = np.sqrt(dx * dx + (ys - cy) ** 2)
inner = (rad > 70) & (rad < 130)  # avoid rim ticks at 12/3/6/9

c.set(cv2.CAP_PROP_POS_FRAMES, 0)
seq = []
i = 0
while True:
    ok, fr = c.read()
    if not ok:
        break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    m = inner & (g > 210)
    bins = np.zeros(360, dtype=np.int32)
    aa = ang[m].astype(np.int32) % 360
    for a in aa:
        bins[a] += 1
    # smooth
    sm = np.convolve(np.r_[bins[-15:], bins, bins[:15]], np.ones(11) / 11, mode="valid")
    # suppress exact tick neighborhoods? find two peaks 40+ deg apart
    peaks = []
    tmp = sm.copy()
    for _ in range(3):
        p = int(np.argmax(tmp))
        peaks.append((p % 360, float(tmp[p])))
        # zero ±20°
        for d in range(-20, 21):
            tmp[(p + d) % 360] = 0
    # quantize to 8
    q = [((p + 22) // 45) % 8 for p, _ in peaks[:2]]
    seq.append((i, peaks[:2], q))
    i += 1

print("frames", i)
# debug a few
for fi in (0, 40, 70, 100, 300, 450):
    print("f", fi, seq[fi])

# runs of quantized pair
runs = []
cur = None
for i, pk, q in seq:
    key = tuple(sorted(q[:2]))
    if key != cur:
        runs.append([i, 1, key, pk])
        cur = key
    else:
        runs[-1][1] += 1
stable = [r for r in runs if r[1] >= 5]
print("stable", len(stable))
NAMES = ["12", "1:30", "3", "4:30", "6", "7:30", "9", "10:30"]
for st, n, key, pk in stable:
    print(f"f{st:3d}+{n:3d}  {NAMES[key[0]]:>5s} {NAMES[key[1]]:>5s}  {key}  peaks={[p[0] for p in pk]}")

Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out\hands.json").write_text(
    json.dumps({"stable": [[st, n, list(key)] for st, n, key, pk in stable]}, indent=1)
)
print("wrote")
