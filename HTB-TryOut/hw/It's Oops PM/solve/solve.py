#!/usr/bin/env python3
"""It's Oops PM — offline solver.

Derives, purely from the provided VHDL sources:
  * backdoor trigger  : D == 0xFFE9  ("1111111111101001")  -> B = '1'
  * leaked key        : K == 0x63E1  ("0110001111100001")  (muxed to Output when B='1')
  * broken encryption : E(i)=D(i)^K(i) for i in 1..15; E(0)=~K(0), E(6)=~K(6), E(13)=~K(13)
  * tpm behaviour     : Output = Key when backdoor fires, else Encrypted.

The flag itself is emitted by the *remote* satellite service (send the trigger over
the wire); it is NOT contained in the downloadable files. This script reproduces the
VHDL simulation so the derived values are verifiable offline.

Usage:
    python solve.py                 # simulate: print trigger, key, sample encryptions
    python solve.py --trigger HOST:PORT   # (optional) talk to live satellite service
"""
from __future__ import annotations

import argparse
import re
import socket
import sys
from pathlib import Path

PATTERN = 0xFFE9          # backdoor.vhdl: "1111111111101001"
KEY = 0x63E1              # key.vhdl:      "0110001111100001"
FLAG_RE = re.compile(r"HTB\{[^}]+\}")


def enc(d: int, k: int = KEY) -> int:
    """Simulate encryption.vhdl (last assignment in process wins).
    E(i) = D(i) ^ K(i) for i in 1..15; E(0),E(6),E(13) = NOT K(i)."""
    e = 0
    for i in range(1, 16):
        e |= ((((d >> i) ^ (k >> i)) & 1) << i)
    for i in (0, 6, 13):  # sequential override: last assignment in process wins
        bit = (~(k >> i)) & 1
        e = (e & ~(1 << i)) | (bit << i)
    return e


def tpm(d: int) -> int:
    """Simulate tpm.vhdl: Output = Key if backdoor fires (D==pattern) else Encrypted."""
    return KEY if d == PATTERN else enc(d)


def decrypt(e: int, k: int = KEY) -> int:
    """Invert encryption where possible: D(i)=E(i)^K(i) for i in 1..15.
    Bits 0, 6, 13 are unrecoverable (ciphertext independent of data there)."""
    d = 0
    for i in range(1, 16):
        d |= (((e >> i) ^ (k >> i)) & 1) << i
    return d


def sim() -> list[str]:
    lines = [
        "TPM simulation (offline, from VHDL sources)",
        f"backdoor trigger D == 0x{PATTERN:04X}  ({PATTERN:016b})",
        f"leaked key       K == 0x{KEY:04X}     ({KEY:016b})",
        f"encrypt(0xFFFF)  = 0x{enc(0xFFFF):04X}",
        f"encrypt(0x0000)  = 0x{enc(0x0000):04X}",
        f"tpm(trigger)     = 0x{tpm(PATTERN):04X}  (== KEY -> backdoor fired)",
        "NOTE: flag text is returned by the live satellite service; absent from files.",
    ]
    return lines


def talk(host: str, port: int, payload: str, timeout: float = 15.0) -> str:
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    banner = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            banner += chunk
            if b"\n" in chunk or len(banner) > 200:
                break
    except socket.timeout:
        pass
    s.sendall((payload + "\n").encode())
    rest = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            rest += chunk
    except socket.timeout:
        pass
    s.close()
    return (banner + rest).decode("utf-8", "replace")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="", help="host:port of the satellite service")
    args = p.parse_args()
    ev = Path(__file__).resolve().parent / "evidence"
    ev.mkdir(parents=True, exist_ok=True)
    out = "\n".join(sim())
    (ev / "02_tpm_sim.txt").write_text(out + "\n", encoding="utf-8")
    print(out)

    if args.target:
        host, port_s = args.target.rsplit(":", 1)
        text = talk(host, int(port_s), f"{PATTERN:016b}")
        (ev / "03_remote.txt").write_text(text[:1500], encoding="utf-8", errors="replace")
        m = FLAG_RE.search(text)
        if m:
            print(m.group(0))
            return 0
        print("no flag in remote response:")
        print(text[:400])
        return 1
    print("\nNo --target given; offline simulation only (flag needs the live satellite).")
    return 2


if __name__ == "__main__":
    sys.exit(main())
