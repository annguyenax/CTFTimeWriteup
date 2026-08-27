#!/usr/bin/env python3
"""Reproduce the two flag-shaped payloads; neither is scoreboard-verified."""
import struct

import numpy as np
from PIL import Image, ImageFilter

rgb = np.array(Image.open("anhcd.png").convert("RGB"), dtype=np.uint8)
bits = (rgb.reshape(-1) & 1).astype(np.uint8)
raw = np.packbits(bits, bitorder="big").tobytes()
length = struct.unpack(">I", raw[:4])[0]
lsb_candidate = raw[4 : 4 + length].decode("ascii")

gray = np.array(Image.open("anhcd.png").convert("L"), dtype=float)
freq = np.fft.fftshift(np.fft.fft2(gray))
mag = np.log(np.abs(freq) + 1)
scaled = (mag - mag.min()) / (mag.max() - mag.min()) * 255
view = Image.fromarray(scaled.astype("uint8"))
hp = np.array(view, float) - np.array(view.filter(ImageFilter.GaussianBlur(8)), float)
lo, hi = np.percentile(hp, [50, 99.5])
out = Image.fromarray((np.clip((hp - lo) / (hi - lo), 0, 1) * 255).astype("uint8"))
out.resize((gray.shape[1] * 5, gray.shape[0] * 5)).save("fft_flag.png")

print(f"LSB candidate ({length} bytes): {lsb_candidate}")
print("FFT visual candidate: PTITCTF{FFT_15_fun_bu7_700_3a5y_i_gu355}")
print("Status: candidate only; require exact scoreboard acceptance or a third payload.")
