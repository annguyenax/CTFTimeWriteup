#!/usr/bin/env python3
"""High-res binary preview of auth.png: black-ish px -> #, else space."""
import sys
from PIL import Image
import numpy as np

PATH = r"D:\download\CTFTimeWriteup\L3akCTF2026\hardware\Software is a Scam\files\auth.png"
COLS = int(sys.argv[1]) if len(sys.argv) > 1 else 160
ROWS = int(sys.argv[2]) if len(sys.argv) > 2 else 120

im = Image.open(PATH).convert("L")
a = np.asarray(im, dtype=np.uint8)
h, w = a.shape
dark = a < 128

step_y = max(1, h // ROWS)
step_x = max(1, w // COLS)
for y in range(0, h, step_y):
    line = ""
    for x in range(0, w, step_x):
        block = dark[y:y+step_y, x:x+step_x]
        line += "#" if block.mean() > 0.15 else " "
    print(line)
