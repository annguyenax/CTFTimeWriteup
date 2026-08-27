#!/usr/bin/env python3
"""Pollard p-1 to pull 32-bit factors from each K candidate."""
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
import gmpy2

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

# primes to 100000 for p-1 B1
B1 = 100000
sieve = bytearray(b"\x01") * (B1 + 1)
sieve[0:2] = b"\x00\x00"
pr = []
for i in range(2, B1 + 1):
    if sieve[i]:
        pr.append(i)
        if i * i <= B1:
            sieve[i * i :: i] = b"\x00" * len(sieve[i * i :: i])
print("primes", len(pr), "tmax", tmax, flush=True)


def pm1(n, primes):
    if n % 2 == 0:
        return 2
    a = 2
    for p in primes:
        pp = p
        # p^k <= B1
        while pp * p <= primes[-1]:
            pp *= p
        a = pow(a, pp, n)
    g = gcd(a - 1, n)
    if 1 < g < n:
        return g
    return None


def strip_pm1(K):
    n0 = K
    sm = 1
    while n0 % 2 == 0:
        n0 //= 2
        sm *= 2
    for p in pr[:6542]:  # 16-bit
        if p * p > n0:
            break
        while n0 % p == 0:
            n0 //= p
            sm *= p
    for _ in range(12):
        if n0.bit_length() <= 530:
            break
        f = pm1(n0, pr)
        if not f:
            break
        if f.bit_length() > 40:
            break
        while n0 % f == 0:
            n0 //= f
            sm *= f
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
    A, rest = strip_pm1(K)
    if A.bit_length() > best:
        best = A.bit_length()
        print("t", t, "A", A.bit_length(), "rest", rest.bit_length(), flush=True)
    if 500 <= A.bit_length() <= 530:
        print("FOUND", t)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(A))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(rest))
        print("A", A)
        print("rest", rest)
        break
print("done best", best)
