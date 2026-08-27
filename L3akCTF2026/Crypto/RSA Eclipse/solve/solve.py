#!/usr/bin/env python3
"""
RSA Eclipse (L3akCTF 2026 - crypto) solver.

The primes are "Mersenne-void" shaped:  p = 2^607 - a,  q = 2^521 - b
with small a, b. This makes N structurally weak:

  N = p*q = 2^1128 - b*2^607 - a*2^521 + a*b

Every term except a*b is a multiple of 2^521, so:
  N mod 2^521 = a*b            (a*b is tiny -> recovered exactly)
And 2^1128 - N is dominated by b*2^607, so:
  b ~= (2^1128 - N) >> 607

From b and the product a*b we get a, rebuild p, q and decrypt.
Values are read from output.txt.
"""
from Crypto.Util.number import long_to_bytes

N = 3646154850295011369707131011438711095400799139943170490872585628683549034362552065955809589514611470241298944167703929337528884908857116141935206466329730159085752668345654509936331954688615906022854023944431613697568688287347119236246668637626142345227229770764648063010195138432756035056498879142322827510772511775252426866445166513402587
e = 65537
c = 780130031328740731381241557377666116541606927063190613432095157294666504313173452612933931946256744751393203553303107662811734383338538890681670111946446558821571739189651457249936740715582882116998037215610749746023669674781060263244524001085422362588029607510686099014625329616764965784356054346294224270468618614209000880981745855992958

P_BITS, Q_BITS = 607, 521

ab = N % (1 << Q_BITS)                             # = a*b (tiny, exact)
b = ((1 << (P_BITS + Q_BITS)) - N) >> P_BITS       # approx b = high part of 2^1128 - N
assert ab % b == 0, "b guess wrong"
a = ab // b

p = (1 << P_BITS) - a
q = (1 << Q_BITS) - b
assert p * q == N, "factorization failed"

d = pow(e, -1, (p - 1) * (q - 1))
m = pow(c, d, N)
flag = long_to_bytes(m)
print("a =", a, " b =", b)
print("p*q == N:", p * q == N)
print("flag:", flag.decode())
