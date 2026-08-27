#!/usr/bin/env python3
import json
from pathlib import Path
data = json.loads(Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\out\clock_fast.json").read_text())
pairs = []
for st, n, p, lit in data["stable"]:
    if len(lit) == 2:
        a, b = sorted(lit)
        pairs.append((a, b))

print("n", len(pairs))

def try_decode(pairs, rot=0, swap=False, mir=False):
    bs = []
    for a, b in pairs:
        if mir:
            a, b = (-a) % 8, (-b) % 8
        a, b = (a + rot) % 8, (b + rot) % 8
        if swap:
            a, b = b, a
        bs.append((a << 3) | b)
    return bytes(bs)

b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
for rot in range(8):
    for swap in (False, True):
        for mir in (False, True):
            raw = try_decode(pairs, rot, swap, mir)
            # as 6-bit + 32 ASCII
            ascii1 = "".join(chr(32 + (x & 63)) for x in raw)
            b64s = "".join(b64[x & 63] for x in raw)
            text = "".join(chr(x) if 32 <= x < 127 else "." for x in raw)
            blob = ascii1 + " | " + b64s + " | " + text
            if any(s in blob.upper() for s in ("PTIT", "FLAG", "CTF")):
                print("HIT rot", rot, "swap", swap, "mir", mir)
                print(" ", ascii1)
                print(" ", b64s)
                print(" ", text)

print("--- samples rot0 ---")
raw = try_decode(pairs, 0, False, False)
print("plus32", "".join(chr(32 + (x & 63)) for x in raw))
print("b64", "".join(b64[x & 63] for x in raw))
print("raw", list(raw)[:20])

# also 5-bit: ignore one numbering
# baudot / ita2
print("as 3+3 two digits", "".join(f"{a}{b}" for a,b in pairs))
