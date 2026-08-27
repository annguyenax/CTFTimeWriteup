#!/usr/bin/env python3
import sys
from pathlib import Path
import gmpy2

sys.stdout.reconfigure(line_buffering=True)
mpz, gcd = gmpy2.mpz, gmpy2.gcd
A = mpz(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").read_text())
R = mpz(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").read_text())
print("A", A.bit_length(), "R", R.bit_length())


def brent(n, c, maxit=400000):
    n, c = mpz(n), mpz(c)
    if n % 2 == 0:
        return mpz(2)
    y = mpz(2)
    m = 256
    g, r, q = mpz(1), 1, mpz(1)
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
    return g if 1 < g < n else None


def factor_smooth(n0):
    fac = []
    n0 = mpz(n0)
    while n0 % 2 == 0:
        fac.append(mpz(2))
        n0 //= 2
    p = mpz(3)
    while p * p <= 1 << 20 and p * p <= n0:
        while n0 % p == 0:
            fac.append(p)
            n0 //= p
        p += 2
    for c0 in range(1, 40):
        if n0 == 1 or gmpy2.is_prime(n0):
            break
        if n0.bit_length() > 40:
            f = brent(n0, c0)
            if f and f.bit_length() <= 36:
                while n0 % f == 0:
                    fac.append(f)
                    n0 //= f
                print("pulled", f.bit_length(), "left", n0.bit_length(), flush=True)
            elif f:
                print("big", f.bit_length(), flush=True)
    if n0 > 1:
        fac.append(n0)
    return fac


print("factor A (should be all 32-bit)", flush=True)
fa = factor_smooth(A)
prod = mpz(1)
for f in fa:
    prod *= f
print("A factors", [(int(f).bit_length(), int(f)) for f in fa], "prod bits", prod.bit_length(), "match", prod == A)
print("factor R", flush=True)
fr = factor_smooth(R)
print("R factors bits", [int(f).bit_length() for f in fr])
print("R leftover prime?", bool(gmpy2.is_prime(fr[-1])) if fr else None, "bits", fr[-1].bit_length() if fr else None)
