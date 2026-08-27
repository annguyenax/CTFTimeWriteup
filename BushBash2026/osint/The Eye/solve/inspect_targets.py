import contextlib
import glob
import io
import os
import sys

import cv2
import numpy as np
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

image = cv2.imread("dots.png")
word_points = np.array([[w[0], w[1]] for w in oc.words])
tree = cKDTree(word_points)
b, g, r = cv2.split(image)
red = (r > 90) & (r > g * 1.35) & (r > b * 1.35)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"), np.ones((7, 7), np.uint8)) > 0] = 0
n, labels, stats, centers = cv2.connectedComponentsWithStats((gray > 15).astype("uint8"))
sources = np.array([centers[i] for i in range(1, n) if stats[i, 4] >= 2])
source_tree = cKDTree(sources)
for path in sorted(glob.glob("target_*.png")):
    crop = cv2.imread(path)
    score = cv2.matchTemplate(image, crop, cv2.TM_CCOEFF_NORMED)
    _, maximum, _, top_left = cv2.minMaxLoc(score)
    center = np.array([top_left[0] + crop.shape[1] / 2, top_left[1] + crop.shape[0] / 2])
    d, idx = tree.query(center, k=8)
    print(os.path.basename(path), "match", maximum, "top_left", top_left, "center", center.tolist())
    for distance, i in zip(d, idx):
        print(" ", int(i), oc.codes[int(i)], "xy", word_points[int(i)].tolist(), "center_distance", round(float(distance), 2))
    sd, si = source_tree.query(center, k=8)
    print(" nearest sources:")
    for source_distance, source_i in zip(sd, si):
        source = sources[int(source_i)]
        wd, wi = tree.query(source + [0, 18])
        print("  source", np.round(source, 2).tolist(), "center_distance", round(float(source_distance), 2), "label", int(wi), oc.codes[int(wi)], "label_offset", round(float(wd), 2))
