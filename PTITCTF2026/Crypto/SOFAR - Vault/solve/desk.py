import sys
import numpy as np
from PIL import Image

def deskew_band(f, x0, y0, x1, y1, angle, out, scale=3):
    """Rotate band by angle and save upscaled."""
    im = Image.open(f).convert('L').crop((x0, y0, x1, y1))
    im = im.rotate(angle, expand=False, fillcolor=255, resample=Image.BICUBIC)
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    im.save(out)

if __name__ == '__main__':
    f = r'files\extracted\SOFAR - Vault\F.png'
    deskew_band(f, 40, 440, 820, 960, 13, r'solve\F_deskewed.png', 4)
    print('saved')
