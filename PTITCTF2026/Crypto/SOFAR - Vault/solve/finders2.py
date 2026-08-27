import sys
import numpy as np
import cv2

def find_finders_precise(gray):
    """Find QR finder patterns via nested square detection using contours + ratio checks."""
    h, w = gray.shape
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    # For each contour, check if it's a finder pattern: outer square containing a ring containing a square
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 200:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < 12 or ch < 12:
            continue
        if abs(cw - ch) / max(cw, ch) > 0.25:
            continue
        # must be square-ish and mostly filled (outer black square)
        bb_area = cw * ch
        fill = area / bb_area
        if fill < 0.5 or fill > 0.98:
            continue
        # check children: should have a nested white ring (child contour with child)
        if hierarchy is None:
            continue
        hchild = hierarchy[0][i]
        if hchild[2] == -1:
            continue
        child_idx = hchild[2]
        # find descendant chain: black->white->black (finder has 3 levels)
        # walk down children
        depth = 0
        cur = i
        seen = set()
        while True:
            if cur in seen:
                break
            seen.add(cur)
            hcur = hierarchy[0][cur]
            if hcur[2] == -1:
                break
            cur = hcur[2]
            depth += 1
            if depth > 5:
                break
        if depth >= 2:
            results.append((x + cw / 2, y + ch / 2, max(cw, ch)))
    return results

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('image:', path, gray.shape[::-1])
    fr = find_finders_precise(gray)
    print('nested-square candidates:', len(fr))
    for f in sorted(fr, key=lambda c: (c[1], c[0])):
        print('  (%.1f, %.1f) size %.1f' % (f[0], f[1], f[2]))
