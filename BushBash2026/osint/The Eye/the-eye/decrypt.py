#!/usr/bin/env python3

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

keyRaw = ""

for i in range(8):
    print(f"Enter key {i}: ")
    keyRaw += input()

key = bytes.fromhex(keyRaw)

with open("prayer.enc", "rb") as f:
    ciphertext = f.read()

cipher = AES.new(key, AES.MODE_ECB)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

with open("prayer.txt", "wb") as f:
    f.write(plaintext)
