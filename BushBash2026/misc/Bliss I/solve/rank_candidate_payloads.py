#!/usr/bin/env python3
"""Compare candidate payload encodings to the cloud without claiming a decode."""

import cv2
import numpy as np
import zxingcpp


IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"
CANDIDATES = [
    "bushbash{atmospherically-questionable-runes}",
    "atmospherically-questionable-runes",
    "/atmospherically-questionable-runes",
    "bushbash{alWaY$-quEsTi0N-yoUR-m3d1a!}",
    "bushbash{this-is-a-random-decoy-string!!}",
]


def patterns(text: str):
    barcode = zxingcpp.create_barcode(text, zxingcpp.BarcodeFormat.DataMatrix)
    image = np.asarray(zxingcpp.write_barcode_to_image(barcode, 1, False, False))
    if image.shape[0] != image.shape[1]:
        return image.shape[0], []
    black = image < 128
    out = []
    for k in range(4):
        rotated = np.rot90(black, k)
        out.extend([rotated, np.fliplr(rotated)])
    return image.shape[0], [np.where(x, 1.0, -1.0).ravel() for x in out]


def main():
    image = cv2.imread(IMAGE)
    sat = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1].astype(float)
    grouped = {}
    for text in CANDIDATES:
        size, pats = patterns(text)
        grouped.setdefault(size, []).append((text, pats))

    for size, candidates in grouped.items():
        rng = np.random.default_rng(20260801 + size)
        total = 500_000
        p = np.column_stack((
            rng.uniform(930, 1030, total), rng.uniform(690, 800, total),
            rng.uniform(390/size, 540/size, total), rng.uniform(-1.5, 2.0, total),
            rng.uniform(-3.0, 1.5, total), rng.uniform(210/size, 330/size, total),
            rng.uniform(-.05, .05, total), rng.uniform(-.05, .05, total)))
        rr, cc = np.indices((size, size)); rr=rr.ravel(); cc=cc.ravel()
        scores = {text: -1.0 for text, _ in candidates}
        for start in range(0,total,1000):
            q=p[start:start+1000]
            x=np.rint(q[:,0,None]+cc*q[:,2,None]+rr*q[:,4,None]+cc*rr*q[:,6,None]).astype(int)
            y=np.rint(q[:,1,None]+cc*q[:,3,None]+rr*q[:,5,None]+cc*rr*q[:,7,None]).astype(int)
            values=sat[y,x]; values-=values.mean(axis=1,keepdims=True)
            values/=np.sqrt((values*values).sum(axis=1,keepdims=True)+1e-9)
            for text,pats in candidates:
                scores[text]=max(scores[text],max(float(np.abs(values@pat/np.linalg.norm(pat)).max()) for pat in pats))
        for text,score in scores.items(): print(size,f"{score:.6f}",text)


if __name__ == "__main__":
    main()
