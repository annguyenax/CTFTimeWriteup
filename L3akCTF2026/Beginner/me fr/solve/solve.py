#!/usr/bin/env python3
"""
me fr (L3akCTF 2026 - Beginner/misc) solver.

The message was typed with the right hand shifted one key to the RIGHT on a
QWERTY keyboard (a classic "hands misaligned" typing mistake). Every right-hand
key came out as the key immediately to its right; left-hand keys, digits 1-5 and
spaces are unaffected.

Decoding = for each typed right-hand key, take the key one column to its LEFT
on the same physical row, preserving the shift (upper) state.
"""
import re

# Physical QWERTY rows: (unshifted, shifted). Right-hand keys begin at index 5
# (the leftmost right-hand key, e.g. 'h'/'y'/'n'/'6', only appears as a decode
# target, never as a typed character), so typed keys we remap are index >= 6.
ROWS = [
    ("1234567890-=",  "!@#$%^&*()_+"),
    ("qwertyuiop[]\\", "QWERTYUIOP{}|"),
    ("asdfghjkl;'",   'ASDFGHJKL:"'),
    ("zxcvbnm,./",    "ZXCVBNM<>?"),
]

decode_map = {}
for lower, upper in ROWS:
    for layer in (lower, upper):
        for i in range(6, len(layer)):
            decode_map[layer[i]] = layer[i - 1]


def decode(text: str) -> str:
    return "".join(decode_map.get(c, c) for c in text)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "files/me_fr.txt"
    with open(path, "rb") as f:
        cipher = f.read().decode()
    plain = decode(cipher)
    print(plain)
    m = re.search(r"L3AK\{[^}]*\}", plain)
    print("FLAG:", m.group(0) if m else "not found")
