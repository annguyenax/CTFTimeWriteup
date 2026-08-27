#!/usr/bin/env python3
"""
rayray (Kali Team CTF 26) — predict hidden flag block

Program fills 100 blocks with decoy text, then:
  srand(time(NULL));
  secret = rand() % 100;
  fgets(flag into blocks[secret]);
asks for a block index and prints DATA: %s.

Solve: reimplement glibc srand/rand, seed ≈ now, query that index.

Local:
  python3 solve/solve.py

Remote:
  python3 solve/solve.py remote HOST PORT
"""
from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

from pwn import *

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    HERE.parent / "files" / "player" / "rayray",
    Path.cwd() / "rayray",
]
BIN = next(p for p in CANDIDATES if p.exists())
WORKDIR = BIN.parent

context.binary = ELF(str(BIN), checksec=False)
context.log_level = "info"


class GlibcRand:
    """glibc TYPE_3 srandom/random — backend of srand/rand."""

    def __init__(self) -> None:
        self.state = [0] * 31
        self.fptr = 0
        self.rptr = 0

    def srand(self, seed: int) -> None:
        seed &= 0xFFFFFFFF
        if seed == 0:
            seed = 1
        st = self.state
        st[0] = seed
        for i in range(1, 31):
            hi = st[i - 1] // 127773
            lo = st[i - 1] % 127773
            x = 16807 * lo - 2836 * hi
            if x < 0:
                x += 2147483647
            st[i] = x
        self.fptr = 3
        self.rptr = 0
        for _ in range(310):
            self.rand()

    def rand(self) -> int:
        st = self.state
        f, r = self.fptr, self.rptr
        st[f] = (st[f] + st[r]) & 0xFFFFFFFF
        val = (st[f] >> 1) & 0x7FFFFFFF
        self.fptr = 0 if f + 1 >= 31 else f + 1
        self.rptr = 0 if r + 1 >= 31 else r + 1
        return val


def block_index(seed: int) -> int:
    g = GlibcRand()
    g.srand(seed)
    return g.rand() % 100


def selftest() -> None:
    g = GlibcRand()
    g.srand(1)
    assert g.rand() == 1804289383


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
    selftest()
    t0 = int(time.time())
    io = start(argv)
    io.recvuntil(b"enter Block number:", timeout=5)
    t1 = int(time.time())

    # widen ±1s for clock skew (esp. remote)
    seeds = list(range(t0 - 1, t1 + 2))
    votes = Counter(block_index(s) for s in seeds)
    best = votes.most_common(1)[0][0]
    log.info(f"seeds {seeds[0]}..{seeds[-1]} votes={dict(votes)} -> {best}")

    io.sendline(str(best).encode())
    out = io.recvall(timeout=3)
    sys.stdout.buffer.write(out if out.endswith(b"\n") else out + b"\n")
    io.close()
    return 0 if b"KaliTeam{" in out or b"DATA:" in out else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
