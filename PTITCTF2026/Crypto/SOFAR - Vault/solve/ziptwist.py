#!/usr/bin/env python3
"""zip-twist-v1 decryptor for SOFAR - Vault.

cipher: zip-twist-v1
seed = SHA256(b"zip-twist-v1|" || passphrase_ascii)
block_i = SHA256(seed || u32be(i))
tmp_byte = plaintext_byte XOR block_i[j]
cipher_byte = ROL8(tmp_byte, rotation)
output = reverse(all_cipher_bytes)

decrypt:
  cipher_bytes_rev = ciphertext (the stored file)
  all_cipher_bytes = reverse(cipher_bytes_rev)   # undo output=reverse()
  for each byte p in order, block=p//32, j=p%32:
     tmp = ROR8(byte, rotation)
     plain = tmp XOR block[block_index][j]
"""
import hashlib, struct, sys

def rol8(b, n):
    n %= 8
    return ((b << n) | (b >> (8 - n))) & 0xFF if n else b

def ror8(b, n):
    n %= 8
    return ((b >> n) | (b << (8 - n))) & 0xFF if n else b

def decrypt(ciphertext: bytes, passphrase: bytes, rotation: int) -> bytes:
    seed = hashlib.sha256(b"zip-twist-v1|" + passphrase).digest()
    L = len(ciphertext)
    nblocks = (L + 31) // 32
    blocks = []
    for i in range(nblocks):
        blocks.append(hashlib.sha256(seed + struct.pack(">I", i)).digest())
    # undo output reverse
    c = ciphertext[::-1]
    out = bytearray()
    for p, b in enumerate(c):
        tmp = ror8(b, rotation)
        j = p % 32
        out.append(tmp ^ blocks[p // 32][j])
    return bytes(out)

def encrypt(plaintext: bytes, passphrase: bytes, rotation: int) -> bytes:
    seed = hashlib.sha256(b"zip-twist-v1|" + passphrase).digest()
    nblocks = (len(plaintext) + 31) // 32
    blocks = [hashlib.sha256(seed + struct.pack(">I", i)).digest() for i in range(nblocks)]
    tmp_bytes = bytearray()
    for p, b in enumerate(plaintext):
        j = p % 32
        tmp_bytes.append(b ^ blocks[p // 32][j])
    c = bytearray(rol8(b, 1) for b in tmp_bytes)  # placeholder rotation
    return bytes(tmp_bytes)

if __name__ == "__main__":
    # quick self-test
    pt = b"Hello World! This is a test of the zip-twist cipher."
    # We need rotation; test rotation 0 and 3
    for rot in range(8):
        enc = bytearray()
        # manual encrypt with rotation rot
        seed = hashlib.sha256(b"zip-twist-v1|" + b"test").digest()
        nblocks = (len(pt)+31)//32
        blocks=[hashlib.sha256(seed+struct.pack(">I",i)).digest() for i in range(nblocks)]
        tmp=[pt[p]^blocks[p//32][p%32] for p in range(len(pt))]
        enc_bytes=bytes(rol8(x,rot) for x in tmp)[::-1]
        dec=decrypt(enc_bytes,b"test",rot)
        if dec==pt:
            print("rot",rot,"OK roundtrip")
