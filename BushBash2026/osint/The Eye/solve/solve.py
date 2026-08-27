#!/usr/bin/env python3
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# Poem order: Waiti, Waita, Pohutukawa, Hiwa-i-te-rangi,
# Tupu-a-nuku, Ururangi, Waipuna-a-rangi, Tupu-a-rangi.
SEGMENTS = ["F02E", "029F", "2358", "2DC8", "29F0", "3468", "1057", "B7A8"]
EXPECTED = b"bushbash{happy-MAT4RlKI,k1-a-k0E-e-HiW4!}"


def main() -> None:
    ciphertext = (Path(__file__).parent.parent / "the-eye" / "prayer.enc").read_bytes()
    key = bytes.fromhex("".join(SEGMENTS))
    plaintext = unpad(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), AES.block_size)
    start = plaintext.index(b"bushbash{")
    flag = plaintext[start : plaintext.index(b"}", start) + 1]
    assert flag == EXPECTED
    print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    main()
