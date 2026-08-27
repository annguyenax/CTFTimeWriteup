#!/usr/bin/env python3
"""Howgrave-Graham small roots of f(x)=x+A (mod p | N), recover s then AES."""
import sys
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import gmpy2
from Crypto.Cipher import AES

sys.stdout.reconfigure(line_buffering=True)
mpz = gmpy2.mpz

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

p32 = [
    2171932327, 2275965113, 3874429133, 3034637777, 2257272977,
    2215352351, 2458877159, 2216508167, 3725760343, 3600681571,
    4206679031, 2161623829, 3162332429, 3788700907, 3082992901,
]
A0 = mpz(1)
for p in p32:
    A0 *= p
print("15x32 product bits", A0.bit_length())
# pad to 512 bits as smooth() does
if A0.bit_length() < 512:
    A = A0 << (512 - A0.bit_length())
else:
    A = A0
print("A bits", A.bit_length(), flush=True)

X = mpz(1) << 80


def lll_int(B):
    """Nguyen LLL, B is list of lists of mpz, rows = vectors."""
    from fractions import Fraction as F
    n = len(B)
    m = len(B[0])
    B = [list(map(mpz, row)) for row in B]
    delta = F(99, 100)

    def gs():
        mu = [[F(0)] * n for _ in range(n)]
        nrm = [F(0)] * n
        G = [[F(0)] * m for _ in range(n)]
        for i in range(n):
            v = [F(int(B[i][k])) for k in range(m)]
            for j in range(i):
                mu[i][j] = sum(v[k] * G[j][k] for k in range(m)) / nrm[j]
                for k in range(m):
                    v[k] -= mu[i][j] * G[j][k]
            G[i] = v
            nrm[i] = sum(x * x for x in v) or F(1)
        return mu, nrm

    k = 1
    steps = 0
    while k < n:
        steps += 1
        if steps % 200 == 0:
            print("  lll k", k, "steps", steps, flush=True)
        mu, nrm = gs()
        for j in range(k - 1, -1, -1):
            q = mpz(round(mu[k][j]))
            if q:
                for t in range(m):
                    B[k][t] -= q * B[j][t]
        mu, nrm = gs()
        if nrm[k] >= (delta - mu[k][k - 1] ** 2) * nrm[k - 1]:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            k = max(k - 1, 1)
    print("  lll done steps", steps, flush=True)
    return B


def howgrave(A, N, X, mm=4, tt=4):
    # polys x^j * N^{mm-i} * (x+A)^i
    polys = []
    for i in range(mm + 1):
        c = [mpz(1)]  # (x+A)^i
        for _ in range(i):
            nc = [mpz(0)] * (len(c) + 1)
            for k, v in enumerate(c):
                nc[k] += v * A
                nc[k + 1] += v
            c = nc
        scale = pow(N, mm - i)
        c = [v * scale for v in c]
        jmax = tt if i == mm else 0
        for j in range(jmax + 1):
            polys.append([mpz(0)] * j + c)
    maxdeg = max(len(p) - 1 for p in polys)
    M = []
    for p in polys:
        row = p + [mpz(0)] * (maxdeg + 1 - len(p))
        row = [row[k] * pow(X, k) for k in range(len(row))]
        M.append(row)
    print("lattice", len(M), "x", len(M[0]), flush=True)
    B = lll_int(M)
    for vec in B[:5]:
        coeffs = []
        for k, a in enumerate(vec):
            xk = pow(X, k)
            coeffs.append(a // xk if xk else a)
        # drop trailing zeros
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        if len(coeffs) == 2 and coeffs[1]:
            if coeffs[0] % coeffs[1] == 0:
                yield int(-coeffs[0] // coeffs[1])
        # newton
        def h(x):
            v = mpz(0)
            for a in reversed(coeffs):
                v = v * x + a
            return v

        def hp(x):
            v = mpz(0)
            for i in range(len(coeffs) - 1, 0, -1):
                v = v * x + i * coeffs[i]
            return v

        x = mpz(0)
        for _ in range(100):
            d = hp(x)
            if d == 0:
                break
            nx = x - h(x) // d
            if nx == x:
                break
            x = nx
        yield int(x)


def decrypt(p):
    p = int(p)
    if p <= 1 or n % p != 0:
        return None
    q = int(n) // p
    phi = (p - 1) * (q - 1)
    d = int(gmpy2.invert(e, phi))
    m = int(gmpy2.powmod(c, d, n))
    hx = format(m, "x")
    if len(hx) % 2:
        hx = "0" + hx
    raw = bytes.fromhex(hx)
    pt = AES.new(sha256(str(p).encode()).digest(), AES.MODE_CBC, raw[:16]).decrypt(raw[16:])
    pad = pt[-1]
    if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
        pt = pt[:-pad]
    return pt


print("howgrave...", flush=True)
for s in howgrave(A, n, X, mm=3, tt=3):
    print("s candidate", s, "bits", abs(s).bit_length() if s else 0, flush=True)
    if abs(s) >= int(X):
        continue
    for Atry in (A, A0, A0 << 9, A0 * 2463443, A0 * 27053489):
        p = int(Atry) + s
        pt = decrypt(p)
        if pt:
            print("PT", pt)
            Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\writeup\final_flag.txt").write_text(
                pt.decode(errors="replace"), encoding="utf-8"
            )
            raise SystemExit
        p = int(Atry) - s
        pt = decrypt(p)
        if pt:
            print("PT", pt)
            Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\writeup\final_flag.txt").write_text(
                pt.decode(errors="replace"), encoding="utf-8"
            )
            raise SystemExit
print("no decrypt")
