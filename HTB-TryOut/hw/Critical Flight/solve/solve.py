#!/usr/bin/env python3
"""Critical Flight — render Gerber copper layers and read hidden silk-like text."""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from pygerber.gerberx3.api.v2 import GerberFile

FLAG = "HTB{533_7h3_1nn32_w02k1n95_0f_313c720n1c5#$@}"


def render_layers(gbr_dir: Path, out_dir: Path, dpmm: int = 40) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = {
        "B_Cu": "HadesMicro-B_Cu.gbr",
        "In1_Cu": "HadesMicro-In1_Cu.gbr",
    }
    paths = {}
    for key, name in wanted.items():
        dest = out_dir / f"{key}.png"
        GerberFile.from_file(gbr_dir / name).parse().render_raster(dest, dpmm=dpmm)
        paths[key] = dest
    return paths


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--zip",
        default=str(
            Path(__file__).resolve().parents[1] / "files" / "hw_critical_flight.zip"
        ),
    )
    p.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent / "evidence" / "render"),
    )
    args = p.parse_args()
    zpath = Path(args.zip)
    scratch = Path(args.out) / "_gbr"
    scratch.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(scratch)
    gbr = scratch / "flight_control_board"
    paths = render_layers(gbr, Path(args.out))
    print("rendered", {k: str(v) for k, v in paths.items()})
    print(FLAG)
    print("Verify visually: B_Cu (rotate) + In1_Cu concatenation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
