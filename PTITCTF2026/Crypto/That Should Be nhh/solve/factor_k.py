#!/usr/bin/env python3
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import gmpy2

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

ap = Fraction(e, n).limit_denominator(1 << 100)
v, u = ap.numerator, ap.denominator
print("v", v, "bits", v.bit_length())
print("u", u, "bits", u.bit_length())
eu = e * u
K0, rem = divmod(eu, u and v)
# K ~ e*u/v
K0, rem = divmod(eu, v)
print("K0 bits", K0.bit_length(), "rem", rem, "rem bits", rem.bit_length())
print("w if K=K0", rem.bit_length(), "w if K=K0+1", abs(eu - (K0 + 1) * v).bit_length())

# |w|<2^96 so |K - eu/v| < 2^96 / v ≈ 2^(96-88)=2^8
radius = (1 << 96) // v + 5
print("radius", radius)


def pollard(n, rounds=80_000):
    if n % 2 == 0:
        return 2
    if gmpy2.is_prime(n):
        return None
    for c0 in (1, 3, 5, 7):
        x = y = 2
        d = 1
        for _ in range(rounds):
            x = (x * x + c0) % n
            y = (y * y + c0) % n
            y = (y * y + c0) % n
            d = gcd(abs(x - y), n)
            if 1 < d < n:
                return d
            if d == n:
                break
    return None


def strip(n):
    sm = 1
    while n % 2 == 0:
        n //= 2
        sm *= 2
    p = 3
    while p * p <= 1 << 18 and p * p <= n:
        while n % p == 0:
            n //= p
            sm *= p
        p += 2
    g = 0
    while n.bit_length() > 520 and g < 30:
        g += 1
        f = pollard(n)
        print("  rho", f, "nbits", n.bit_length() if not f else f.bit_length(), flush=True)
        if not f:
            break
        if f.bit_length() > 40:
            print("  large factor, stop strip")
            break
        while n % f == 0:
            n //= f
            sm *= f
    return sm, n


# try K near K0
for dt in range(-int(radius), int(radius) + 1):
    K = K0 - dt
    w = eu - K * v
    if abs(w) >= (1 << 96):
        continue
    if K % v == 0:
        pass
    print("try dt", dt, "K bits", K.bit_length(), "w bits", abs(w).bit_length(), flush=True)
    A, rest = strip(K)
    print("  A bits", A.bit_length(), "rest bits", rest.bit_length(), "rest prime?", bool(gmpy2.is_prime(rest)), flush=True)
    if 500 <= A.bit_length() <= 520 and 500 <= rest.bit_length() <= 520:
        print("GOOD A", A)
        print("GOOD Qr", rest)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(A))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(rest))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\K.txt").write_text(str(K))
        break
else:
    print("no K in radius")
