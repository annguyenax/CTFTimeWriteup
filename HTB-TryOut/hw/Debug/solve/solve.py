#!/usr/bin/env python3
"""Debug — decode the Saleae Logic capture (.sal) as UART 8N1 @ 115200 baud.

The challenge ships hw_debug.sal (a Saleae Logic 2 capture of a satellite
dish's serial boot output). meta.json reports two digital channels:
  - TX (channel 0)
  - RX (channel 1)
at 25 MS/s. The serial signal is UART 8N1 @ 115200 baud on the RX channel.
Decoding it yields a boot log in which the flag is embedded.

IMPORTANT: The internal .sal digital files use Saleae's undocumented
"render mipmap" (type=100) encoding. The intended workflow is to open the
.sal in Saleae Logic 2, add an Async Serial analyzer on RX with
Baud=115200, Bits=8, Parity=None, Stop=1, then read the decoded terminal.
This script automates the equivalent decode given a raw digital-1.bin
export (Logic 2 "Export -> digital data -> binary"). A helper parses a
Logic 2 binary digital export (type 0) and performs the 115200-baud
sampling.

FLAG (verified): HTB{547311173_n37w02k_c0mp20m153d}
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import zipfile
from pathlib import Path

FLAG_RE = re.compile(r"HTB\{[^}]+\}")
BAUD = 115200
RATE = 25_000_000


def parse_digital_export(data: bytes):
    """Parse a Saleae Logic 2 digital binary export (type 0)."""
    assert data[:8] == b"<SALEAE>", "not a Saleae export"
    ver, typ = struct.unpack_from("<ii", data, 8)
    off = 16
    if ver >= 1:
        nchunks = struct.unpack_from("<Q", data, off)[0]
        off += 8
    else:
        nchunks = 1
    if typ != 0:
        raise SystemExit("need digital export (type 0); .sal internal is type 100")
    chunks = []
    for _ in range(nchunks):
        initial = struct.unpack_from("<I", data, off)[0]
        off += 4
        if ver >= 1:
            rate = struct.unpack_from("<d", data, off)[0]
            off += 8
        begin, end, n = struct.unpack_from("<ddQ", data, off)
        off += 24
        times = list(struct.unpack_from("<%dd" % n, data, off))
        off += 8 * n
        chunks.append((initial, rate, begin, end, times))
    return chunks


def edges_to_samples(initial: int, times: list[float], rate: float):
    """Rebuild a per-sample high/low array (1/0) at `rate` Hz from edge times."""
    if not times:
        return []
    spb = rate / BAUD
    t0 = times[0]
    # state before first edge is `initial`; after first edge toggles
    pts = [(times[0], 1 - initial)]
    st = 1 - initial
    for te in times[1:]:
        st = 1 - st
        pts.append((te, st))
    end = times[-1]
    t = times[0]
    bit = 1.0 / BAUD
    out = []
    pi = 0
    while t < end:
        while pi + 1 < len(pts) and pts[pi + 1][0] <= t:
            pi += 1
        out.append(pts[pi][1])
        t += bit
    return out


def uart_decode(bits: list[int]) -> str:
    chars = []
    i = 0
    n = len(bits)
    while i < n - 10:
        if bits[i] != 0:  # wait for start bit (low)
            i += 1
            continue
        val = 0
        ok = True
        for b in range(8):
            if i + 1 + b >= n:
                ok = False
                break
            if bits[i + 1 + b]:
                val |= 1 << b
        if ok and i + 9 < n and bits[i + 9] == 1:
            chars.append(val)
        i += 10
    return bytes(chars).decode("latin1")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--sal", default=str(
        Path(__file__).resolve().parents[1] / "files" / "hw_debug.zip"))
    p.add_argument("--export", default=str(
        Path(__file__).resolve().parent / "evidence" / "digital_1.bin"),
        help="Logic 2 binary export of RX channel (type 0)")
    args = p.parse_args()

    ev = Path(__file__).resolve().parent / "evidence"
    ev.mkdir(parents=True, exist_ok=True)

    exp = Path(args.export)
    if not exp.exists():
        print(f"Provide a Logic 2 binary export of the RX channel at {exp}")
        return 2
    chunks = parse_digital_export(exp.read_bytes())
    log = ""
    for initial, rate, begin, end, times in chunks:
        bits = edges_to_samples(initial, times, rate or RATE)
        log += uart_decode(bits)
    (ev / "02_uart_log.txt").write_text(log[:4000], encoding="utf-8")
    m = FLAG_RE.search(log)
    flag = m.group(0) if m else None
    print("FLAG:", flag)
    print("first 300 chars:", log[:300].replace("\n", " | "))
    return 0 if flag else 1


if __name__ == "__main__":
    raise SystemExit(main())
