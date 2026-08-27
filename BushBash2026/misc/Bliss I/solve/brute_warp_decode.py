#!/usr/bin/env python3
import cv2
import numpy as np
import zxingcpp

SRC = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"
OUT = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\solve\warp_decoded.png"

im = cv2.imread(SRC)
rng = np.random.default_rng(20260801)
base = np.float32([[970, 726], [1389, 742], [1389, 967], [970, 967]])
dst = np.float32([[0, 0], [479, 0], [479, 479], [0, 479]])

for attempt in range(6000):
    jitter = rng.normal(0, [18, 14], (4, 2)).astype(np.float32)
    src = base + jitter
    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(im, matrix, (480, 480))
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    candidates = []
    for threshold in (45, 65, 85, 105, 125, 145, 165):
        binary = np.where(hsv[:, :, 1] < threshold, 0, 255).astype(np.uint8)
        candidates.append(binary)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    candidates.extend([otsu, 255 - otsu])
    for candidate in candidates:
        padded = cv2.copyMakeBorder(candidate, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=255)
        result = zxingcpp.read_barcode(padded, try_rotate=True, try_invert=True)
        if result and result.text:
            print("attempt", attempt, "corners", src.tolist())
            print(result.format, repr(result.text))
            cv2.imwrite(OUT, padded)
            raise SystemExit
print("No decode")
