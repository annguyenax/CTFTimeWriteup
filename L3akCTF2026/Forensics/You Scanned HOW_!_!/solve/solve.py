#!/usr/bin/env python3
"""Build and deskew a longitudinal radiograph from the multi-slice scan."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import subprocess
import tempfile
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path

import numpy as np
from PIL import Image


TABLE_PATTERN = re.compile(r"slice_(\d+)cm$")
DEFAULT_SCRATCH = Path(r"D:\download\ctf-scratch\l3akctf_you_scanned_how")


@contextmanager
def database_from_input(source: Path, scratch: Path) -> Iterator[Path]:
    if source.suffix.lower() in {".sqlite", ".db"}:
        yield source
        return

    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="solver-", dir=scratch) as temporary:
        destination = Path(temporary)
        subprocess.run(
            ["tar", "-xf", str(source.resolve()), "-C", str(destination)],
            check=True,
        )
        matches = list(destination.rglob("*.sqlite"))
        if len(matches) != 1:
            raise ValueError(f"expected one SQLite database, found {len(matches)}")
        yield matches[0]


def ordered_slice_tables(connection: sqlite3.Connection) -> list[tuple[int, str]]:
    tables: list[tuple[int, str]] = []
    for row in connection.execute("PRAGMA table_list"):
        match = TABLE_PATTERN.fullmatch(row[1])
        if match:
            tables.append((int(match.group(1)), row[1]))
    tables.sort()
    if len(tables) < 2:
        raise ValueError("not enough slice tables")
    steps = {b[0] - a[0] for a, b in zip(tables, tables[1:], strict=False)}
    if len(steps) != 1 or next(iter(steps)) <= 0:
        raise ValueError(f"slice spacing is not uniform: {sorted(steps)}")
    return tables


def projection_row(
    connection: sqlite3.Connection, table: str, angle: int
) -> tuple[int, np.ndarray]:
    # Table names are accepted only after the strict TABLE_PATTERN check above.
    row = connection.execute(
        f'SELECT detector_count, light_values FROM "{table}" '
        "WHERE angle_degrees = ?",
        (angle,),
    ).fetchone()
    if row is None:
        raise ValueError(f"missing angle {angle} in {table}")
    vector = np.asarray(json.loads(row[1]), dtype=np.float32)
    if len(vector) != row[0]:
        raise ValueError(f"detector_count mismatch in {table} at angle {angle}")
    return int(row[0]), vector


def build_radiograph(database: Path) -> tuple[Image.Image, int, int, float]:
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    try:
        tables = ordered_slice_tables(connection)
        z_spacing = tables[1][0] - tables[0][0]

        # The expanded 800x400 slice reaches its maximum detector width near a
        # diagonal view. Get that common canvas width without decoding all JSON.
        detector_axis = max(
            row[0]
            for row in connection.execute(
                f'SELECT detector_count FROM "{tables[0][1]}"'
            )
        )

        rows: list[np.ndarray] = []
        for _, table in tables:
            detector_count, means = projection_row(connection, table, 0)
            orthogonal_count, _ = projection_row(connection, table, 90)
            line_integral = means * orthogonal_count
            output_row = np.zeros(detector_axis, dtype=np.float32)
            start = (detector_axis - detector_count) // 2
            output_row[start : start + detector_count] = line_integral
            rows.append(output_row)
    finally:
        connection.close()

    radiograph = np.stack(rows)
    low, high = np.percentile(radiograph, (1.0, 99.7))
    normalized = np.uint8(np.clip((radiograph - low) / (high - low), 0, 1) * 255)
    image = Image.fromarray(np.flipud(normalized), mode="L")

    # The table suffix records a 3 cm slice spacing. Displaying each slice as one
    # pixel compresses z by 3, so restore physical aspect before deskewing.
    image = image.resize(
        (image.width, image.height * z_spacing), resample=Image.Resampling.BICUBIC
    )

    pixels = np.asarray(image)
    yy, xx = np.indices(pixels.shape)
    mask = (pixels > 220) & (xx > image.width * 0.15) & (xx < image.width * 0.85)
    y, x = np.nonzero(mask)
    if len(x) < 100:
        raise ValueError("not enough foreground pixels for PCA deskew")
    centered = np.column_stack((x - x.mean(), y - y.mean()))
    eigenvalues, eigenvectors = np.linalg.eigh(centered.T @ centered)
    axis = eigenvectors[:, eigenvalues.argmax()]
    if axis[1] < 0:
        axis = -axis
    angle = float(np.degrees(np.arctan2(axis[1], axis[0])))

    image = image.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    image = image.rotate(180, expand=False)
    return image, len(tables), z_spacing, angle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="path to scan2.7z or scan2.sqlite")
    parser.add_argument("output", type=Path, help="path for the calibrated PNG")
    parser.add_argument("--scratch", type=Path, default=DEFAULT_SCRATCH)
    args = parser.parse_args()

    with database_from_input(args.source, args.scratch) as database:
        image, slice_count, spacing, angle = build_radiograph(database)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"slices: {slice_count}; z spacing: {spacing}; PCA angle: {angle:.6f}")
    print(f"sha256: {digest}")
    print(args.output)


if __name__ == "__main__":
    main()
