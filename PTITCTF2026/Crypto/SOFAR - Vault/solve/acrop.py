import cv2, numpy as np, os, sys

base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'

def ascii_crop(f, x0, y0, x1, y1, w=None, invert=False):
    im = cv2.imread(os.path.join(base, f + ('.png' if not f.endswith('.png') else '')), cv2.IMREAD_GRAYSCALE)
    a = im[y0:y1, x0:x1]
    if invert:
        a = 255 - a
    h, ww = a.shape
    if w and w < ww:
        a2 = cv2.resize(a, (w, max(1, int(h * w / ww))), interpolation=cv2.INTER_AREA)
    else:
        a2 = a
    chars = ' .:-=+*#%@'
    out = []
    for row in a2:
        out.append(''.join(chars[min(9, int(v / 25.6))] for v in row))
    return '\n'.join(out)

if __name__ == '__main__':
    f = sys.argv[1]
    x0, y0, x1, y1 = [int(v) for v in sys.argv[2:6]]
    w = int(sys.argv[6]) if len(sys.argv) > 6 else None
    inv = len(sys.argv) > 7 and sys.argv[7] == 'inv'
    print(ascii_crop(f, x0, y0, x1, y1, w, inv))
