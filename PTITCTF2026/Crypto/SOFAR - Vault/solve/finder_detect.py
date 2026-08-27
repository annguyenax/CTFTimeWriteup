import sys
import numpy as np
import cv2

def detect_finder_patterns(gray, min_size=20):
    """Detect QR finder patterns using the 1:1:3:1:1 scanline signature."""
    h, w = gray.shape
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    finders = []
    # scan rows for 1:1:3:1:1 dark:light:dark:light:dark patterns
    for y in range(min_size, h - min_size, 2):
        row = bw[y, :]
        # find runs
        runs = []
        in_dark = row[0] == 0
        start = 0
        for x in range(1, w):
            dark = row[x] == 0
            if dark != in_dark:
                runs.append((start, x - 1, in_dark))
                start = x
                in_dark = dark
        runs.append((start, w - 1, in_dark))
        # look for 5-run sequence dark-light-dark-light-dark with ratios 1:1:3:1:1
        for i in range(len(runs) - 4):
            r1, r2, r3, r4, r5 = runs[i:i+5]
            if not (r1[2] and not r2[2] and r3[2] and not r4[2] and r5[2]):
                continue
            l1 = r1[1] - r1[0] + 1
            l2 = r2[1] - r2[0] + 1
            l3 = r3[1] - r3[0] + 1
            l4 = r4[1] - r4[0] + 1
            l5 = r5[1] - r5[0] + 1
            if l1 < 3 or l3 < 3:
                continue
            # check ratios
            s = l1 + l2 + l3 + l4 + l5
            # ideal: 1:1:3:1:1 -> l3 ~ 3*l1, l2 ~ l1, l4 ~ l1, l5 ~ l1
            if 0.6*l1 < l2 < 1.8*l1 and 0.6*l1 < l4 < 1.8*l1 and 0.6*l1 < l5 < 1.8*l1:
                if 2.0*l1 < l3 < 4.5*l1:
                    cx = (r1[0] + r5[1]) / 2
                    size = l3
                    finders.append((cx, y, size))
    return finders

def cluster_finders(finders, dist=60):
    """Cluster nearby detections into unique finder centers."""
    clusters = []
    for cx, cy, size in finders:
        placed = False
        for cl in clusters:
            if abs(cl[0] - cx) < dist and abs(cl[1] - cy) < dist:
                cl[0] = (cl[0] + cx) / 2
                cl[1] = (cl[1] + cy) / 2
                cl[2] = max(cl[2], size)
                placed = True
                break
        if not placed:
            clusters.append([cx, cy, size])
    return clusters

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('image:', path, gray.shape[::-1])
    finders = detect_finder_patterns(gray)
    clusters = cluster_finders(finders)
    print('raw finder hits:', len(finders), 'clustered:', len(clusters))
    for c in sorted(clusters, key=lambda c: (c[1], c[0])):
        print('  finder at (%.1f, %.1f) size %.1f' % (c[0], c[1], c[2]))
