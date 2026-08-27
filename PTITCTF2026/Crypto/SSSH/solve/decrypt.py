#!/usr/bin/env python3
# SSSH vault: raw_key = base64decode("SSSH-VAULT-" stripped). The last 4 base64 chars in key.txt are
# shown as "XXXX" (redacted/unknown) -> the last 3 raw_key bytes are unknown. Brute them (2^24) using
# the crc32 tag as an oracle, then XOR-SHA256-keystream decrypt.
import base64, binascii, hashlib

KEY = "SSSH-VAULT-YoDxsAogs4fPVwKhGTUQlayeXXXX"
ENC = "VJz43kaYYYcUkfXRITJ/XX/wPjIYnW+czQ3NBkm8QFA33aftSsgFGv2OLM7wdcl0mYnwHfWRasBCPpK5xyfrpGaf2CUcyJrgmvtuc60="

data = base64.b64decode(ENC)
nonce, tag, ct = data[:16], data[16:20], data[20:]
tag_val = int.from_bytes(tag, "big")

after = KEY[len("SSSH-VAULT-"):]          # YoDxsAogs4fPVwKhGTUQlayeXXXX
known = after.rstrip("X")                  # YoDxsAogs4fPVwKhGTUQlaye  (24 chars -> 18 bytes)
assert len(known) % 4 == 0
base = base64.b64decode(known)             # first 18 bytes of raw_key
print(f"[*] known raw_key prefix = {len(base)} bytes; brute 3 bytes (crc32 tag oracle)")

prefix_crc = binascii.crc32(b"SSSH vault tag|" + base)   # running crc up to the unknown bytes
suffix = nonce + ct

def stream(rk, nonce, size):
    out = bytearray(); c = 0
    while len(out) < size:
        out.extend(hashlib.sha256(rk + nonce + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(out[:size])

found = []
for x in range(1 << 24):
    b3 = x.to_bytes(3, "big")
    c = binascii.crc32(b3, prefix_crc)
    c = binascii.crc32(suffix, c)
    if c == tag_val:
        rk = base + b3
        pt = bytes(a ^ b for a, b in zip(ct, stream(rk, nonce, len(ct))))
        print(f"[+] TAG MATCH b3={b3.hex()} -> {pt!r}")
        found.append(pt)
        import re
        m = re.search(rb"PTITCTF\{[^}]+\}", pt)
        if m:
            print("\n[FLAG]", m.group().decode()); break
if not found:
    print("[-] no tag match. raw_key derivation differs (maybe key uses full string / different KDF).")
