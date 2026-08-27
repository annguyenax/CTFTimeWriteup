import contextlib
import io
import sys

import cv2
import numpy as np
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

im = cv2.imread("dots.png")
b, g, r = cv2.split(im)
red = (r > 90) & (r > g * 1.35) & (r > b * 1.35)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"), np.ones((7, 7), np.uint8)) > 0] = 0
n, labels, stats, _ = cv2.connectedComponentsWithStats((gray > 15).astype("uint8"))
flat = labels.ravel()
wt = gray.ravel().astype(float)
yy, xx = np.indices(gray.shape)
flux = np.bincount(flat, weights=wt, minlength=n)
sx = np.bincount(flat, weights=wt * xx.ravel(), minlength=n)
sy = np.bincount(flat, weights=wt * yy.ravel(), minlength=n)
word_points = np.array([[w[0], w[1]] for w in oc.words])
tree = cKDTree(word_points)
for rank, i in enumerate(np.argsort(flux[1:])[::-1] + 1, 1):
    if stats[i, 4] < 3 or flux[i] <= 0:
        continue
    x, y = sx[i] / flux[i], sy[i] / flux[i]
    # Labels are normally 8--35 pixels below their source.
    candidates = tree.query_ball_point([x, y + 18], 45)
    candidates = [j for j in candidates if 5 <= word_points[j, 1] - y <= 42 and abs(word_points[j, 0] - x) <= 35]
    if candidates:
        j = min(candidates, key=lambda z: np.linalg.norm(word_points[z] - [x, y + 18]))
        print(rank, round(x, 1), round(y, 1), j, oc.codes[j], "word", word_points[j].tolist(), "flux", round(flux[i], 1))
    else:
        print(rank, round(x, 1), round(y, 1), None, None, "flux", round(flux[i], 1))
    if rank >= 80:
        break
