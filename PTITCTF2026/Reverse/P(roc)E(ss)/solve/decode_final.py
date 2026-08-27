#!/usr/bin/env python3
"""
P(roc)E(ss) flag decoder — CORRECTED.

The challenge binary (MinGW x64) contains a dead-code ARX stream cipher at
0x140002379 (referenced only from .data[0], never called). The real flag is
recovered offline by decrypting the ciphertext blob found in .rdata.

Algorithm (reversed from disassembly, cross-checked by running the real function
in angr):
  key  = tolower(strip(".exe", xor_decode(blob@0x14000503c, 0x64)))  -> "4mcnfu"
  salt = blob@0x14000502c (16 bytes)
  arg3 = 0  (nonce)

  key schedule: seed = fnv1a64(key) -> fnv1a64(salt) -> fnv1a64(arg3_le)
                then 3x splitmix64 finalizer -> 24 bytes -> 6 dwords k[0..5]
  per 8-byte block i:
      a = (i ^ k[4]); b = (k[5] ^ arg3)
      27 rounds ARX over state (s0=k0, s1=k1, s2=k2, s3=k3):
          a = (ror(a,8)+b) ^ s0
          b = rol(b,3) ^ a
          j = r % 3
          s[j] = (ror(s[j],8)+s0) ^ r      # s[0]=s1, s[1]=s2, s[2]=s3
          s0 = rol(s0,3) ^ s[j]
      keystream = (a, b) little-endian, XORed with ciphertext

Ciphertext = 36 bytes at file offset 0x36b3 in .rdata.
Plaintext  = "50m371m35_1nf0rm4710n_1n_42ce4d87b74" (leetspeak, readable).
"""
import struct

MASK = 0xffffffffffffffff
SALT = bytes.fromhex('7f69fd375b06cd415d4b36aade3db1a1')  # @0x14000502c
ARG3 = 0
KEY = b'4mcnfu'   # tolower(strip(".exe", "4mCnFu.exe"))
CIPHERTEXT_OFFSET = 0x36b3   # file offset of the ciphertext in live_chall.exe
CIPHERTEXT_LEN = 36


def fnv1a_64(data, seed=0xcbf29ce484222325):
    for b in data:
        seed ^= b
        seed = (seed * 0x100000001b3) & MASK
    return seed


def splitmix_final(x):
    x &= MASK
    x ^= x >> 30
    x = (x * 0xbf58476d1ce4e5b9) & MASK
    x ^= x >> 27
    x = (x * 0x94d049bb133111eb) & MASK
    x ^= x >> 31
    return x


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff


def rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def arx(a, b, k):
    s0, s1, s2, s3 = k[0], k[1], k[2], k[3]
    st = [s1, s2, s3]
    for r in range(27):
        a = ((ror(a, 8) + b) ^ s0) & 0xffffffff
        b = (rol(b, 3) ^ a) & 0xffffffff
        i = r % 3
        st[i] = ((ror(st[i], 8) + s0) ^ r) & 0xffffffff
        s0 = (rol(s0, 3) ^ st[i]) & 0xffffffff
    return a, b


def key_schedule(key, arg3=ARG3):
    s = fnv1a_64(key)
    s = fnv1a_64(SALT, s)
    s = fnv1a_64(struct.pack('<I', arg3 & 0xffffffff), s)
    words = []
    for _ in range(3):
        s = (s + 0x9e3779b97f4a7c15) & MASK
        words.append(splitmix_final(s))
    return list(struct.unpack('<6I', b''.join(x.to_bytes(8, 'little') for x in words)))


def decrypt(blob, key=KEY, arg3=ARG3):
    k = key_schedule(key, arg3)
    out = bytearray(len(blob))
    for i in range(0, len(blob), 8):
        a = (i // 8) ^ k[4]
        b = k[5] ^ arg3
        a, b = arx(a, b, k)
        kb = struct.pack('<II', a, b)
        for j in range(8):
            if i + j < len(blob):
                out[i + j] = blob[i + j] ^ kb[j]
    return bytes(out)


if __name__ == '__main__':
    data = open('live_chall.exe', 'rb').read()
    ct = data[CIPHERTEXT_OFFSET:CIPHERTEXT_OFFSET + CIPHERTEXT_LEN]
    pt = decrypt(ct)
    flag = 'PTITCTF2026{' + pt.decode('latin1') + '}'
    print('ciphertext:', ct.hex())
    print('plaintext :', pt)
    print('flag      :', flag)
