#!/usr/bin/env python3
"""Extract 8-direction clock hands + outer sector bits from Signaling.mp4."""
from pathlib import Path
import json
import cv2
import numpy as np

VID = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4")
OUT = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out")
OUT.mkdir(exist_ok=True)

# 8 directions: 0=up (12 o'clock), then clockwise every 45°
# angle in screen coords: x right, y down. 12 o'clock is angle -90° in atan2(y,x) or atan2(-dy, dx) for math.
NAMES = ["12", "1:30", "3", "4:30", "6", "7:30", "9", "10:30"]

c = cv2.VideoCapture(str(VID))
ok, fr0 = c.read()
h, w = fr0.shape[:2]
print("size", w, h)
g0 = cv2.cvtColor(fr0, cv2.COLOR_BGR2GRAY)
# center: brightest in middle
cy, cx = h // 2, w // 2
# refine: look for hub
hub = g0[cy - 40 : cy + 40, cx - 40 : cx + 40]
yy, xx = np.unravel_index(np.argmax(hub), hub.shape)
cy = cy - 40 + int(yy)
cx = cx - 40 + int(xx)
print("center", cx, cy)

# precompute angle/radius
ys, xs = np.ogrid[0:h, 0:w]
dx = xs - cx
dy = cy - ys  # up is +y in clock coords
ang = (np.degrees(np.arctan2(dx, dy)) + 360) % 360  # 0 at 12, clockwise
rad = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)

inner = (rad > 55) & (rad < 175)
outer = (rad > 210) & (rad < 330)

c.set(cv2.CAP_PROP_POS_FRAMES, 0)
rows = []
idx = 0
while True:
    ok, fr = c.read()
    if not ok:
        break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    # 8 hand scores: mean of very bright pixels along ray
    hand_sc = []
    for k in range(8):
        a0 = k * 45
        # ±12° around ray
        d = np.minimum((ang - a0) % 360, (a0 - ang) % 360)
        m = inner & (d < 12)
        vals = g[m]
        # 90th percentile to catch white hands
        hand_sc.append(float(np.percentile(vals, 92)) if vals.size else 0.0)
    # 8 sector means
    sec = []
    for k in range(8):
        a0 = k * 45
        d = np.minimum((ang - a0) % 360, (a0 - ang) % 360)
        m = outer & (d < 22.5)
        sec.append(float(g[m].mean()) if m.any() else 0.0)
    rows.append({"i": idx, "hands": hand_sc, "sec": sec})
    idx += 1

print("frames", idx)

# pick 2 strongest hands
seq = []
for r in rows:
    hs = np.array(r["hands"])
    order = np.argsort(hs)[::-1]
    a, b = int(order[0]), int(order[1])
    if a > b:
        a, b = b, a
    # if second is weak, single hand
    gap = hs[order[0]] - hs[order[1]]
    pair = (int(order[0]), int(order[1])) if hs[order[1]] > hs.mean() + 8 else (int(order[0]), int(order[0]))
    # sectors lit: those above mid
    s = np.array(r["sec"])
    th = (s.max() + s.min()) / 2 + 2
    lit = [i for i in range(8) if s[i] > th]
    seq.append({"i": r["i"], "pair": pair, "scores": [round(x, 1) for x in hs], "lit": lit, "sec": [round(x, 1) for x in s]})

# run-length on pair
runs = []
cur = None
for s in seq:
    key = (tuple(s["pair"]), tuple(s["lit"]))
    if cur != key:
        runs.append({"start": s["i"], "n": 1, "pair": s["pair"], "lit": s["lit"], "names": [NAMES[s["pair"][0]], NAMES[s["pair"][1]]]})
        cur = key
    else:
        runs[-1]["n"] += 1

# filter short flicker
stable = [r for r in runs if r["n"] >= 4]
print("stable holds", len(stable))
for r in stable:
    print(f"  f{r['start']:3d}+{r['n']:3d}  hands {r['names']}  lit {r['lit']}")

# Semaphore (signaller facing us? try both)
# Positions 0=down? Standard diagram: 8 positions around.
# I'll use: letter from frozenset of two directions.

# Wikipedia flag semaphore (signaller's view, 0=down, clockwise from signaller's right):
# We'll brute a mapping.

def decode_pairs(pairs, table):
    return "".join(table.get(frozenset(p) if p[0] != p[1] else p[0], "?") for p in pairs)

# dump json
(OUT / "clock.json").write_text(json.dumps({"center": [cx, cy], "stable": stable, "seq_sample": seq[::10]}, indent=1), encoding="utf-8")
print("wrote clock.json")
