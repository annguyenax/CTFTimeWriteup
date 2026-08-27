from itertools import product

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# Candidate characters come only from the nearest raster glyphs printed by
# inspect_glyphs.py. This is a bounded OCR correction, not a key-space brute
# force: 196,608 candidate renderings out of 2^128 AES keys.
glyphs = [
    ["F"], ["0", "9"], ["2"], ["E"],
    ["0", "9"], ["2"], ["9", "0"], ["F"],
    ["2"], ["3", "8"], ["5", "6"], ["8", "6"],
    ["2"], ["D", "B"], ["C"], ["8", "6"],
    ["2"], ["9", "0"], ["F"], ["0", "9"],
    ["3", "2"], ["4"], ["8", "6", "B"], ["8", "6", "3", "9"],
    ["D"], ["9", "0"], ["5", "6", "8", "0"], ["7"],
    ["B"], ["7"], ["A"], ["8"],
]
ciphertext = open("../the-eye/prayer.enc", "rb").read()
last_block = ciphertext[-16:]
tested = 0
for chars in product(*glyphs):
    keyhex = "".join(chars)
    cipher = AES.new(bytes.fromhex(keyhex), AES.MODE_ECB)
    tail = cipher.decrypt(last_block)
    pad = tail[-1]
    tested += 1
    if not (1 <= pad <= 16 and tail[-pad:] == bytes([pad]) * pad):
        continue
    plain = cipher.decrypt(ciphertext)
    try:
        plain = unpad(plain, 16)
    except ValueError:
        continue
    printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
    if b"bushbash{" in plain.lower() or printable > 0.85:
        print("AES HIT", keyhex, repr(plain))
print("tested", tested)
