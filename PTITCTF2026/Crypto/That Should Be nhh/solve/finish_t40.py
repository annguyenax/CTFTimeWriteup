#!/usr/bin/env python3
"""Fully factor 32-bit part of K at t=40 (best smoothness so far)."""
import sys
from fractions import Fraction
from pathlib import Path
import gmpy2
from hashlib import sha256
from Crypto.Cipher import AES

sys.stdout.reconfigure(line_buffering=True)
mpz, gcd = gmpy2.mpz, gmpy2.gcd

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
t = 40
rho = rho0 + t * v
K = (e * u - u // 2 + rho) // v
print("K bits", K.bit_length(), flush=True)


def brent(n, c, maxit=400000):
    n, c = mpz(n), mpz(c)
    if n % 2 == 0:
        return mpz(2)
    y = mpz(2)
    m = 256
    g = mpz(1)
    r = 1
    q = mpz(1)
    it = 0
    ys = y
    x = y
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


n0 = K
sm = mpz(1)
while n0 % 2 == 0:
    n0 //= 2
    sm *= 2
p = mpz(3)
while p * p <= 4096:
    while n0 % p == 0:
        n0 //= p
        sm *= p
    p += 2
print("start rest", n0.bit_length(), "A", sm.bit_length(), flush=True)

for c0 in list(range(1, 30)) + [41, 61, 97, 101, 131, 163, 193]:
    if n0.bit_length() <= 530:
        break
    print("c", c0, "rest", n0.bit_length(), flush=True)
    f = brent(n0, c0)
    if not f:
        continue
    print("  factor bits", f.bit_length(), flush=True)
    if f.bit_length() > 40:
        print("  large, skip")
        continue
    while n0 % f == 0:
        n0 //= f
        sm *= f
    print("  A", sm.bit_length(), "rest", n0.bit_length(), flush=True)

print("FINAL A", sm.bit_length(), "rest", n0.bit_length(), "prime rest", bool(gmpy2.is_prime(n0)))
Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(int(sm)))
Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(int(n0)))
print("saved")
