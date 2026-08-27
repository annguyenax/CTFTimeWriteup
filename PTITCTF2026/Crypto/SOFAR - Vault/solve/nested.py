import sys
import numpy as np
import cv2

def find_nested_squares(gray, min_size=10):
    """Find nested square structures via contour hierarchy."""
    h, w = gray.shape
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 100:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < 8 or ch < 8:
            continue
        if abs(cw - ch) / max(cw, ch) > 0.35:
            continue
        bb = cw * ch
        fill = area / bb
        # outer square: mostly filled
        if fill < 0.4 or fill > 0.99:
            continue
        hc = hierarchy[0][i]
        # need at least a child
        if hc[2] == -1:
            continue
        # walk children to find depth
        depth = 0
        cur = hc[2]
        seen = set()
        while cur != -1 and cur not in seen:
            seen.add(cur)
            depth += 1
            cur = hierarchy[0][cur][2]
            if depth > 6:
                break
        if depth >= 2:
            results.append((x + cw / 2, y + ch / 2, cw, ch, depth))
    return results

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('image:', path, gray.shape[::-1])
    res = find_nested_squares(gray)
    print('nested squares:', len(res))
    for r in sorted(res, key=lambda r: (r[1], r[0])):
        print('  (%.1f, %.1f) size %d depth %d' % (r[0], r[1], r[2], r[4]))
