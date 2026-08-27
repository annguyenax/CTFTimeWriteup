#!/usr/bin/env python3
"""Correct semaphore table (facing the signaler, 0=12 clockwise)."""
import json
from pathlib import Path

# Scout chart + Wikipedia, viewer-facing, 0=up CW
SEMA = {
    frozenset([4, 5]): "A",
    frozenset([4, 6]): "B",
    frozenset([4, 7]): "C",
    frozenset([0, 4]): "D",
    frozenset([1, 4]): "E",
    frozenset([2, 4]): "F",
    frozenset([3, 4]): "G",
    frozenset([5, 6]): "H",
    frozenset([5, 7]): "I",
    frozenset([0, 2]): "J",
    frozenset([0, 6]): "K",
    frozenset([1, 5]): "L",
    frozenset([2, 5]): "M",
    frozenset([3, 5]): "N",
    frozenset([6, 7]): "O",
    frozenset([0, 5]): "P",  # try; Wikipedia P is W+N? actually P is 9+12 = K. we'll rotate
    frozenset([1, 6]): "P",
    frozenset([2, 6]): "R",
    frozenset([3, 6]): "S",
    frozenset([0, 7]): "T",
    frozenset([1, 7]): "U",
    frozenset([0, 3]): "V",
    frozenset([1, 2]): "W",
    frozenset([2, 3]): "X",
    frozenset([2, 7]): "Y",
    frozenset([3, 7]): "Z",
    frozenset([1, 3]): "Q",
}

# fix P/K conflict: K={0,6} P={1,6} Q={2,6} wait Q isn't R. R={2,6} so Q={2,6} conflict.
# Wikipedia Q is 9+1:30 = {1,6} if P is something else.
# P: 9+12 {0,6} K also {0,6}. Wikipedia K is 12+9, P is 12+9? 
# P: left 9, up 12. K: 7:30+10:30. Different.
# I'll keep K={0,6}, P={1,6} overwritten - use two dicts.

data = json.loads(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out\clock_fast.json").read_text())
seq = []
for st, n, p, lit in data["stable"]:
    if len(lit) == 2:
        seq.append(frozenset(lit))

def apply(fs, rot, mir):
    out = []
    for x in fs:
        if mir:
            x = (-x) % 8
        out.append((x + rot) % 8)
    return frozenset(out)

# Build complete rotary-based table without conflicts
# Circle1 left-down + other:
base = {}
# down=4 plus k
for let, d in zip("ABCDEFG", [5, 6, 7, 0, 1, 2, 3]):
    base[frozenset([4, d])] = let
# Circle2 SW=5 plus
for let, d in zip("HIJKLMN", [6, 7, 0, 1, 2, 3, 4]):
    # skip d==4 already G; Wikipedia N is 5+3
    if d != 4:
        base[frozenset([5, d])] = let
# The zip is wrong. Manual remaining from scout:
base[frozenset([5, 6])] = "H"
base[frozenset([5, 7])] = "I"
base[frozenset([0, 2])] = "J"
base[frozenset([5, 0])] = "K"  # if K is 7:30+12? try 0,5
base[frozenset([1, 5])] = "L"
base[frozenset([2, 5])] = "M"
base[frozenset([3, 5])] = "N"
base[frozenset([6, 7])] = "O"
base[frozenset([0, 6])] = "P"
base[frozenset([1, 6])] = "Q"
base[frozenset([2, 6])] = "R"
base[frozenset([3, 6])] = "S"
base[frozenset([0, 7])] = "T"
base[frozenset([1, 7])] = "U"
base[frozenset([0, 3])] = "V"
base[frozenset([1, 2])] = "W"
base[frozenset([2, 3])] = "X"
base[frozenset([2, 7])] = "Y"
base[frozenset([3, 7])] = "Z"

print("table size", len(base), sorted(base.values()))

def dec(seq, rot=0, mir=False):
    chars = []
    for s in seq:
        t = apply(s, rot, mir)
        chars.append(base.get(t, "?"))
    return "".join(chars)

print("seq", [tuple(sorted(s)) for s in seq])
print()
for rot in range(8):
    for mir in (False, True):
        msg = dec(seq, rot, mir)
        flag = " <---" if "PTIT" in msg or "FLAG" in msg else ""
        print(f"rot={rot} mir={int(mir)} {msg}{flag}")
