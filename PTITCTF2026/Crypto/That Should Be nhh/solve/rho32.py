#!/usr/bin/env python3
"""Pollard-Brent tuned for 31–32-bit factors (A is product of those)."""
import sys
from fractions import Fraction
from pathlib import Path
import gmpy2

sys.stdout.reconfigure(line_buffering=True)
mpz = gmpy2.mpz
gcd = gmpy2.gcd

text = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\files\enc.sage").read_text()
n = e = c = None
for raw in text.splitlines():
    if not raw.strip().startswith("#"):
        continue
    line = raw.strip().lstrip("#").strip().replace(" ", "")
    if line.startswith("n="):
        n = mpz(line[2:])
    elif line.startswith("e="):
        e = mpz(line[2:])
    elif line.startswith("c="):
        c = mpz(line[2:])
ap = Fraction(int(e), int(n)).limit_denominator(1 << 100)
v, u = mpz(ap.numerator), mpz(ap.denominator)
rho0 = (u // 2 - (e * u % v)) % v
tmax = int(u // v) + 2
print("tmax", tmax, flush=True)


def brent32(n, maxit=250000):
    n = mpz(n)
    if n % 2 == 0:
        return mpz(2)
    y = mpz(2)
    c = mpz(1)
    m = 128
    g = mpz(1)
    r = 1
    q = mpz(1)
    it = 0
    while g == 1 and it < maxit:
        x = y
        for _ in range(r):
            y = (y * y + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r - k)):
                y = (y * y + c) % n
                q = (q * abs(x - y)) % n
            g = gcd(q, n)
            k += m
            it += m
        r *= 2
    if g == n:
        g = mpz(1)
        while g == 1:
            ys = (ys * ys + c) % n
            g = gcd(abs(x - ys), n)
        if g == n:
            return None
    if 1 < g < n:
        return g
    return None


def strip(K):
    n0 = mpz(K)
    sm = mpz(1)
    while n0 % 2 == 0:
        n0 //= 2
        sm *= 2
    p = mpz(3)
    lim = mpz(1) << 12  # tiny only
    while p * p <= lim and p * p <= n0:
        while n0 % p == 0:
            n0 //= p
            sm *= p
        p += 2
    for _ in range(20):
        if n0.bit_length() <= 530:
            break
        f = brent32(n0)
        if not f:
            break
        bl = f.bit_length()
        if bl > 36:
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
    A, rest = strip(K)
    ab, rb = A.bit_length(), rest.bit_length()
    if ab > best:
        best = ab
        print("t", t, "A", ab, "rest", rb, flush=True)
    if 500 <= ab <= 530:
        print("FOUND t", t, flush=True)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(int(A)))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(int(rest)))
        print("A", int(A))
        print("Qr", int(rest))
        break
print("done best", best, flush=True)
