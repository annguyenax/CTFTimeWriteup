import sys
import numpy as np
import cv2
from pyzbar import pyzbar

def find_finder_quads(gray):
    """Find QR finder patterns using contour hierarchy (nested squares)."""
    h, w = gray.shape
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 300:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < 15 or ch < 15:
            continue
        if abs(cw - ch) / max(cw, ch) > 0.3:
            continue
        bb_area = cw * ch
        fill = area / bb_area
        if fill < 0.45 or fill > 0.98:
            continue
        hc = hierarchy[0][i]
        if hc[2] == -1:
            continue
        # count descendant depth (ring structure)
        depth = 0
        cur = hc[2]
        seen = set()
        while cur != -1 and cur not in seen:
            seen.add(cur)
            depth += 1
            cur = hierarchy[0][cur][2]
            if depth > 8:
                break
        if depth >= 2:
            results.append((x + cw / 2, y + ch / 2, cw, ch))
    return results

def cluster(pts, dist=60):
    clusters = []
    for x, y, cw, ch in pts:
        placed = False
        for cl in clusters:
            if abs(cl[0] - x) < dist and abs(cl[1] - y) < dist:
                cl[0] = (cl[0] + x) / 2
                cl[1] = (cl[1] + y) / 2
                cl[2] = max(cl[2], cw)
                cl[3] = max(cl[3], ch)
                placed = True
                break
        if not placed:
            clusters.append([x, y, cw, ch])
    return clusters

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    print('image:', path, (w, h))
    quads = find_finder_quads(gray)
    clusters = cluster(quads)
    print('finder-like quads:', len(quads), 'clustered:', len(clusters))
    for c in sorted(clusters, key=lambda c: (c[1], c[0])):
        print('  (%.1f, %.1f) size %.1f' % (c[0], c[1], c[2]))
