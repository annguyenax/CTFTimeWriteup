#!/usr/bin/env python3
"""Invert GhostVM VM2 Feistel and unpack the 32-byte input."""
from __future__ import annotations

import re
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location(
    "g", Path(__file__).with_name("solve_ghostvm.py")
)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

MASK64 = 0xFFFFFFFFFFFFFFFF
SBOX = g.make_sbox()
KFIX = 0xA0761D6478BD642F
MUL1 = 0xD6E8FEB86659FD93
MUL2 = 0x9FB21C651E98DF25
SPLAT = 0x0101010101010101


def rol(x, n):
    n &= 63
    x &= MASK64
    return x if n == 0 else ((x << n) | (x >> (64 - n))) & MASK64


def G_half(primary, other, xor1, rot, addc):
    r = primary ^ xor1
    t = rol(other ^ KFIX, rot)
    r = (r + t) & MASK64
    r7 = r
    r ^= (SBOX[(r7 >> 0) & 0xFF] << 56)
    r ^= (SBOX[(r7 >> 16) & 0xFF] << 32)
    r ^= (SBOX[(r7 >> 40) & 0xFF] << 8)
    r8 = (SBOX[(other >> 24) & 0xFF] * SPLAT) & MASK64
    r = (r + r8) & MASK64
    r = (r * MUL1) & MASK64
    t = (r + other) & MASK64
    sh = ((r >> 58) & 0x1F) + 5
    t = rol(t, sh)
    r ^= t
    r = (r + addc) & MASK64
    r ^= (r >> 23)
    r = (r * MUL2) & MASK64
    r ^= (r >> 29)
    r = (r + rol(other, 17)) & MASK64
    r ^= (r >> 32)
    return r & MASK64


def G(r2, r3, c1, rot1, c2, c3, rot2, c4):
    r4 = G_half(r2, r3, c1, rot1, c2)
    r5 = G_half(r3, r2, c3, rot2, c4)
    return r4, r5


def parse_rounds(asm: str):
    lines = asm.splitlines()
    # skip packing until first "mov r4, r2" after the 4 ldi zeros packing
    rounds = []
    i = 0
    # find all round starts: `mov r4, r2` followed by `xori r4`
    while i < len(lines):
        if re.search(r"mov\s+r4, r2", lines[i]) and i + 1 < len(lines) and "xori" in lines[i + 1]:
            chunk = "\n".join(lines[i : i + 80])
            xors = re.findall(r"xori\s+r4, 0x([0-9a-f]+)", chunk)
            # first xori r4 is c1; later addi r4 is c2
            c1 = int(xors[0], 16)
            addis = re.findall(r"addi\s+r4, 0x([0-9a-f]+)", chunk)
            c2 = int(addis[0], 16)
            rols = [int(x) for x in re.findall(r"roli\s+r6, (\d+)", chunk)]
            # [rot1, 17, rot2, 17]
            rot1 = rols[0]
            rot2 = rols[2] if len(rols) >= 3 else rols[0]
            xor5 = re.findall(r"xori\s+r5, 0x([0-9a-f]+)", chunk)
            c3 = int(xor5[0], 16)
            addi5 = re.findall(r"addi\s+r5, 0x([0-9a-f]+)", chunk)
            c4 = int(addi5[0], 16)
            rounds.append((c1, rot1, c2, c3, rot2, c4))
            i += 50
            continue
        i += 1
    return rounds


def invert_feistel(final, rounds):
    r0, r1, r2, r3 = final
    for c1, rot1, c2, c3, rot2, c4 in reversed(rounds):
        # (A',B') = (B, A xor F(B)) with A=(r0,r1), B=(r2,r3)
        # After round: r0,r1 = old r2,r3 = B
        # r2,r3 = old A xor F(B)
        B0, B1 = r0, r1
        Ap0, Ap1 = r2, r3
        f0, f1 = G(B0, B1, c1, rot1, c2, c3, rot2, c4)
        A0 = Ap0 ^ f0
        A1 = Ap1 ^ f1
        r0, r1, r2, r3 = A0, A1, B0, B1
    return r0, r1, r2, r3


# packing map: (reg, shift, in_index, xor)
PACK = [
    (0, 0, 19, 0x56),
    (0, 8, 2, 0xB6),
    (0, 16, 25, 0x38),
    (0, 24, 7, 0xC9),
    (0, 32, 14, 0x08),
    (0, 40, 30, 0xC4),
    (0, 48, 4, 0xA5),
    (0, 56, 22, 0x24),
    (1, 0, 1, 0xD2),
    (1, 8, 17, 0x79),
    (1, 16, 28, 0xFB),
    (1, 24, 11, 0x47),
    (1, 32, 5, 0x39),
    (1, 40, 24, 0x9E),
    (1, 48, 9, 0xD5),
    (1, 56, 31, 0x09),
    (2, 0, 13, 0xC3),
    (2, 8, 0, 0x63),
    (2, 16, 21, 0x2B),
    (2, 24, 6, 0xC7),
    (2, 32, 27, 0xA4),
    (2, 40, 16, 0x78),
    (2, 48, 3, 0x2E),
    (2, 56, 18, 0xC7),
    (3, 0, 29, 0x19),
    (3, 8, 10, 0xDD),
    (3, 16, 23, 0x14),
    (3, 24, 15, 0xD8),
    (3, 32, 8, 0x00),
    (3, 40, 26, 0x98),
    (3, 48, 12, 0x44),
    (3, 56, 20, 0xCE),
]


def unpack(words):
    inp = [0] * 32
    for reg, sh, idx, x in PACK:
        inp[idx] = ((words[reg] >> sh) & 0xFF) ^ x
    return bytes(inp)


def pack(inp: bytes):
    words = [0, 0, 0, 0]
    for reg, sh, idx, x in PACK:
        words[reg] |= ((inp[idx] ^ x) & 0xFF) << sh
    return words


def forward(words, rounds):
    r0, r1, r2, r3 = words
    for c1, rot1, c2, c3, rot2, c4 in rounds:
        f0, f1 = G(r2, r3, c1, rot1, c2, c3, rot2, c4)
        r0, r1, r2, r3 = r2, r3, r0 ^ f0, r1 ^ f1
    return r0, r1, r2, r3


def main():
    asm = Path(__file__).with_name("vm2.asm").read_text(encoding="utf-8")
    rounds = parse_rounds(asm)
    print("rounds", len(rounds))
    for i, r in enumerate(rounds):
        print(i, [hex(x) if isinstance(x, int) and x > 64 else x for x in r])

    final = (
        0xFFE472913819FB83,
        0xFF12A1C6DFF42510,
        0xABA41A37D8F557EA,
        0xDF68174149473FC4,
    )
    rec = invert_feistel(final, rounds)
    print("recovered words", [hex(x) for x in rec])
    chk = forward(rec, rounds)
    print("forward check", [hex(x) for x in chk])
    print("match", chk == final)
    inp = unpack(rec)
    print("input", inp, inp.decode("latin1", errors="replace"))
    print("ascii", "".join(chr(b) if 32 <= b < 127 else "." for b in inp))


if __name__ == "__main__":
    main()
