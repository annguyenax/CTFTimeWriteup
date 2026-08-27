import sys
import numpy as np
import cv2
from pyzbar import pyzbar

def find_finder_centers(gray):
    """Find QR finder patterns by scanning for 1:1:3:1:1 ratios in rows AND columns."""
    h, w = gray.shape
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    centers = []

    def scan_runs(seq):
        runs = []
        cur = seq[0]
        start = 0
        for i in range(1, len(seq)):
            if seq[i] != cur:
                runs.append((start, i - 1, cur))
                start = i
                cur = seq[i]
        runs.append((start, len(seq) - 1, cur))
        return runs

    def check_ratios(r):
        # pattern dark(1):light(1):dark(3):light(1):dark(1)
        if len(r) != 5:
            return False
        if not (r[0][2] and not r[1][2] and r[2][2] and not r[3][2] and r[4][2]):
            return False
        l1 = r[0][1] - r[0][0] + 1
        l2 = r[1][1] - r[1][0] + 1
        l3 = r[2][1] - r[2][0] + 1
        l4 = r[3][1] - r[3][0] + 1
        l5 = r[4][1] - r[4][0] + 1
        if min(l1, l2, l3, l4, l5) < 3:
            return False
        # ratios approx 1:1:3:1:1 with tolerance
        if not (0.6 < l2 / l1 < 1.7 and 0.6 < l4 / l1 < 1.7 and 0.6 < l5 / l1 < 1.7):
            return False
        if not (2.0 < l3 / l1 < 4.5):
            return False
        return True

    row_hits = []
    for y in range(h):
        row = (bw[y, :] == 0).astype(np.uint8)
        runs = scan_runs(row)
        for i in range(len(runs) - 4):
            if check_ratios(runs[i:i + 5]):
                r0, r2, r4 = runs[i], runs[i + 2], runs[i + 4]
                cx = (r0[0] + r4[1]) / 2
                row_hits.append((cx, y))

    col_hits = []
    for x in range(w):
        col = (bw[:, x] == 0).astype(np.uint8)
        runs = scan_runs(col)
        for i in range(len(runs) - 4):
            if check_ratios(runs[i:i + 5]):
                r0, r2, r4 = runs[i], runs[i + 2], runs[i + 4]
                cy = (r0[0] + r4[1]) / 2
                col_hits.append((x, cy))

    # Intersections of row and col hits
    grid = {}
    for cx, cy in row_hits:
        key = (round(cx / 8), round(cy / 8))
        grid.setdefault(key, []).append((cx, cy))
    centers = []
    for key, pts in grid.items():
        # find matching column hit near the same point
        cx = np.mean([p[0] for p in pts])
        cy = np.mean([p[1] for p in pts])
        # verify a col hit near here
        near = [(x, y) for x, y in col_hits if abs(x - cx) < 25 and abs(y - cy) < 25]
        if near:
            centers.append((cx, cy))
    return centers

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    print('image:', path, (w, h))
    centers = find_finder_centers(gray)
    print('finder centers:', len(centers))
    for c in sorted(centers, key=lambda c: (c[1], c[0])):
        print('  (%.1f, %.1f)' % (c[0], c[1]))
