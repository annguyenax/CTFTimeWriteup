#!/usr/bin/env python3
import sys
from pathlib import Path
from hashlib import sha256
import gmpy2
from sympy import Matrix
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

p32 = [
    2171932327, 2275965113, 3874429133, 3034637777, 2257272977,
    2215352351, 2458877159, 2216508167, 3725760343, 3600681571,
    4206679031, 2161623829, 3162332429, 3788700907, 3082992901,
]
A0 = 1
for p in p32:
    A0 *= p
As = [
    A0 << 40,
    A0 * 27053489 << 16,
    A0 * 2463443 << 19,
]
X = 1 << 80


def howgrave(A, N, X, mm=3, tt=3):
    polys = []
    for i in range(mm + 1):
        c = [1]
        for _ in range(i):
            nc = [0] * (len(c) + 1)
            for k, v in enumerate(c):
                nc[k] += v * A
                nc[k + 1] += v
            c = nc
        scale = pow(N, mm - i)
        c = [v * scale for v in c]
        jmax = tt if i == mm else 0
        for j in range(jmax + 1):
            polys.append([0] * j + c)
    maxdeg = max(len(p) - 1 for p in polys)
    rows = []
    for p in polys:
        row = p + [0] * (maxdeg + 1 - len(p))
        row = [row[k] * pow(X, k) for k in range(len(row))]
        rows.append(row)
    B = Matrix(rows).lll()
    roots = []
    for i in range(min(6, B.rows)):
        vec = [int(B[i, j]) for j in range(B.cols)]
        coeffs = [vec[k] // pow(X, k) for k in range(len(vec))]
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        if len(coeffs) == 2 and coeffs[1] and coeffs[0] % coeffs[1] == 0:
            roots.append(-coeffs[0] // coeffs[1])
        x = 0
        for _ in range(80):
            h = hp = 0
            for a in reversed(coeffs):
                hp = hp * x + h
                h = h * x + a
            if hp == 0:
                break
            nx = x - h // hp
            if nx == x:
                break
            x = nx
        roots.append(x)
    return roots


def decrypt(p):
    if p <= 1 or n % p:
        return None
    q = n // p
    d = int(gmpy2.invert(e, (p - 1) * (q - 1)))
    m = int(gmpy2.powmod(c, d, n))
    hx = format(m, "x")
    if len(hx) % 2:
        hx = "0" + hx
    raw = bytes.fromhex(hx)
    pt = AES.new(sha256(str(p).encode()).digest(), AES.MODE_CBC, raw[:16]).decrypt(raw[16:])
    pad = pt[-1]
    if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
        return pt[:-pad]
    return pt


for i, A in enumerate(As):
    print("=== A", i, "bits", A.bit_length(), flush=True)
    for s in howgrave(A, n, X):
        print(" s", s, "bits", abs(s).bit_length() if s else 0, flush=True)
        for p in (A + s, A - s):
            if abs(p).bit_length() != 512:
                continue
            pt = decrypt(p)
            if pt:
                print("PT", pt)
                Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\That Should Be nhh\writeup\final_flag.txt").write_text(
                    pt.decode(errors="replace"), encoding="utf-8"
                )
                raise SystemExit
print("no flag")
