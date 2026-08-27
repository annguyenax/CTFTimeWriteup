import sys
import numpy as np
from PIL import Image

# Read the F.png rotated band and dump rows as ASCII to identify text lines
img = Image.open(r'files\extracted\SOFAR - Vault\F.png').convert('L')
a = np.array(img)
band = Image.fromarray(a[430:960, 30:830]).rotate(13, expand=False, fillcolor=255, resample=Image.BICUBIC)
ba = np.array(band)
h, w = ba.shape

# Find text lines: rows with many dark pixels
dark = (ba < 170).astype(np.uint8)
rowsum = dark.sum(axis=1)
lines = []
in_band = False
for y in range(h):
    v = rowsum[y] > 15
    if v and not in_band:
        start = y
        in_band = True
    elif not v and in_band:
        if y - start > 4:
            lines.append((start, y - 1))
        in_band = False
if in_band:
    lines.append((start, h - 1))

print('num lines:', len(lines))
for i, (a0, b) in enumerate(lines):
    print(f'line {i}: y={a0}-{b} h={b-a0+1}')
