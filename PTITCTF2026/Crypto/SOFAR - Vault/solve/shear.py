import sys
import numpy as np
from PIL import Image

def shear_correct(f, x0, y0, x1, y1, out, shear=0.0, scale=3):
    im = Image.open(f).convert('L').crop((x0, y0, x1, y1))
    a = np.array(im)
    h, w = a.shape
    # Apply horizontal shear: x' = x + shear * y
    if shear != 0:
        # Use affine transform via PIL
        import math
        # shear in PIL: data = (1, shear, 0, 0, 1, 0)
        im = im.transform(im.size, Image.AFFINE, (1, -shear, 0, 0, 1, 0), resample=Image.BICUBIC, fillcolor=255)
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    im.save(out)
    return im.size

if __name__ == '__main__':
    f, x0, y0, x1, y1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    shear = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
    scale = int(sys.argv[8]) if len(sys.argv) > 8 else 3
    print(shear_correct(f, x0, y0, x1, y1, out, shear, scale))
