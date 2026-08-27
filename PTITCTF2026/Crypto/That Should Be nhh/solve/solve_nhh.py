#!/usr/bin/env python3
"""That Should Be nhh — recover AES key sha256(str(p)) from special RSA.

Public (e, N): e/N ≈ v/u with tiny u,v (Wiener/CF).
K ≈ e*u/v = A*(q-r); A is 32-bit-smooth.
p = A + s (|s|<2^80) → Howgrave-Graham known-MSBs.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path

import gmpy2
from Crypto.Cipher import AES

N = 142217133950331383280849240147704444479347756839197748359496621059788089766910006904838605206502343346784621083909830941944628842677247904138991949650529500950063288595336962598606848151740001164215358829068316743899886573916423795874723508083910684350048423004067616316245233835164152303866893899098404075307
E = 735562091150242199086137919579103601129940065511032380153512599537270426450426263582268920053003161544983227567832252495021917091489748774366094722437238758924451476396513769768400726278723557098141590858309774096405563453563592561074531837480565567125040985794075273534996592428835861192841524496633102653
C = 137457406660129767400819964317866522985441842464715884517889980293434382803283064686956906367455039759668586682637407035813231325408151214355647002146143963348554367638105785351285114550546508429635975747755892192290014158317026703192846835308010477939727103064715916819117898597698267398988054857699040341517
# NOTE: c copied from enc.sage — verify digits!

DBIT, SBIT, PBIT = 96, 80, 512


def continued_fraction_convergents(num: int, den: int):
    a, b = num, den
    cf = []
    while b:
        q, r = divmod(a, b)
        cf.append(q)
        a, b = b, r
    n0, n1 = 0, 1
    d0, d1 = 1, 0
    conv = []
    for q in cf:
        n0, n1 = n1, q * n1 + n0
        d0, d1 = d1, q * d1 + d0
        conv.append((n1, d1))
    return conv


def pollard_rho(n: int, rounds: int = 200_000) -> int | None:
    if n % 2 == 0:
        return 2
    if gmpy2.is_prime(n):
        return None
    for c in (1, 2, 3, 5, 7, 11):
        x = y = 2
        d = 1
        f = lambda v: (v * v + c) % n
        for _ in range(rounds):
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
            if d == n:
                break
            if d > 1:
                return d
    return None


def strip_small_factors(n: int, max_bits: int = 32) -> tuple[int, int]:
    """Return (smooth_part, remaining)."""
    smooth = 1
    # twos
    while n % 2 == 0:
        n //= 2
        smooth *= 2
    # tiny trial
    p = 3
    while p * p <= min(n, 1 << 20):
        while n % p == 0:
            n //= p
            smooth *= p
        p += 2
    # rho for remaining 32-bit factors
    guard = 0
    while n.bit_length() > PBIT + 8 and guard < 40:
        guard += 1
        f = pollard_rho(n)
        if not f:
            break
        if f.bit_length() > max_bits + 2:
            # large factor — keep in remaining if ~512-bit composite split
            if f.bit_length() >= PBIT - 20:
                break
            # maybe Qr split; stop
            break
        while n % f == 0:
            n //= f
            smooth *= f
    return smooth, n


def lll(M: list[list[int]], delta: Fraction = Fraction(99, 100)):
    """Simple integer LLL (Nguyen-Stehlé style), M rows are basis vectors."""
    from fractions import Fraction as F

    n = len(M)
    m = len(M[0])
    B = [list(map(int, row)) for row in M]

    def dot(i, j):
        return sum(B[i][k] * B[j][k] for k in range(m))

    def gram():
        mu = [[F(0)] * n for _ in range(n)]
        nrm = [F(0)] * n
        Gs = [[F(0)] * m for _ in range(n)]
        for i in range(n):
            v = [F(B[i][k]) for k in range(m)]
            for j in range(i):
                mu[i][j] = sum(v[k] * Gs[j][k] for k in range(m)) / nrm[j]
                for k in range(m):
                    v[k] -= mu[i][j] * Gs[j][k]
            Gs[i] = v
            nrm[i] = sum(x * x for x in v)
            if nrm[i] == 0:
                nrm[i] = F(1)
        return mu, nrm

    k = 1
    while k < n:
        mu, nrm = gram()
        # size reduce
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                for t in range(m):
                    B[k][t] -= q * B[j][t]
        mu, nrm = gram()
        if nrm[k] >= (delta - mu[k][k - 1] ** 2) * nrm[k - 1]:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            k = max(k - 1, 1)
    return B


def howgrave_univariate(A: int, N: int, X: int, mm: int = 6, tt: int = 6):
    """Find small x0, |x0|<X, such that gcd(A+x0, N) is nontrivial.
    Polynomial f(x)=x+A, Howgrave-Graham / Coppersmith, beta=0.5.
    """
    # Use f(x) = x + A  (monic). Work with F(x) = f(xX)/? standard:
    # polynomials g_{i,j} = x^j * N^{m-i} * f(x)^i  for i=0..m, j=0..t? 
    # for deg 1, i=0..mm, j=0..tt for i=mm only typically.
    # Lattice of coefficients of g(xX).
    fA = A  # f = x + A

    # monomials 1, x, x^2, ..., x^{mm+tt}
    nn = mm + tt + 1
    # each row: coeffs of  N^{mm-i} * (x+A)^i * x^j   evaluated as poly in x, then subst x->X
    polys = []
    for i in range(mm + 1):
        # (x+A)^i * N^{mm-i}
        # binom
        coef = [0] * (i + 1)
        # (x+A)^i
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
        # actually standard: for i=0..m-1, only j=0; for i=m, j=0..t
        if i < mm:
            jmax = 0
        for j in range(jmax + 1):
            pc = [0] * j + c  # * x^j
            polys.append(pc)

    dim = len(polys)
    maxdeg = max(len(p) - 1 for p in polys)
    # pad
    M = []
    for p in polys:
        row = p + [0] * (maxdeg + 1 - len(p))
        # multiply coeff of x^k by X^k
        row = [row[k] * pow(X, k) for k in range(len(row))]
        M.append(row)

    print(f"  LLL dim={len(M)} deg={maxdeg} ...")
    B = lll(M)
    # shortest vector -> polynomial
    for vec in B[:4]:
        # divide out X^k
        coeffs = []
        for k, a in enumerate(vec):
            if a == 0:
                coeffs.append(0)
                continue
            xk = pow(X, k)
            if a % xk != 0:
                coeffs.append(a // xk)  # tolerate
            else:
                coeffs.append(a // xk)
        # try small integer roots of this poly, or gcd with f
        # evaluate brute is impossible; use derivative Newton for |x|<X is still 2^80
        # Instead: resultant/gcd approach: the short poly h(x) satisfies h(x0)=0
        # recover x0 as rational root (possible small roots of h)
        # try rational-root: factors of const / leading
        while coeffs and coeffs[-1] == 0:
            coeffs.pop()
        if len(coeffs) < 2:
            continue
        # gcd of content
        g = 0
        for a in coeffs:
            g = gcd(g, abs(a))
        if g > 1:
            coeffs = [a // g for a in coeffs]
        # linear?
        if len(coeffs) == 2:
            # c0 + c1 x = 0 => x = -c0/c1
            c0, c1 = coeffs[0], coeffs[1]
            if c1 and c0 % c1 == 0:
                x0 = -c0 // c1
                yield x0
        # quadratic formula
        if len(coeffs) == 3:
            c0, c1, c2 = coeffs
            disc = c1 * c1 - 4 * c2 * c0
            if disc >= 0:
                s = isqrt(disc)
                if s * s == disc:
                    for sgn in (1, -1):
                        num = -c1 + sgn * s
                        den = 2 * c2
                        if den and num % den == 0:
                            yield num // den
        # try gcd(N, A+x) for x = -const/lead if nearly linear (high coeffs tiny)
        if coeffs[-1]:
            # possible integer roots: factors of const term — too many
            # Newton from 0
            def h(x):
                v = 0
                for a in reversed(coeffs):
                    v = v * x + a
                return v

            def hp(x):
                v = 0
                for i in range(len(coeffs) - 1, 0, -1):
                    v = v * x + i * coeffs[i]
                return v

            x = 0
            for _ in range(80):
                pval = hp(x)
                if pval == 0:
                    break
                nxt = x - h(x) // pval
                if nxt == x:
                    break
                x = nxt
            yield x


def decrypt_flag(p: int, n: int, e: int, c: int) -> bytes | None:
    q = n // p
    if p * q != n:
        return None
    phi = (p - 1) * (q - 1)
    d = int(gmpy2.invert(e, phi))
    m = int(gmpy2.powmod(c, d, n))
    raw = bytes.fromhex(format(m, "x") if len(format(m, "x")) % 2 == 0 else "0" + format(m, "x"))
    if len(raw) < 17:
        return None
    iv, ct = raw[:16], raw[16:]
    key = sha256(str(p).encode()).digest()
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
        pt = pt[:-pad]
    return pt


def main():
    # verify c from file (avoid transcription error)
    sage = Path(__file__).resolve().parents[1] / "files" / "enc.sage"
    text = sage.read_text(encoding="utf-8")
    ns, es, cs = None, None, None
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("#"):
            continue
        line = line.lstrip("#").strip().replace(" ", "")
        if line.startswith("n="):
            ns = int(line[2:])
        elif line.startswith("e="):
            es = int(line[2:])
        elif line.startswith("c="):
            cs = int(line[2:])
    n, e, c = ns, es, cs
    assert n and e and c
    print("n bits", n.bit_length(), "e bits", e.bit_length(), "c bits", c.bit_length())
    print("e/n", float(Fraction(e, n)))

    conv = continued_fraction_convergents(e, n)
    hits = []
    for v, u in conv:
        if u <= 0 or v <= 0:
            continue
        if u.bit_length() > DBIT + 4 or v.bit_length() > DBIT + 4:
            continue
        if u.bit_length() >= DBIT - 12 and v.bit_length() >= DBIT - 16:
            hits.append((v, u))
    print("CF candidates", len(hits))
    for v, u in hits[-10:]:
        print("  v", v.bit_length(), "u", u.bit_length(), v, u)

    # also Fraction.limit_denominator
    ap = Fraction(e, n).limit_denominator(1 << DBIT)
    print("limit_denom", ap.numerator.bit_length(), ap.denominator.bit_length(), ap.numerator, ap.denominator)
    if (ap.numerator, ap.denominator) not in hits:
        hits.append((ap.numerator, ap.denominator))

    X = 1 << SBIT
    tried = 0
    for v, u in hits:
        if gcd(v, u) != 1:
            continue
        # K = (e*u - w)/v , |w|<2^DBIT
        # w ≡ e*u (mod v)
        eu = e * u
        # K near eu/v
        K0, rem = divmod(eu, v)
        # rem = eu - K0*v = w when using this K0? w = eu - K v
        # try K = K0 and K0+1 and nearby t with |eu-K v| < 2^DBIT
        # |K - eu/v| < 2^DBIT / v  ≈ 2^(DBIT - vbits)
        radius = (1 << DBIT) // v + 3
        print(f"u={u.bit_length()}b v={v.bit_length()}b K0bits={K0.bit_length()} radius={radius}")
        for dt in range(-radius, radius + 1):
            K = K0 - dt
            if K <= 0:
                continue
            w = eu - K * v
            if abs(w) >= (1 << DBIT):
                continue
            A, rest = strip_small_factors(K)
            if A.bit_length() < PBIT - 40 or rest.bit_length() < PBIT - 40:
                continue
            # A should be ~512 bits
            if abs(A.bit_length() - PBIT) > 8:
                continue
            tried += 1
            print(f"  candidate A bits {A.bit_length()} rest {rest.bit_length()} w bits {abs(w).bit_length()}")
            # p ≈ A, try gcd(A, N) no; Howgrave
            for x0 in howgrave_univariate(A, n, X, mm=5, tt=5):
                if abs(x0) >= X:
                    continue
                p = A + x0
                if p > 1 and n % p == 0:
                    print("FACTOR p", p)
                    pt = decrypt_flag(p, n, e, c)
                    print("PT", pt)
                    if pt:
                        out = Path(__file__).resolve().parents[1] / "writeup" / "final_flag.txt"
                        try:
                            s = pt.decode()
                        except Exception:
                            s = repr(pt)
                        out.write_text(s if s.startswith("PTIT") else f"PTITCTF{{{s}}}", encoding="utf-8")
                        print("wrote", out)
                        return
            # also try p = A + s with s odd small via gcd(A,N) and gcd(A±1..? no
            g = gcd(A, n)
            if 1 < g < n:
                print("gcd A", g)
                pt = decrypt_flag(g, n, e, c)
                print(pt)
                return
        print("  done this (u,v), tried K", tried)


if __name__ == "__main__":
    main()
