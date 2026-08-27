#!/usr/bin/env python3
"""Reconstruct the scanned object from the challenge SQLite projections."""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import tempfile
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.transform import iradon


def load_projections(database: Path) -> tuple[np.ndarray, list[np.ndarray], dict[int, int]]:
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "SELECT angle_degrees, detector_count, light_values "
            "FROM projections ORDER BY angle_degrees"
        ).fetchall()
    finally:
        connection.close()

    if not rows:
        raise ValueError("the projections table is empty")

    angles = np.asarray([row[0] for row in rows], dtype=np.float64)
    values = [np.asarray(json.loads(row[2]), dtype=np.float64) for row in rows]
    declared = {int(row[0]): int(row[1]) for row in rows}
    if any(len(vector) != row[1] for vector, row in zip(values, rows, strict=True)):
        raise ValueError("detector_count does not match light_values")
    if set(declared) != set(range(180)):
        raise ValueError("expected one projection for each integer angle from 0 to 179")
    return angles, values, declared


def reconstruct(database: Path) -> np.ndarray:
    angles, means, widths = load_projections(database)
    canvas_size = max(widths.values())
    sinogram = np.zeros((canvas_size, len(angles)), dtype=np.float64)

    for column, (angle, vector) in enumerate(zip(angles.astype(int), means, strict=True)):
        # The database stores column means of an expanded, rotated image.  The
        # width of the view 90 degrees away is the current rotated canvas height.
        canvas_height = widths[(angle + 90) % 180]
        line_integral = vector * canvas_height
        start = (canvas_size - len(line_integral)) // 2
        sinogram[start : start + len(line_integral), column] = line_integral

    image = iradon(
        sinogram,
        theta=angles,
        output_size=canvas_size,
        filter_name="ramp",
        interpolation="linear",
        circle=False,
    )
    return image


@contextmanager
def database_from_input(source: Path) -> Iterator[Path]:
    if source.suffix.lower() in {".sqlite", ".db"}:
        yield source
        return

    with tempfile.TemporaryDirectory(prefix="you-scanned-what-") as temporary:
        destination = Path(temporary)
        subprocess.run(
            ["tar", "-xf", str(source.resolve()), "-C", str(destination)],
            check=True,
        )
        matches = list(destination.rglob("*.sqlite"))
        if len(matches) != 1:
            raise ValueError(f"expected one SQLite database, found {len(matches)}")
        yield matches[0]


def save_contrast_image(array: np.ndarray, output: Path) -> None:
    low, high = np.percentile(array, (1.0, 99.5))
    scaled = np.clip((array - low) / (high - low), 0.0, 1.0)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Image coordinates and Radon coordinates use opposite vertical directions.
    Image.fromarray(np.flipud(np.uint8(scaled * 255)), mode="L").save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="path to scan.7z or extracted scan.sqlite")
    parser.add_argument("output", type=Path, help="path for the reconstructed PNG")
    args = parser.parse_args()
    with database_from_input(args.source) as database:
        save_contrast_image(reconstruct(database), args.output)
    print(args.output)


if __name__ == "__main__":
    main()
