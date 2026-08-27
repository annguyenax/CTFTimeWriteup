import cv2
import numpy as np


ref = cv2.imread("reference_matariki.png")
dst = cv2.imread("dots.png")

def prepare(im, remove_red=False):
    out = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    if remove_red:
        b, g, r = cv2.split(im)
        red = (r > 80) & (r > g * 1.25) & (r > b * 1.25)
        out[cv2.dilate(red.astype("uint8"), np.ones((9, 9), np.uint8)) > 0] = 0
    return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(out)

g1 = prepare(ref)
g2 = prepare(dst, True)
sift = cv2.SIFT_create(nfeatures=15000, contrastThreshold=0.01, edgeThreshold=12)
k1, d1 = sift.detectAndCompute(g1, None)
k2, d2 = sift.detectAndCompute(g2, None)
print("keypoints", len(k1), len(k2))
matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
good = [a for a, b in matches if a.distance < 0.78 * b.distance]
print("ratio_matches", len(good))
if len(good) >= 4:
    src = np.float32([k1[m.queryIdx].pt for m in good])
    target = np.float32([k2[m.trainIdx].pt for m in good])
    H, mask = cv2.findHomography(src, target, cv2.RANSAC, 8.0)
    print("inliers", int(mask.sum()) if mask is not None else 0)
    print("homography", H.tolist() if H is not None else None)
    if H is not None:
        # Approximate star centers in the labelled Wikimedia reference, in
        # poem order. Refine each to the brightest local peak first.
        approx = np.array([
            [355, 435], [255, 505], [369, 566], [190, 380],
            [894, 269], [432, 137], [194, 253], [894, 210],
        ], dtype=float)
        refined = []
        for x, y in approx:
            x0, y0 = max(0, int(x - 18)), max(0, int(y - 18))
            roi = g1[y0:int(y + 19), x0:int(x + 19)]
            _, _, _, peak = cv2.minMaxLoc(roi)
            refined.append([x0 + peak[0], y0 + peak[1]])
        projected = cv2.perspectiveTransform(np.array([refined], np.float32), H)[0]
        print("reference_stars", refined)
        print("projected", np.round(projected, 2).tolist())
