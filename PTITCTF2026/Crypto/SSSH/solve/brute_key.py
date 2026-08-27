#!/usr/bin/env python3
# Brute-force the 4 unknown characters (XXXX) in the vault key using CRC32 tag verification.
# Key format: SSSH-VAULT-YoDxsAogs4fPVwKhGTUQlaye????
# The tag in the blob is CRC32 of b"SSSH vault tag|" + raw_key + nonce + ciphertext.
# We know nonce (16B) and tag (4B) from the blob. raw_key = key_string.encode().
import base64, binascii, hashlib, string, itertools, re, time

KEY_PREFIX = "SSSH-VAULT-YoDxsAogs4fPVwKhGTUQlaye"
ENC_B64 = "VJz43kaYYYcUkfXRITJ/XX/wPjIYnW+czQ3NBkm8QFA33aftSsgFGv2OLM7wdcl0mYnwHfWRasBCPpK5xyfrpGaf2CUcyJrgmvtuc60="

data = base64.b64decode(ENC_B64)
nonce = data[:16]
tag = data[16:20]
ciphertext = data[20:]
tag_int = int.from_bytes(tag, "big")

print(f"nonce={nonce.hex()}, tag={tag.hex()} (0x{tag_int:08x}), ct_len={len(ciphertext)}")

# Pre-compute fixed part of CRC32 input: b"SSSH vault tag|" + key_prefix_bytes
fixed_prefix = b"SSSH vault tag|" + KEY_PREFIX.encode()
fixed_suffix = nonce + ciphertext

# Charset: try alphanumeric + common special chars
charset = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"

def _stream(raw_key: bytes, nonce: bytes, size: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < size:
        out.extend(hashlib.sha256(raw_key + nonce + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:size])

print(f"Charset size: {len(charset)}, combos: {len(charset)**4}")
t0 = time.time()
found = 0

for c1 in charset:
    for c2 in charset:
        for c3 in charset:
            for c4 in charset:
                suffix = (c1 + c2 + c3 + c4).encode()
                full_input = fixed_prefix + suffix + fixed_suffix
                crc = binascii.crc32(full_input) & 0xffffffff
                if crc == tag_int:
                    key_str = KEY_PREFIX + c1 + c2 + c3 + c4
                    raw_key = key_str.encode()
                    pt = bytes(a ^ b for a, b in zip(ciphertext, _stream(raw_key, nonce, len(ciphertext))))
                    print(f"\n[+] Key found: {key_str}")
                    print(f"    Plaintext: {pt}")
                    m = re.search(rb"PTITCTF\{[^}]+\}", pt)
                    if m:
                        print(f"\n[FLAG] {m.group().decode()}")
                    found += 1

elapsed = time.time() - t0
print(f"\nDone in {elapsed:.1f}s, {found} hit(s)")
