#!/usr/bin/env python3
"""Probe schematic.png: size, palette, LSB stego check, tesseract search."""
import os
import struct
from PIL import Image

P = r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\It's Oops PM\files\_work\hardware_its_oops_pm\schematic.png"
im = Image.open(P)
print("size", im.size, "mode", im.mode, "format", im.format)

# sample colors
im2 = im.convert("RGB")
colors = im2.getcolors(maxcolors=10_000_000)
colors.sort(reverse=True)
print("top colors:", colors[:8])

# LSB check: extract LSBs of each channel in order and look for ASCII runs
w, h = im2.size
px = im2.load()
bits = []
for y in range(0, h, 1):
    for x in range(0, w, 1):
        r, g, b = px[x, y]
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)
# convert to bytes
byts = bytearray()
for i in range(0, len(bits) - 7, 8):
    v = 0
    for b in bits[i:i + 8]:
        v = (v << 1) | b
    byts.append(v)
data = bytes(byts)
print("lsb bytes:", len(data))
import re
for m in re.finditer(rb"HTB\{[^}]{0,80}\}", data):
    print("LSB FLAG:", m.group(0))
for m in re.finditer(rb"[ -~]{8,}", data[:500000]):
    print("LSB ascii:", m.group(0)[:200])
print("done")
