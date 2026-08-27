#!/usr/bin/env python3
import sys
from pathlib import Path
import gmpy2
from hashlib import sha256
from Crypto.Cipher import AES

sys.stdout.reconfigure(line_buffering=True)
mpz, gcd = gmpy2.mpz, gmpy2.gcd
A = mpz(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").read_text())
n0 = mpz(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").read_text())
print("A", A.bit_length(), "rest", n0.bit_length(), "prime", bool(gmpy2.is_prime(n0)), flush=True)


def brent(n, c, maxit=600000):
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


for c0 in list(range(16, 80)) + [97, 101, 131, 163, 193, 211, 241, 271, 307]:
    if gmpy2.is_prime(n0) or n0.bit_length() < 500:
        break
    print("c", c0, "rest", n0.bit_length(), flush=True)
    f = brent(n0, c0)
    if not f:
        continue
    print("  factor bits", f.bit_length(), flush=True)
    if f.bit_length() > 40:
        continue
    while n0 % f == 0:
        n0 //= f
        A *= f
    print("  A", A.bit_length(), "rest", n0.bit_length(), "prime", bool(gmpy2.is_prime(n0)), flush=True)

print("FINAL A", A.bit_length(), "rest", n0.bit_length(), "prime", bool(gmpy2.is_prime(n0)))
Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(int(A)))
Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(int(n0)))
