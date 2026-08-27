#!/usr/bin/env python3
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

text = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\files\enc.sage").read_text()
n = e = c = None
for raw in text.splitlines():
    line = raw.strip()
    if not line.startswith("#"):
        continue
    line = line.lstrip("#").strip().replace(" ", "")
    if line.startswith("n="):
        n = int(line[2:])
    elif line.startswith("e="):
        e = int(line[2:])
    elif line.startswith("c="):
        c = int(line[2:])
print("nbits", n.bit_length(), "ebits", e.bit_length(), "e/n", float(e) / float(n))

def convs(num, den):
    a, b = num, den
    n0, n1, d0, d1 = 0, 1, 1, 0
    out = []
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        n0, n1 = n1, q * n1 + n0
        d0, d1 = d1, q * d1 + d0
        out.append((n1, d1))
    return out

hits = []
for v, u in convs(e, n):
    if u <= 0 or v <= 0:
        continue
    if 70 <= u.bit_length() <= 110 and 70 <= v.bit_length() <= 110:
        hits.append((v, u, abs(e * u - n * v)))
print("convergents in range", len(hits))
for v, u, w in hits[:20]:
    print(" v", v.bit_length(), "u", u.bit_length(), " |eu-nv| bits", w.bit_length() if w else 0, "gcd", gcd(v, u))

ap = Fraction(e, n).limit_denominator(1 << 100)
print("limit", ap.numerator.bit_length(), ap.denominator.bit_length(), float(ap))
