from PIL import Image
import numpy as np

img = Image.open(r'files\extracted\SOFAR - Vault\F.png').convert('L')
a = np.array(img)
band = Image.fromarray(a[430:960, 30:830]).rotate(13, expand=False, fillcolor=255, resample=Image.BICUBIC)
ba = np.array(band)
dark = (ba < 170).astype(np.uint8)
rowsum = dark.sum(axis=1)
# find line bands
in_band = False
lines = []
for y in range(len(rowsum)):
    v = rowsum[y] > 8
    if v and not in_band:
        start = y
        in_band = True
    elif not v and in_band:
        lines.append((start, y - 1))
        in_band = False
if in_band:
    lines.append((start, len(rowsum) - 1))
print('text line bands in rotated band (y0,y1):')
for a0, b in lines:
    if b - a0 > 3:
        print(f'  {a0}-{b} height={b-a0+1}')
