import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("dirs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = cv2.imread(str(args.source), cv2.IMREAD_GRAYSCALE)
    if source is None:
        raise SystemExit(f"Cannot read source: {args.source}")

    sift = cv2.SIFT_create(nfeatures=5000)
    kp1, des1 = sift.detectAndCompute(source, None)
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    rows = []

    images = []
    for directory in args.dirs:
        images.extend(p for p in directory.glob("*.jpg") if p.name.lower() != "top80.jpg")

    for idx, path in enumerate(images, 1):
        target = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if target is None:
            continue
        kp2, des2 = sift.detectAndCompute(target, None)
        if des2 is None:
            continue
        pairs = matcher.knnMatch(des1, des2, k=2)
        good = [m for m, n in pairs if m.distance < 0.72 * n.distance]
        inliers = 0
        median_error = None
        if len(good) >= 4:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            h, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if h is not None and mask is not None:
                inliers = int(mask.sum())
                projected = cv2.perspectiveTransform(src_pts, h)
                errors = np.linalg.norm(projected - dst_pts, axis=2).ravel()
                selected = errors[mask.ravel().astype(bool)]
                if selected.size:
                    median_error = float(np.median(selected))
        rows.append({
            "path": str(path),
            "good_matches": len(good),
            "inliers": inliers,
            "inlier_ratio": (inliers / len(good)) if good else 0,
            "median_error": median_error,
        })
        if idx % 100 == 0:
            print(f"processed {idx}/{len(images)}")

    rows.sort(key=lambda r: (r["inliers"], r["inlier_ratio"], r["good_matches"]), reverse=True)
    args.output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    for row in rows[:30]:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
