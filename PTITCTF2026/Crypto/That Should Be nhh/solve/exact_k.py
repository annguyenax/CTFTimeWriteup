#!/usr/bin/env python3
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
import gmpy2

sys.stdout.reconfigure(line_buffering=True)
text = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\files\enc.sage").read_text()
n=e=c=None
for raw in text.splitlines():
    line=raw.strip()
    if not line.startswith('#'): continue
    line=line.lstrip('#').strip().replace(' ','')
    if line.startswith('n='): n=int(line[2:])
    elif line.startswith('e='): e=int(line[2:])
    elif line.startswith('c='): c=int(line[2:])
ap=Fraction(e,n).limit_denominator(1<<100)
v,u=int(ap.numerator),int(ap.denominator)
print('u,v primes', gmpy2.is_prime(u), gmpy2.is_prime(v))

# e = (K*v + u//2)//u
# K*v + u//2 = e*u + rho, 0<=rho<u
# rho ≡ u//2 - e*u (mod v)  wait K*v ≡ e*u - u//2 + rho, need ≡ 0 mod v so
# rho ≡ -e*u + u//2 (mod v)
rho = (u // 2 - (e * u % v)) % v
print('rho', rho, 'bits', rho.bit_length(), 'rho<u', rho < u)
num = e * u - u // 2 + rho
assert num % v == 0
K = num // v
print('K bits', K.bit_length(), 'K<n?', K < n, 'n-K bits', (n-K).bit_length() if n>K else 'K>=n', 'K-n bits', (K-n).bit_length() if K>=n else None)
w = e * u - K * v
print('w', w, 'w bits', abs(w).bit_length())

def brent(n, maxit=500000):
    if n % 2 == 0: return 2
    if gmpy2.is_prime(n): return None
    for c in range(1, 8):
        y, m = 2, 64
        g, r, q = 1, 1, 1
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
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
                it += m
            r *= 2
        if 1 < g < n:
            return int(g)
    return None

n0 = K
sm = 1
while n0 % 2 == 0:
    n0 //= 2; sm *= 2
print('after 2, left', n0.bit_length(), 'twos', sm.bit_length()-1)
p = 3
while p*p <= 1<<20 and p*p <= n0:
    while n0 % p == 0:
        n0 //= p; sm *= p
    p += 2
print('after trial 2^20, A bits', sm.bit_length(), 'left', n0.bit_length(), flush=True)
steps=0
while n0.bit_length() > 520 and steps < 40:
    steps += 1
    f = brent(n0)
    print('brent', f, 'fbits' if f else '', f.bit_length() if f else None, 'left', n0.bit_length(), flush=True)
    if not f: break
    if f.bit_length() > 36:
        print('big factor, maybe Qr split')
        # if f is ~512 keep as rest candidate
        break
    while n0 % f == 0:
        n0 //= f; sm *= f
print('FINAL A bits', sm.bit_length(), 'rest bits', n0.bit_length(), 'rest prime', bool(gmpy2.is_prime(n0)))
Path(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\K.txt').write_text(str(K))
Path(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\solve\A_partial.txt').write_text(str(sm)+'\n'+str(n0))
print('wrote K')
