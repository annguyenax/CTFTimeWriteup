#!/usr/bin/env python3
"""Recover the Bliss I flag from the saved Svelte route node and CSS."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NODE = ROOT / "evidence" / "route_node_22.js"
CSS = ROOT / "evidence" / "app.css"

CONDITIONS = [
    "screen and (aspect-ratio: 6/7)",
    "screen and (pointer: coarse)",
    "print and (orientation: landscape)",
    "(monochrome)",
    "screen and (-webkit-device-pixel-ratio: 3)",
]


def main() -> None:
    node = NODE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    chars = {
        int(square_id): char
        for square_id, char in re.findall(
            r'id="square-(\d+)">([^<])</h2>', node
        )
    }
    if len(chars) != 64:
        raise ValueError(f"expected 64 rune characters, found {len(chars)}")

    media_blocks = {
        condition: selector_text
        for condition, selector_text in re.findall(
            r"@media\s+([^{}]+)\{([^{}]+)"
            r"\{background:#d79e3a;color:#050108\}\}",
            css,
        )
    }

    segments: list[str] = []
    for condition in CONDITIONS:
        selectors = media_blocks.get(condition)
        if selectors is None:
            raise ValueError(f"missing media query: {condition}")
        ids = [int(value) for value in re.findall(r"square-(\d+)", selectors)]
        segment = "".join(chars[square_id] for square_id in ids)
        segments.append(segment)
        print(f"{condition}: {ids} -> {segment}")

    # runes.png draws literal hyphens between the four symbols inside braces.
    flag = segments[0] + "{" + "-".join(segments[1:]) + "}"
    print(flag)


if __name__ == "__main__":
    main()
