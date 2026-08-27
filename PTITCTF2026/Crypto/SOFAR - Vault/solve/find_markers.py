import cv2, numpy as np, os, sys

base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
name = sys.argv[1]
img = cv2.imread(os.path.join(base, name+'.png'))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H, S, V = cv2.split(hsv)
print(name, 'shape', img.shape)

# Find bright non-green regions: high saturation and high value (colored markers)
mask = (S > 60) & (V > 100)
# remove green pitch: hue in green range (H 35-85 in OpenCV 0-179)
mask_green = (H > 35) & (H < 90) & (S > 60)
mask = mask & ~mask_green
mask = mask.astype(np.uint8)*255
kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
n, labels, stats, cents = cv2.connectedComponentsWithStats(mask, 8)
items = []
for i in range(1, n):
    x, y, w, h, area = stats[i]
    if area < 40 or w < 8 or h < 8:
        continue
    # markers likely squarish/round
    items.append((y+h//2, x+w//2, w, h, area))
items.sort()
print('component count (filtered):', len(items))
for cy, cx, w, h, area in items:
    print(f'  cy={cy:4d} cx={cx:4d} w={w:3d} h={h:3d} area={area}')
