#!/usr/bin/env python3
"""Crop-based binary preview of auth.png.
Usage: crop_preview.py COLS ROWS [x0 y0 x1 y1]  (coords in px, default full image)
Black-ish px -> #, else space.
"""
import sys
from PIL import Image
import numpy as np

PATH = r"D:\download\CTFTimeWriteup\L3akCTF2026\hardware\Software is a Scam\files\auth.png"
COLS = int(sys.argv[1]); ROWS = int(sys.argv[2])
im = Image.open(PATH).convert("L")
a = np.asarray(im, dtype=np.uint8)
h, w = a.shape
if len(sys.argv) >= 7:
    x0, y0, x1, y1 = map(int, sys.argv[3:7])
else:
    x0, y0, x1, y1 = 0, 0, w, h
sub = a[y0:y1, x0:x1]
sh, sw = sub.shape
dark = sub < 128
step_y = max(1, sh // ROWS)
step_x = max(1, sw // COLS)
print(f"# crop x={x0}-{x1} y={y0}-{y1} ({sw}x{sh})")
for y in range(0, sh, step_y):
    line = ""
    for x in range(0, sw, step_x):
        block = dark[y:y+step_y, x:x+step_x]
        line += "#" if block.mean() > 0.15 else " "
    print(line)
