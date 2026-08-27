#!/usr/bin/env python3
"""Extract White's queen paths from the PGN and render the hidden glyphs."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


PHRASE = "HARD TO KEEP UP WITH THE QUEEN"  # Human-read from the rendered glyphs.
FLAG = "L3AK{" + PHRASE.replace(" ", "_") + "}"
SQUARE_RE = re.compile(r"([a-h][1-8])(?:=[QRBN])?[+#]?$")


def extract_paths(pgn: str) -> list[list[str]]:
    games = re.split(r"(?m)(?=^\[Event )", pgn)
    paths: list[list[str]] = []
    for game in games:
        if not game.strip():
            continue
        movetext = " ".join(
            line for line in game.splitlines() if not line.startswith("[")
        )
        queen_path: list[str] = []
        for match in re.finditer(r"\b\d+\.\s*(\S+)(?:\s+(\S+))?", movetext):
            white_san = match.group(1)
            if not white_san.startswith("Q"):
                continue
            square = SQUARE_RE.search(white_san)
            if not square:
                raise ValueError(f"Cannot parse queen destination from {white_san!r}")
            queen_path.append(square.group(1))
        paths.append(queen_path)
    return paths


def render_svg(paths: list[list[str]], output: Path) -> None:
    cols, cell, pad, board = 6, 170, 20, 128
    rows = (len(paths) + cols - 1) // cols
    width, height = cols * cell, rows * cell
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    for index, path in enumerate(paths):
        ox, oy = (index % cols) * cell + pad, (index // cols) * cell + pad
        step = board / 7
        for n in range(8):
            x = ox + n * step
            y = oy + n * step
            parts.append(f'<path d="M{x:.2f},{oy} V{oy + board}" stroke="#ddd"/>')
            parts.append(f'<path d="M{ox},{y:.2f} H{ox + board}" stroke="#ddd"/>')
        points = []
        for square in path:
            file_no = ord(square[0]) - ord("a")
            rank_no = int(square[1]) - 1
            points.append(f"{ox + file_no * step:.2f},{oy + (7 - rank_no) * step:.2f}")
        parts.append(
            f'<polyline points="{" ".join(points)}" fill="none" stroke="#111" '
            'stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        parts.append(
            f'<text x="{ox}" y="{oy - 6}" font-family="monospace" font-size="13">'
            f'Game {index + 1:02d}</text>'
        )
    parts.append("</svg>")
    output.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pgn", type=Path)
    parser.add_argument("--svg", type=Path, default=Path("queen_paths.svg"))
    parser.add_argument("--evidence", type=Path, default=Path("evidence.txt"))
    args = parser.parse_args()

    raw = args.pgn.read_bytes()
    paths = extract_paths(raw.decode("utf-8"))
    letters = PHRASE.replace(" ", "")
    if len(paths) != len(letters):
        raise SystemExit(f"Expected {len(letters)} games, got {len(paths)}")
    if any(len(path) < 2 for path in paths):
        raise SystemExit("At least one game has too few queen moves to draw a glyph")

    render_svg(paths, args.svg)
    lines = [
        f"games.pgn sha256: {hashlib.sha256(raw).hexdigest()}",
        f"game count: {len(paths)}",
        "",
    ]
    lines.extend(
        f"{i:02d} {letter}: {' '.join(path)}"
        for i, (letter, path) in enumerate(zip(letters, paths), 1)
    )
    lines.extend(["", f"decoded phrase: {PHRASE}", f"flag: {FLAG}"])
    args.evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rendered {len(paths)} glyphs to {args.svg}")
    print(f"Decoded phrase: {PHRASE}")
    print(f"Flag: {FLAG}")


if __name__ == "__main__":
    main()
