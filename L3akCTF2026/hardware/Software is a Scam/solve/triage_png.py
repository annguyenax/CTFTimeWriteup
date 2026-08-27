#!/usr/bin/env python3
"""Triage auth.png: chunk structure + content fingerprint (no image viewing)."""
import struct, sys, zlib
from PIL import Image
import numpy as np

PATH = r"D:\download\CTFTimeWriteup\L3akCTF2026\hardware\Software is a Scam\files\auth.png"

data = open(PATH, "rb").read()
print(f"file size: {len(data)}")

# --- chunk walk ---
pos = 8
chunks = []
while pos < len(data):
    ln = struct.unpack(">I", data[pos:pos+4])[0]
    typ = data[pos+4:pos+8].decode("latin1")
    chunks.append((typ, ln, pos))
    pos += 12 + ln
    if typ == "IEND":
        break
print(f"trailing bytes after IEND: {len(data) - pos}")
for typ, ln, p in chunks:
    print(f"  {typ} len={ln} at {p}")

# --- decompress IDAT and look at raw scanlines ---
idat = b"".join(data[p+8:p+8+ln] for typ, ln, p in chunks if typ == "IDAT")
try:
    raw = zlib.decompress(idat)
    print(f"IDAT decompressed: {len(raw)} bytes")
except Exception as e:
    print(f"IDAT decompress error: {e}")

# --- open image ---
im = Image.open(PATH)
print(f"mode={im.mode} size={im.size}")
rgb = im.convert("RGB")
a = np.asarray(rgb, dtype=np.uint8)
h, w, _ = a.shape
print(f"array shape {a.shape}")

# unique colors
uniq = np.unique(a.reshape(-1, 3), axis=0)
print(f"unique colors: {len(uniq)}")
# top colors
from collections import Counter
cnt = Counter(map(tuple, a.reshape(-1, 3)))
for c, n in cnt.most_common(12):
    print(f"  color {c} : {n} px ({100*n/(h*w):.2f}%)")

# alpha channel info (32bpp ARGB)
if im.mode == "RGBA":
    al = np.asarray(im)[:, :, 3]
    print(f"alpha min/max: {al.min()}/{al.max()}, transparent px: {(al==0).sum()}")

# --- downsample ascii preview (luminance) ---
gray = a.mean(axis=2)
def ascii_preview(g, cols=120, rows=60):
    gh, gw = g.shape
    step_y = max(1, gh // rows)
    step_x = max(1, gw // cols)
    out = []
    ramp = " .:-=+*#%@"
    for y in range(0, gh, step_y):
        line = ""
        for x in range(0, gw, step_x):
            v = g[y:y+step_y, x:x+step_x].mean()
            line += ramp[min(9, int(v / 25.6))]
        out.append(line)
    return "\n".join(out)

print("\n=== ASCII preview (luminance, %dx%d) ===" % (120, 60))
print(ascii_preview(gray))
