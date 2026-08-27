#!/usr/bin/env python3
"""
Immiscible (L3akCTF 2026 - crypto) solver.

The public key is the RAW central map of an Oil-and-Vinegar scheme over F_79:
9 quadratic polynomials in 8 variables (V=4 vinegar x0..x3, O=4 oil x4..x7).
Crucially there are NO oil*oil terms ("immiscible" — oil and vinegar don't mix).

=> Fix the 4 vinegar variables and every equation becomes LINEAR in the 4 oil vars.
Brute-force the vinegar space (79^4), solve the 9x4 (overdetermined) linear system
for oil using the first 4 equations, and verify the remaining 5. The unique
consistent point is the secret signature; AES key = sha256(bytes(signature)).

Pure numpy (batched modular Gaussian elimination) — no z3/sage needed. ~10s.
"""
import json, hashlib, numpy as np, sys
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

P, M, V, O = 79, 9, 4, 4
here = Path(__file__).parent
data = json.loads((here / "public.json").read_text())
target = data["target"]; polys = data["polynomials"]; ct = bytes.fromhex(data["encrypted_flag"])

const = np.array([polys[k]["const"] for k in range(M)])
lin   = np.array([polys[k]["linear"] for k in range(M)])      # (9,8)
Cvv   = np.zeros((M, V, V), dtype=np.int64)                   # vinegar*vinegar
Dvo   = np.zeros((M, V, O), dtype=np.int64)                   # vinegar*oil
for k in range(M):
    for i, j, c in polys[k]["quad"]:
        if j < V: Cvv[k, i, j] = c
        else:     Dvo[k, i, j - V] = c

inv = np.array([0] + [pow(a, P - 2, P) for a in range(1, P)])

def batch_solve(A, b):
    """Solve A(K,4,4) x = b(K,4) over F_P via batched Gauss-Jordan. Return x, valid."""
    A = A.copy() % P; b = b.copy() % P; K = A.shape[0]; valid = np.ones(K, bool)
    for col in range(4):
        found = A[:, col, col] % P != 0
        for row in range(col + 1, 4):
            need = (~found) & (A[:, row, col] % P != 0)
            if need.any():
                A[need, col, :], A[need, row, :] = A[need, row, :].copy(), A[need, col, :].copy()
                b[need, col], b[need, row] = b[need, row].copy(), b[need, col].copy()
                found |= need
        valid &= found
        piv = A[:, col, col] % P; pivinv = np.where(piv != 0, inv[piv % P], 0)
        A[:, col, :] = (A[:, col, :] * pivinv[:, None]) % P; b[:, col] = (b[:, col] * pivinv) % P
        for row in range(4):
            if row == col: continue
            f = A[:, row, col].copy() % P
            A[:, row, :] = (A[:, row, :] - f[:, None] * A[:, col, :]) % P
            b[:, row] = (b[:, row] - f * b[:, col]) % P
    return b % P, valid

def eval_public(sig):
    out = []
    for k in range(M):
        t = polys[k]["const"]
        for i, c in enumerate(polys[k]["linear"]): t += c * sig[i]
        for i, j, c in polys[k]["quad"]: t += c * sig[i] * sig[j]
        out.append(t % P)
    return out

rng = range(P)
for v0 in rng:
    g = np.array(np.meshgrid(rng, rng, rng, indexing='ij')).reshape(3, -1).T
    K = g.shape[0]
    Vm = np.empty((K, 4), dtype=np.int64); Vm[:, 0] = v0; Vm[:, 1:] = g
    C = (const[None, :] + Vm[:, :V] @ lin[:, :V].T) % P
    for i in range(V):
        for j in range(i, V):
            C = (C + Cvv[:, i, j][None, :] * (Vm[:, i] * Vm[:, j])[:, None]) % P
    D = lin[:, V:][None, :, :].astype(np.int64).repeat(K, 0)
    for i in range(V):
        D = D + Vm[:, i][:, None, None] * Dvo[:, i, :][None, :, :]
    D %= P
    r = (np.array(target)[None, :] - C) % P
    oil, valid = batch_solve(D[:, :4, :], r[:, :4])
    chk = (np.einsum('kro,ko->kr', D[:, 4:, :], oil) % P == r[:, 4:] % P).all(1)
    for t in np.nonzero(valid & chk)[0]:
        sig = [int(z) % P for z in list(Vm[t]) + list(oil[t])]
        if eval_public(sig) != target:      # rigorous check
            continue
        key = hashlib.sha256(bytes(sig)).digest()
        try:
            flag = unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), 16)
        except ValueError:
            continue
        print("signature   :", sig)
        print("eval==target:", eval_public(sig) == target)
        print("flag        :", flag.decode())
        sys.exit(0)
print("no solution found")
