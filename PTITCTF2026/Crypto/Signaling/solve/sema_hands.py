#!/usr/bin/env python3
import json
from pathlib import Path

pairs = []
for st, n, key in json.loads(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out\hands.json").read_text())["stable"]:
    a, b = key
    if a == b:
        pairs.append(None)  # rest/space
    else:
        pairs.append(frozenset(key))

base = {}
base[frozenset([4, 5])] = "A"
base[frozenset([4, 6])] = "B"
base[frozenset([4, 7])] = "C"
base[frozenset([0, 4])] = "D"
base[frozenset([1, 4])] = "E"
base[frozenset([2, 4])] = "F"
base[frozenset([3, 4])] = "G"
base[frozenset([5, 6])] = "H"
base[frozenset([5, 7])] = "I"
base[frozenset([0, 2])] = "J"
base[frozenset([0, 6])] = "K"
base[frozenset([1, 5])] = "L"
base[frozenset([2, 5])] = "M"
base[frozenset([3, 5])] = "N"
base[frozenset([6, 7])] = "O"
base[frozenset([1, 6])] = "P"
base[frozenset([2, 6])] = "Q"
base[frozenset([3, 6])] = "R"  # wait R is {2,6} both horizontal. Q vs R:
# Scout: Q is 9+1:30 {1,6}=P conflict. Let me set:
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
# P is 9+12 {0,6} but that's K. Wikipedia: P = W+N {6,0}=K.
# Alternative P={0,5}
base[frozenset([0, 5])] = "P"
# K stays {0,6}

def apply(fs, rot, mir):
    if fs is None:
        return None
    out = []
    for x in fs:
        if mir:
            x = (-x) % 8
        out.append((x + rot) % 8)
    return frozenset(out)

def dec(rot, mir):
    chars = []
    for s in pairs:
        if s is None:
            chars.append(" ")
            continue
        chars.append(base.get(apply(s, rot, mir), "?"))
    return "".join(chars)

print("n", len(pairs), "seq", [None if p is None else tuple(sorted(p)) for p in pairs])
for rot in range(8):
    for mir in (False, True):
        msg = dec(rot, mir)
        mark = ""
        if "PTIT" in msg or "FLAG" in msg or "CTF" in msg:
            mark = " ****"
        print(f"rot={rot} mir={int(mir)} {msg}{mark}")
