from itertools import product

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


segments = [
    ["91C5"],
    ["A991"],
    ["AB8D"],
    ["8FFF"],
    ["400A"],
    ["7A90"],
    ["F78A", "8DF7"],
    ["400A", "AFF3", "571A", "A011", "1130", "A0A1", "58A0", "4F0C"],
]
ciphertext = open("../the-eye/prayer.enc", "rb").read()
for parts in product(*segments):
    keyhex = "".join(parts)
    decrypted = AES.new(bytes.fromhex(keyhex), AES.MODE_ECB).decrypt(ciphertext)
    try:
        plain = unpad(decrypted, 16)
    except ValueError:
        continue
    printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
    if b"bushbash{" in plain.lower() or printable > 0.85:
        print("AES HIT", keyhex, repr(plain))
