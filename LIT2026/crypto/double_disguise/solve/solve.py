#!/usr/bin/env python3
"""
LIT2026 / crypto / double_disguise
Two disguise layers: Base64 (outer) over single-byte XOR (inner).

Given only the ciphertext string, we:
  1. Base64-decode it (layer 1).
  2. Recover the single-byte XOR key from the known flag prefix 'LITCTF{'
     (each key byte is identical -> single-byte XOR). Key = 0x2A.
  3. XOR to get the flag.
"""
import base64

CIPHERTEXT_B64 = 'ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw=='
KNOWN_PREFIX = b'LITCTF{'


def solve():
    raw = base64.b64decode(CIPHERTEXT_B64)                 # layer 1: base64
    key_stream = [raw[i] ^ KNOWN_PREFIX[i] for i in range(len(KNOWN_PREFIX))]
    assert len(set(key_stream)) == 1, 'not a single-byte XOR'
    key = key_stream[0]                                     # layer 2: XOR key
    flag = bytes(b ^ key for b in raw).decode()
    return key, flag


if __name__ == '__main__':
    key, flag = solve()
    print(f'xor key = {key} (0x{key:02x})')
    print(f'flag    = {flag}')
    # verification: re-encrypt (xor + base64) must reproduce the ciphertext
    reenc = base64.b64encode(bytes(b ^ key for b in flag.encode())).decode()
    assert reenc == CIPHERTEXT_B64, 'round-trip failed'
    print('round-trip re-encryption OK')
