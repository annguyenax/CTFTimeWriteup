#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

data = json.loads(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out\clock_fast.json").read_text())
stable = data["stable"]
# [start, n, pair, lit]
lits = []
for st, n, p, lit in stable:
    if len(lit) == 2:
        lits.append((frozenset(lit), st, n))
    elif len(lit) != 2:
        lits.append((("REST", tuple(lit)), st, n))

print("n 2-lit", sum(1 for x in lits if not (isinstance(x[0], tuple) and x[0][0]=="REST")))
seq = [x[0] for x in lits if not (isinstance(x[0], tuple))]
print("seq len", len(seq))
print(seq)
print("unique", len(set(map(frozenset, [tuple(sorted(s)) for s in seq]))))
print(Counter(tuple(sorted(s)) for s in seq))

pref = "PTITCTF"
# check if any offset matches T-repeat pattern
for off in range(0, min(10, len(seq))):
    s = seq[off:]
    if len(s) < 7:
        break
    # T at 1,3,5
    ok = s[1] == s[3] == s[5]
    distinct = len({s[0], s[2], s[4], s[6], s[1]}) == 5
    print(f"off {off} T-repeat {ok} 5 distinct {distinct} first7 {[tuple(sorted(x)) for x in s[:7]]}")

# Wikipedia semaphore (signaller facing us, 8 dirs clockwise from 12):
# I'll load a standard map. Dirs 0=N,1=NE,2=E,3=SE,4=S,5=SW,6=W,7=NW
# From https://en.wikipedia.org/wiki/Flag_semaphore  (approximate)
# Many sources number:
SEMA = {
    frozenset([4, 5]): "A",  # S + SW
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
    frozenset([0, 5]): "O",
    frozenset([1, 6]): "P",
    frozenset([2, 6]): "Q",
    frozenset([3, 6]): "R",
    frozenset([0, 6]): "K",  # dup
    frozenset([1, 7]): "S",
    frozenset([2, 7]): "T",
    frozenset([0, 3]): "U",
    frozenset([1, 2]): "V",
    frozenset([0, 1]): "W",
    frozenset([2, 3]): "X",
    frozenset([0, 7]): "Y",
    frozenset([1, 3]): "Z",
    frozenset([3, 7]): "J",  # sometimes J is 0,2
}

def dec(seq, rot=0, mirror=False):
    out = []
    for s in seq:
        a, b = sorted(s)
        if mirror:
            a, b = (-a) % 8, (-b) % 8
        a, b = (a + rot) % 8, (b + rot) % 8
        out.append(SEMA.get(frozenset([a, b]), "?"))
    return "".join(out)

print("\n=== semaphore rotations ===")
for rot in range(8):
    for mir in (False, True):
        msg = dec(seq, rot, mir)
        if "PTIT" in msg or msg.count("?") <= 8:
            print("rot", rot, "mir", mir, msg)
        elif rot == 0 and not mir:
            print("rot0", msg)
# print all
print("--- all ---")
for rot in range(8):
    print(rot, "N", dec(seq, rot, False))
    print(rot, "M", dec(seq, rot, True))
