#!/usr/bin/env python3
"""
BabyLCG (L3akCTF 2026 - Beginner/crypto) solver.

Given a truncated LCG state sequence (s0, s1, s2) modulo m, recover the
multiplier `a` and increment `c`, predict the next output `key`, and XOR it
against the ciphertext to recover the flag.

LCG recurrence:  s_{n+1} = (a*s_n + c) mod m

Values are read from the challenge output.txt (chall.py prints them).
"""

# Values from Beginner/BabyLCG/files -> output.txt
m  = 88044978735773602913395349457408066612245192322881563734438993831688084200491
s0 = 4452065008288242560629390669208864932242141417756588067313178112477164149842
s1 = 30356301725547557665274966292036883630163427635439138410477840356169747135880
s2 = 33330863090985168864945055645699247424789280002692545918305324950320521259312
ct = 8850041716144071587274828779665113489634774808247082181515445941038495956603515

# s1 - s0 = a*(s0 - s_{-1})... but with two consecutive diffs the increment c cancels:
#   s1 - s0 = a*(s0) + c - (a*s_{-1} + c)   (not directly usable)
# Instead use the two known recurrences directly:
#   s1 = a*s0 + c
#   s2 = a*s1 + c
# Subtract: s2 - s1 = a*(s1 - s0)  =>  a = (s2 - s1) * inv(s1 - s0) mod m
a = ((s2 - s1) * pow(s1 - s0, -1, m)) % m
c = (s1 - a * s0) % m

# Sanity: the recovered params must regenerate the observed states.
assert (a * s0 + c) % m == s1
assert (a * s1 + c) % m == s2

# The next output after s2 is the XOR key used on the flag.
key = (a * s2 + c) % m
flag_int = ct ^ key
flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, "big")

print("a   =", a)
print("c   =", c)
print("key =", key)
print("flag =", flag.decode())
