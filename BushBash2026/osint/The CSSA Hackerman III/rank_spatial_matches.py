import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def hull_fraction(points, width, height):
    if len(points) < 3:
        return 0.0
    hull = cv2.convexHull(np.float32(points))
    return float(cv2.contourArea(hull) / (width * height))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("dirs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = cv2.imread(str(args.source), cv2.IMREAD_GRAYSCALE)
    sh, sw = source.shape
    sift = cv2.SIFT_create(nfeatures=5000)
    kp1, des1 = sift.detectAndCompute(source, None)
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    images = [p for d in args.dirs for p in d.glob("*.jpg") if "top" not in p.name and "contact" not in p.name]
    rows = []
    for index, path in enumerate(images, 1):
        target = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if target is None:
            continue
        th, tw = target.shape
        kp2, des2 = sift.detectAndCompute(target, None)
        if des2 is None:
            continue
        pairs = matcher.knnMatch(des1, des2, k=2)
        good = [m for m, n in pairs if m.distance < 0.72 * n.distance]
        inliers = 0
        src_area = dst_area = score = 0.0
        quadrants = 0
        if len(good) >= 4:
            src = np.float32([kp1[m.queryIdx].pt for m in good])
            dst = np.float32([kp2[m.trainIdx].pt for m in good])
            matrix, mask = cv2.findHomography(src.reshape(-1, 1, 2), dst.reshape(-1, 1, 2), cv2.RANSAC, 4.0)
            if matrix is not None and mask is not None:
                keep = mask.ravel().astype(bool)
                inliers = int(keep.sum())
                src_kept, dst_kept = src[keep], dst[keep]
                src_area = hull_fraction(src_kept, sw, sh)
                dst_area = hull_fraction(dst_kept, tw, th)
                occupied = set((int(x >= sw / 2), int(y >= sh / 2)) for x, y in src_kept)
                quadrants = len(occupied)
                score = inliers * np.sqrt(src_area * dst_area) * (0.5 + quadrants / 4)
        rows.append({"path": str(path), "good": len(good), "inliers": inliers,
                     "source_hull_fraction": src_area, "target_hull_fraction": dst_area,
                     "source_quadrants": quadrants, "spatial_score": float(score)})
        if index % 250 == 0:
            print(f"processed {index}/{len(images)}", flush=True)
    rows.sort(key=lambda row: (row["spatial_score"], row["inliers"]), reverse=True)
    args.output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    for row in rows[:40]:
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
