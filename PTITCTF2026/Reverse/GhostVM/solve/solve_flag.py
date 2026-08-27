#!/usr/bin/env python3
"""Invert GhostVM stage-2 Feistel and recover the 32-byte flag."""
import re
from pathlib import Path

import pefile

from emu import MASK64, make_perm, rol64, run_vm1

DISASM = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\GhostVM\solve\vm2_disasm.txt")
BIN = r"D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe"

KXOR = 0xA0761D6478BD642F
MUL1 = 0xD6E8FEB86659FD93
MUL2 = 0x9FB21C651E98DF25
SPREAD = 0x0101010101010101


def parse_disasm(text: str):
    lines = []
    for raw in text.splitlines():
        m = re.match(r"([0-9a-f]+): (.*)", raw)
        if m:
            lines.append((int(m.group(1), 16), m.group(2)))
    return lines


def parse_packing(lines):
    """Return list of (word, shift, flag_index, xor) and the 4-word packing."""
    specs = []
    cur_word = None
    pending = None  # (flag_idx, xor)
    shift = 0
    for _, s in lines:
        m = re.match(r"LOAD_INPUT r4, flag\[(\d+)\]", s)
        if m:
            pending = [int(m.group(1)), None]
            shift = 0
            continue
        m = re.match(r"XOR_IMM r4, (0x[0-9a-f]+)", s)
        if m and pending and pending[1] is None:
            pending[1] = int(m.group(1), 16)
            continue
        m = re.match(r"SHL_IMM r4, (\d+)", s)
        if m and pending:
            shift = int(m.group(1))
            continue
        m = re.match(r"OR r(\d), r4", s)
        if m and pending:
            word = int(m.group(1))
            specs.append((word, shift, pending[0], pending[1]))
            pending = None
            continue
        if s.startswith("MOV r4, r2"):
            break
    return specs


def parse_rounds(lines):
    rounds = []
    i = 0
    while i < len(lines):
        _, s = lines[i]
        if s == "MOV r4, r2":
            # start of F
            rec = {}
            # XOR_IMM r4
            i += 1
            rec["Ca"] = int(re.search(r"0x[0-9a-f]+", lines[i][1]).group(), 16)
            # MOV r6, r3; XOR_IMM r6; ROL_IMM r6
            i += 3
            rec["rota"] = int(re.search(r"ROL_IMM r6, (\d+)", lines[i][1]).group(1))
            # find ADD_IMM r4 after first MUL_IMM 9fb21... no, ADD_IMM r4 after XOR r4, r6
            # easier: scan forward
            while True:
                i += 1
                if lines[i][1].startswith("ADD_IMM r4,"):
                    rec["Cadda"] = int(re.search(r"0x[0-9a-f]+", lines[i][1]).group(), 16)
                    break
            while True:
                i += 1
                if lines[i][1] == "MOV r5, r3":
                    break
            i += 1
            rec["Cb"] = int(re.search(r"0x[0-9a-f]+", lines[i][1]).group(), 16)
            i += 3
            rec["rotb"] = int(re.search(r"ROL_IMM r6, (\d+)", lines[i][1]).group(1))
            while True:
                i += 1
                if lines[i][1].startswith("ADD_IMM r5,"):
                    rec["Caddb"] = int(re.search(r"0x[0-9a-f]+", lines[i][1]).group(), 16)
                    break
            rounds.append(rec)
        i += 1
    return rounds


def sbox_mix_half(x, other, sbox, xor_c, rot, add_c):
    """F half: x is the 'primary' (r2 for left, r3 for right), other is the other 64-bit."""
    r = (x ^ xor_c) & MASK64
    r6 = rol64((other ^ KXOR) & MASK64, rot)
    r = (r + r6) & MASK64
    r7 = r
    r ^= (sbox[(r7 >> 0) & 0xFF] << 56) & MASK64
    r ^= (sbox[(r7 >> 16) & 0xFF] << 32) & MASK64
    r ^= (sbox[(r7 >> 40) & 0xFF] << 8) & MASK64
    r8 = (sbox[(other >> 24) & 0xFF] * SPREAD) & MASK64
    r = (r + r8) & MASK64
    r = (r * MUL1) & MASK64
    r6 = (r + other) & MASK64
    r8 = ((r >> 58) & 0x1F) + 5
    r6 = rol64(r6, r8)
    r ^= r6
    r = (r + add_c) & MASK64
    r ^= r >> 23
    r = (r * MUL2) & MASK64
    r ^= r >> 29
    r = (r + rol64(other, 17)) & MASK64
    r ^= r >> 32
    return r & MASK64


def F(r2, r3, rnd, sbox):
    r4 = sbox_mix_half(r2, r3, sbox, rnd["Ca"], rnd["rota"], rnd["Cadda"])
    r5 = sbox_mix_half(r3, r2, sbox, rnd["Cb"], rnd["rotb"], rnd["Caddb"])
    return r4, r5


def feistel_forward(r0, r1, r2, r3, rounds, sbox):
    for rnd in rounds:
        r4, r5 = F(r2, r3, rnd, sbox)
        r10 = r0 ^ r4
        r11 = r1 ^ r5
        r0, r1, r2, r3 = r2, r3, r10, r11
    return r0, r1, r2, r3


def feistel_inverse(r0, r1, r2, r3, rounds, sbox):
    for rnd in reversed(rounds):
        L0, L1 = r0, r1
        r4, r5 = F(L0, L1, rnd, sbox)
        r0, r1, r2, r3 = r2 ^ r4, r3 ^ r5, L0, L1
    return r0, r1, r2, r3


def unpack(r, specs):
    words = list(r)
    flag = [None] * 32
    for word, shift, idx, xorv in specs:
        b = ((words[word] >> shift) & 0xFF) ^ xorv
        flag[idx] = b
    return bytes(flag)


def main():
    text = DISASM.read_text(encoding="utf-8")
    lines = parse_disasm(text)
    specs = parse_packing(lines)
    print("packing specs", len(specs))
    for t in specs:
        print(" ", t)
    missing = [i for i in range(32) if not any(s[2] == i for s in specs)]
    print("missing indices", missing)

    rounds = parse_rounds(lines)
    print("rounds", len(rounds))
    for i, r in enumerate(rounds):
        print(f"  {i:2d}", {k: hex(v) if v > 64 else v for k, v in r.items()})

    pe = pefile.PE(BIN)
    data = pe.get_memory_mapped_image()
    sbox = make_perm()
    print("sbox[:16]", sbox[:16].hex())

    ct = (
        0xFFE472913819FB83,
        0xFF12A1C6DFF42510,
        0xABA41A37D8F557EA,
        0xDF68174149473FC4,
    )
    pt = feistel_inverse(*ct, rounds, sbox)
    print("plaintext words", [hex(x) for x in pt])

    # sanity: forward
    back = feistel_forward(*pt, rounds, sbox)
    print("forward match", back == ct, [hex(x) for x in back])

    flag = unpack(pt, specs)
    print("flag bytes", flag)
    print("flag", flag.decode("latin1"))

    # known prefix check
    print("prefix", flag[:8])


if __name__ == "__main__":
    main()
