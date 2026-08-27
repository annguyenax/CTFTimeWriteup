#!/usr/bin/env python3
# Decrypt SSSH vault using the exact getflag.py algorithm found on the server.
import base64, binascii, hashlib, re

KEY_TXT = "SSSH-VAULT-YoDxsAogs4fPVwKhGTUQlayeXXXX"
ENC_B64 = "VJz43kaYYYcUkfXRITJ/XX/wPjIYnW+czQ3NBkm8QFA33aftSsgFGv2OLM7wdcl0mYnwHfWRasBCPpK5xyfrpGaf2CUcyJrgmvtuc60="

def _stream(raw_key: bytes, nonce: bytes, size: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < size:
        out.extend(hashlib.sha256(raw_key + nonce + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:size])

def _tag(raw_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    value = binascii.crc32(b"SSSH vault tag|" + raw_key + nonce + ciphertext) & 0xffffffff
    return value.to_bytes(4, "big")

def decrypt(blob_b64: str, raw_key: bytes) -> bytes:
    data = base64.b64decode(blob_b64)
    nonce = data[:16]
    tag = data[16:20]
    ciphertext = data[20:]
    computed = _tag(raw_key, nonce, ciphertext)
    if tag != computed:
        return None  # invalid key
    return bytes(a ^ b for a, b in zip(ciphertext, _stream(raw_key, nonce, len(ciphertext))))

# Try many key interpretations
prefix = "SSSH-VAULT-"
after = KEY_TXT[len(prefix):]
after_noX = after.rstrip("X")

candidates = {
    "full_str": KEY_TXT.encode(),
    "after_prefix": after.encode(),
    "after_noX": after_noX.encode(),
    "sha256_full": hashlib.sha256(KEY_TXT.encode()).digest(),
    "sha256_after": hashlib.sha256(after.encode()).digest(),
    "md5_full": hashlib.md5(KEY_TXT.encode()).digest(),
    "md5_after": hashlib.md5(after.encode()).digest(),
}

# try b64 decode of after-prefix part
for suffix in ("", "=", "==", "==="):
    try:
        dec = base64.b64decode(after + suffix)
        candidates[f"b64_after({suffix})"] = dec
        candidates[f"sha256_b64_after({suffix})"] = hashlib.sha256(dec).digest()
    except Exception:
        pass
for suffix in ("", "=", "==", "==="):
    try:
        dec = base64.b64decode(after_noX + suffix)
        candidates[f"b64_afterNoX({suffix})"] = dec
        candidates[f"sha256_b64_afterNoX({suffix})"] = hashlib.sha256(dec).digest()
    except Exception:
        pass

data = base64.b64decode(ENC_B64)
print(f"blob total={len(data)}, nonce={data[:16].hex()}, tag={data[16:20].hex()}, ct={data[20:].hex()} ({len(data[20:])} bytes)")

for name, key in candidates.items():
    result = decrypt(ENC_B64, key)
    if result is not None:
        print(f"\n[+] KEY={name} ({len(key)} bytes): {key[:32]}")
        print(f"    Plaintext: {result}")
        m = re.search(rb"PTITCTF\{[^}]+\}", result)
        if m:
            print(f"\n[FLAG] {m.group().decode()}")

print("\n[done] if no [+] shown, all keys gave tag mismatch.")
