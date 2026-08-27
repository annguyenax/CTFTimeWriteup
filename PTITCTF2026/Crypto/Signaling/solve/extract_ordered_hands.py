#!/usr/bin/env python3
"""Extract ordered clock hands and decode the first semaphore layer."""

from pathlib import Path
import math

import cv2
import numpy as np

VIDEO = Path(__file__).parents[1] / "files" / "extracted" / "Signaling" / "Signaling.mp4"
CX, CY = 540, 675

SEMAPHORE = {
    frozenset(pair): letter
    for letter, pair in {
        "A": (5, 4), "B": (6, 4), "C": (7, 4), "D": (0, 4),
        "E": (4, 1), "F": (4, 2), "G": (4, 3), "H": (6, 5),
        "I": (7, 5), "J": (0, 2), "K": (5, 0), "L": (5, 1),
        "M": (5, 2), "N": (5, 3), "O": (6, 7), "P": (6, 0),
        "Q": (6, 1), "R": (6, 2), "S": (6, 3), "T": (7, 0),
        "U": (7, 1), "V": (0, 3), "W": (1, 2), "X": (3, 1),
        "Y": (7, 2), "Z": (3, 2),
    }.items()
}


def ray_end(gray: np.ndarray, direction: int) -> int:
    angle = math.radians(direction * 45)
    end = 14
    for radius in range(15, 170):
        x = round(CX + radius * math.sin(angle))
        y = round(CY - radius * math.cos(angle))
        if float(np.mean(gray[y - 2:y + 3, x - 2:x + 3])) <= 185:
            break
        end = radius
    return end


def main() -> None:
    capture = cv2.VideoCapture(str(VIDEO))
    symbols: list[tuple[int, int]] = []
    for frame_no in range(45, 506, 10):
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"cannot read frame {frame_no}")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ends = [ray_end(gray, direction) for direction in range(8)]
        long_dirs = [i for i, end in enumerate(ends) if end >= 145]
        short_dirs = [i for i, end in enumerate(ends) if 90 <= end < 145]
        if len(long_dirs) != 1 or len(short_dirs) != 1:
            raise RuntimeError(f"ambiguous hands at frame {frame_no}: {ends}")
        symbols.append((long_dirs[0], short_dirs[0]))

    decoded = []
    for long_dir, short_dir in symbols:
        transformed = frozenset((((-long_dir) % 8 + 1) % 8, ((-short_dir) % 8 + 1) % 8))
        decoded.append(SEMAPHORE[transformed])

    print(f"stable_symbols={len(symbols)}")
    print("semaphore_ciphertext=" + "".join(decoded))


if __name__ == "__main__":
    main()
