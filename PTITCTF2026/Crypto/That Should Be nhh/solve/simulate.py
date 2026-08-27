#!/usr/bin/env python3
"""Simulate the sage generator at toy size to validate CF → K recovery."""
import random
from fractions import Fraction
from math import gcd
import gmpy2

random.seed(0)

def isprime(n):
    return bool(gmpy2.is_prime(n))

def rnd_prime(bits):
    while True:
        x = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if isprime(x):
            return x

NBIT, PBIT, SBIT, DBIT, FBIT = 128, 64, 16, 24, 8  # scaled down

def smooth(bits):
    x = 1
    while x.bit_length() < bits - FBIT:
        x *= rnd_prime(FBIT)
    shift = bits - x.bit_length()
    if shift > 0:
        x <<= shift
    return x

def small(bits, odd=False):
    v = random.randrange(-(1 << (bits - 1)), 1 << (bits - 1))
    return 2 * v + (1 if odd else 0)

def gen():
    while True:
        A = smooth(PBIT)
        for _ in range(5000):
            s = small(SBIT, True)
            p = A + s
            if p.bit_length() == PBIT and isprime(p):
                break
        else:
            continue
        q = rnd_prime(PBIT)
        r = small(SBIT)
        if p == q or q <= abs(r):
            continue
        N = p * q
        K = A * (q - r)
        u = rnd_prime(DBIT)
        v = rnd_prime(DBIT - 8)
        e = (K * v + u // 2) // u
        w = e * u - K * v
        if 1 < e < N and abs(w) < (1 << DBIT) and gcd(e, (p - 1) * (q - 1)) == 1:
            return p, q, A, s, r, N, K, e, u, v, w

p, q, A, s, r, N, K, e, u, v, w = gen()
print("p bits", p.bit_length(), "A bits", A.bit_length(), "s", s)
print("true u bits", u.bit_length(), "v", v.bit_length())
print("true K bits", K.bit_length(), "K<N", K < N, "abs(K-N) bits", abs(K-N).bit_length())
print("e/N", e / N, "v/u", v / u)

ap = Fraction(e, N).limit_denominator(1 << (DBIT + 4))
print("CF v/u", ap.numerator, ap.denominator, "match", ap.numerator == v and ap.denominator == u)

# recover K
uu, vv = int(ap.denominator), int(ap.numerator)
rho = (uu // 2 - (e * uu % vv)) % vv
num = e * uu - uu // 2 + rho
print("divisible", num % vv == 0)
Krec = num // vv
print("Krec==K", Krec == K, "Krec bits", Krec.bit_length())
print("w rec", e * uu - Krec * vv, "true w", w)
rho0 = (uu // 2 - (e * uu % vv)) % vv
print("search t")
for t in range(uu // vv + 3):
    rho = rho0 + t * vv
    if rho >= uu:
        break
    num = e * uu - uu // 2 + rho
    if num % vv == 0 and num // vv == K:
        print("FOUND t", t, "rho", rho)
        break
else:
    print("t not found; try minus formula")
    for t in range(uu // vv + 3):
        rho = rho0 + t * vv
        num2 = e * uu + rho - uu // 2
        if num2 % vv == 0:
            Kr = num2 // vv
            if Kr == K:
                print("FOUND alt t", t)
                break
    print("true K*v + u//2 - e*u =", K * v + u // 2 - e * u)
