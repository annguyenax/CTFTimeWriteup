import sys
import numpy as np
from PIL import Image

def ascii_crop(f, x0, y0, x1, y1, w=None):
    im = Image.open(f).convert('L').crop((x0, y0, x1, y1))
    a = np.array(im)
    h, ww = a.shape
    if w and w < ww:
        im2 = im.resize((w, max(1, int(h * w / ww))))
        a2 = np.array(im2)
    else:
        a2 = a
    chars = ' .:-=+*#%@'
    return '\n'.join(''.join(chars[min(9, int(v / 25.6))] for v in row) for row in a2)

if __name__ == '__main__':
    f = sys.argv[1]
    x0, y0, x1, y1 = [int(v) for v in sys.argv[2:6]]
    w = int(sys.argv[6]) if len(sys.argv) > 6 else None
    print(ascii_crop(f, x0, y0, x1, y1, w))
