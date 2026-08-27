#!/usr/bin/env python3
"""Decrypt config.enc from PTITCTF2026 Reverse / Pablo Escobar.

Reconstructs the obfuscated PBKDF2 password from Tool.exe (configkey.Key),
then AES-256-GCM-opens the envelope.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import struct
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

IMAGE_BASE = 0x140000000
TEXT_VA, TEXT_RAW = 0x1000, 0x600
DATA_VA, DATA_RAW = 0x297000, 0x295800

# configkey.Key @ 0x140103660
KEY_FN = 0x140103660
T1_VA = 0x14010369D + 0x194623  # lea rsi, [rip+0x194623]
T2_VA = 0x1401036A8 + 0x1945D8  # lea r8,  [rip+0x1945d8]
KEY_LEN = 0x2C


def va_to_off(va: int) -> int:
    rva = va - IMAGE_BASE
    if rva >= DATA_VA:
        return DATA_RAW + (rva - DATA_VA)
    return TEXT_RAW + (rva - TEXT_VA)


def recover_password(exe: bytes) -> bytes:
    t1 = exe[va_to_off(T1_VA) : va_to_off(T1_VA) + KEY_LEN]
    t2 = exe[va_to_off(T2_VA) : va_to_off(T2_VA) + KEY_LEN]
    out = bytearray(KEY_LEN)
    for i in range(KEY_LEN):
        # rdx = 73*i + 0x5d; then xor with (t1[i] ^ t2[i]); store dl
        rdx = (i + i * 8)
        rdx = (i + rdx * 8) + 0x5D
        out[i] = (rdx ^ (t1[i] ^ t2[i])) & 0xFF
    return bytes(out)


def b64(s: str) -> bytes:
    return base64.b64decode(s + "=" * ((4 - len(s) % 4) % 4))


def decrypt(exe_path: Path, enc_path: Path) -> dict:
    password = recover_password(exe_path.read_bytes())
    env = json.loads(enc_path.read_text(encoding="utf-8"))
    assert env["kdf"] == "pbkdf2-sha256"
    key = hashlib.pbkdf2_hmac(
        "sha256", password, b64(env["salt"]), int(env["iterations"]), dklen=32
    )
    pt = AESGCM(key).decrypt(b64(env["nonce"]), b64(env["ciphertext"]), None)
    return json.loads(pt)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", type=Path, required=True)
    ap.add_argument("--enc", type=Path, required=True)
    args = ap.parse_args()
    cfg = decrypt(args.exe, args.enc)
    print(json.dumps(cfg, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
