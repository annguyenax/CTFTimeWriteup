#!/usr/bin/env python3
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
import gmpy2
from hashlib import sha256
from Crypto.Cipher import AES

sys.stdout.reconfigure(line_buffering=True)

text = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\files\enc.sage").read_text()
n = e = c = None
for raw in text.splitlines():
    line = raw.strip()
    if not line.startswith("#"):
        continue
    line = line.lstrip("#").strip().replace(" ", "")
    if line.startswith("n="): n = int(line[2:])
    elif line.startswith("e="): e = int(line[2:])
    elif line.startswith("c="): c = int(line[2:])

ap = Fraction(e, n).limit_denominator(1 << 100)
v, u = int(ap.numerator), int(ap.denominator)
print("v bits", v.bit_length(), "u bits", u.bit_length())

# invert e = (K*v + u//2)//u  => K ≈ (e*u - u//2)/v
num = e * u - (u // 2)
K, r = divmod(num, v)
print("K bits", K.bit_length(), "r", r, "rbits", r.bit_length())
cands = [K]
if r > v // 2:
    cands.append(K + 1)
cands.append(K - 1)
cands.append(K + 1)
print("trying", cands[:4])


def brent(n, maxit=200000):
    if n % 2 == 0:
        return 2
    if gmpy2.is_prime(n):
        return None
    y, c, m = 2, 1, 64
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for _ in range(r):
            y = (y * y + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r - k)):
                y = (y * y + c) % n
                q = q * abs(x - y) % n
            g = gcd(q, n)
            k += m
        r *= 2
        if r > maxit:
            return None
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
            if g == n:
                return None
    return int(g) if 1 < g < n else None


def factor_smooth(K):
    n0 = K
    sm = 1
    while n0 % 2 == 0:
        n0 //= 2
        sm *= 2
    p = 3
    while p * p <= 1 << 16 and p * p <= n0:
        while n0 % p == 0:
            n0 //= p
            sm *= p
        p += 2
    steps = 0
    while n0.bit_length() > 520 and steps < 25:
        steps += 1
        f = brent(n0)
        print("  factor", f, "left", n0.bit_length(), flush=True)
        if not f:
            break
        if f.bit_length() > 34:
            print("  too big", f.bit_length())
            break
        while n0 % f == 0:
            n0 //= f
            sm *= f
    return sm, n0


for K in dict.fromkeys(cands):
    print("=== K", K.bit_length(), "w bits", (e * u - K * v).bit_length(), flush=True)
    A, rest = factor_smooth(K)
    print("A", A.bit_length(), "rest", rest.bit_length(), "prime rest", bool(gmpy2.is_prime(rest)), flush=True)
    if 500 <= A.bit_length() <= 520:
        print("FOUND A", A)
        print("Qr", rest)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(A))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(rest))
        break
else:
    print("failed canonical K")
