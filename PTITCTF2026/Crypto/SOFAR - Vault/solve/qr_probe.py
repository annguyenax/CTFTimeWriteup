import sys
import numpy as np
import cv2

def find_qr_finders(gray, verbose=False):
    """Detect QR finder patterns (concentric squares) in grayscale image."""
    h, w = gray.shape
    # Binarize
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # find contours
    contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    finders = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 100:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < 10 or ch < 10:
            continue
        # aspect ~ square
        if abs(cw - ch) / max(cw, ch) > 0.3:
            continue
        # check for nested rings: contour hierarchy approach
        # simpler: check ratio of contour area to bounding box area
        bb_area = cw * ch
        fill = area / bb_area
        # outer ring of finder pattern has fill ~ (1 - (3/7)^2) ~ 0.82
        if 0.5 < fill < 0.95:
            finders.append((x + cw / 2, y + ch / 2, cw, ch))
    return finders

def try_decode(gray, label):
    det = cv2.QRCodeDetector()
    data, pts, _ = det.detectAndDecode(gray)
    if data:
        print(f'{label}: QR = {data!r}')
        return data
    return None

if __name__ == '__main__':
    path = sys.argv[1]
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('image', path, gray.shape[::-1])
    try_decode(gray, 'raw')
    # adaptive threshold variants
    for bs in (11, 21, 31, 51):
        ad = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, bs, 5)
        try_decode(ad, f'adapt{bs}')
        try_decode(255 - ad, f'adapt{bs}_inv')
    finders = find_qr_finders(gray)
    print('finders:', len(finders))
    for f in finders:
        print('  finder at', tuple(round(v, 1) for v in f[:2]), 'size', f[2])
