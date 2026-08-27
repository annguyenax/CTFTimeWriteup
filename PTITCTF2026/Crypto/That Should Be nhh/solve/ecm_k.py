#!/usr/bin/env python3
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
from primefac import pollardrho_brent, ecm, pollard_pm1

sys.stdout.reconfigure(line_buffering=True)
text = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\files\enc.sage").read_text()
n = e = None
for raw in text.splitlines():
    if not raw.strip().startswith("#"):
        continue
    line = raw.strip().lstrip("#").strip().replace(" ", "")
    if line.startswith("n="):
        n = int(line[2:])
    elif line.startswith("e="):
        e = int(line[2:])
ap = Fraction(e, n).limit_denominator(1 << 100)
v, u = int(ap.numerator), int(ap.denominator)
rho0 = (u // 2 - (e * u % v)) % v
tmax = u // v + 2
print("tmax", tmax, flush=True)


def trial(n0):
    sm = 1
    while n0 % 2 == 0:
        n0 //= 2
        sm *= 2
    p = 3
    while p * p <= 1 << 20 and p * p <= n0:
        while n0 % p == 0:
            n0 //= p
            sm *= p
        p += 2
    return sm, n0


def pull_small(n0, rounds=6):
    sm = 1
    for _ in range(rounds):
        if n0.bit_length() < 540:
            break
        f = None
        for meth in (pollardrho_brent, pollard_pm1, ecm):
            try:
                f = meth(n0)
            except Exception:
                f = None
            if f and 1 < f < n0:
                break
            f = None
        if not f:
            break
        if f.bit_length() > 40:
            # leftover large; stop
            break
        while n0 % f == 0:
            n0 //= f
            sm *= f
        print("    pulled", f.bit_length(), "bit, left", n0.bit_length(), flush=True)
    return sm, n0


best = 0
for t in range(tmax):
    rho = rho0 + t * v
    if rho >= u:
        break
    num = e * u - u // 2 + rho
    if num % v:
        continue
    K = num // v
    A, rest = trial(K)
    A2, rest = pull_small(rest)
    A *= A2
    if A.bit_length() >= best:
        best = A.bit_length()
        print("t", t, "A", A.bit_length(), "rest", rest.bit_length(), flush=True)
    if 500 <= A.bit_length() <= 530:
        print("FOUND t", t)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(A))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(rest))
        break
print("best", best)
