#!/usr/bin/env python3
"""Brute ~256 K = (e*u - u//2 + rho0 + t*v)/v and test 32-bit-smooth half."""
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
    if not raw.strip().startswith("#"):
        continue
    line = raw.strip().lstrip("#").strip().replace(" ", "")
    if line.startswith("n="):
        n = int(line[2:])
    elif line.startswith("e="):
        e = int(line[2:])
    elif line.startswith("c="):
        c = int(line[2:])
ap = Fraction(e, n).limit_denominator(1 << 100)
v, u = int(ap.numerator), int(ap.denominator)
print("u", u.bit_length(), "v", v.bit_length(), "primes", gmpy2.is_prime(u), gmpy2.is_prime(v))

rho0 = (u // 2 - (e * u % v)) % v
tmax = u // v + 2
print("tmax", tmax, "rho0", rho0.bit_length())

# primes to 2^16
sieve = bytearray(b"\x01") * (1 << 16)
sieve[0:2] = b"\x00\x00"
primes = []
for i in range(2, 1 << 16):
    if sieve[i]:
        primes.append(i)
        step = i
        start = i * i
        if start < len(sieve):
            sieve[start::step] = b"\x00" * len(sieve[start::step])
print("nprimes", len(primes), flush=True)


def pollard_quick(n, it=8000):
    if n % 2 == 0:
        return 2
    x = y = 2
    d = 1
    c = 1
    for _ in range(it):
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
        if 1 < d < n:
            return d
        if d == n:
            return None
    return None


def smooth_bits(K):
    n0 = K
    bits = 0
    while n0 % 2 == 0:
        n0 //= 2
        bits += 1
    for p in primes:
        if p * p > n0:
            break
        while n0 % p == 0:
            n0 //= p
            bits += p.bit_length()  # not accurate; count factors properly
    # recount A properly
    return bits, n0


def strip(K):
    n0 = K
    sm = 1
    while n0 % 2 == 0:
        n0 //= 2
        sm *= 2
    for p in primes:
        if p * p > n0:
            break
        while n0 % p == 0:
            n0 //= p
            sm *= p
    # skip hopeless (true A leaves ~768 bits after 16-bit trial)
    if n0.bit_length() > 860:
        return sm, n0
    for _ in range(16):
        if n0.bit_length() <= 520:
            break
        if gmpy2.is_prime(n0):
            break
        f = pollard_quick(n0, it=40000)
        if not f or f.bit_length() > 36:
            break
        while n0 % f == 0:
            n0 //= f
            sm *= f
    return sm, n0


def decrypt(p):
    if n % p or p <= 1 or p == n:
        return None
    q = n // p
    phi = (p - 1) * (q - 1)
    d = int(gmpy2.invert(e, phi))
    m = int(gmpy2.powmod(c, d, n))
    hx = format(m, "x")
    if len(hx) % 2:
        hx = "0" + hx
    raw = bytes.fromhex(hx)
    iv, ct = raw[:16], raw[16:]
    pt = AES.new(sha256(str(p).encode()).digest(), AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
        pt = pt[:-pad]
    return pt


best = (0, None)
for t in range(tmax):
    rho = rho0 + t * v
    if rho >= u:
        break
    num = e * u - u // 2 + rho
    if num % v:
        continue
    K = num // v
    if K <= 0:
        continue
    A, rest = strip(K)
    if A.bit_length() > best[0]:
        best = (A.bit_length(), (t, A.bit_length(), rest.bit_length(), A, rest, K))
        print("t", t, "A", A.bit_length(), "rest", rest.bit_length(), flush=True)
    if 500 <= A.bit_length() <= 524 and 500 <= rest.bit_length() <= 524:
        print("CANDIDATE t", t, flush=True)
        print("A", A)
        print("Qr", rest)
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A.txt").write_text(str(A))
        Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\Qr.txt").write_text(str(rest))
        # try p = A + s via gcd(A, n) no; Coppersmith later
        g = gcd(A, n)
        print("gcd(A,n)", g)
        # brute s is 80 bit no; try p~A howgrave linear: gcd(A,n) 
        # Fermat-ish: N % (A+s)==0, s odd small around 0 is 80 bit
        break
else:
    print("best", best[0], "info", None if not best[1] else best[1][:3])
