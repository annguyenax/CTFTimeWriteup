#!/usr/bin/env python3
"""
LIT2026 / crypto / faulty_image_3

The visible red text "LITCTF{1mAg3_F1ag_1o3fjs!}" is a DECOY.

The real flag is hidden in the orange BORDER. On the very top row (y=0) there are
30 pixels spaced every 7px whose colour differs from the orange border (they look
blue-ish / "colorful"). Their RED channel byte values spell the flag; the G/B
channels are just noise to make the marks look colored.
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else 'files/corrupt3.png'
ORANGE = (255, 157, 0)


def solve():
    a = np.array(Image.open(SRC).convert('RGB'))
    row0 = a[0, :, :]
    marks = [tuple(int(v) for v in row0[x]) for x in range(a.shape[1])
             if tuple(int(v) for v in row0[x]) != ORANGE]
    flag = bytes(m[0] for m in marks)          # RED channel of each mark
    return flag.decode()


if __name__ == '__main__':
    print(solve())
