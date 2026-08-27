#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTB TryOut - "Satellite Hijack" (rev) - solver
================================================

Goal: recover the satellite control codes (the flag HTB{...}).

Binary layout (library.so, x86-64 ELF):
  * The program (`satellite`) reads a line and calls `send_satellite_message(0, input)`.
  * `library.so` is "tampered": the exported `send_satellite_message` (0x25d0) is a stub
    that, if env `SAT_PROD_ENVIRONMENT` is set, calls the unpacker 0x23e3 which
      - mmap()s an RWX page,
      - memcpy()s 0x1000 bytes from .text [0x11a9,0x21a9),
      - memfrob()s it (XOR 42)  -> real code.
  * The real flag-check routine sits at 0x11a9 in the encrypted region. It scans the
    input for the magic "HTB{" and calls the checker at 0x1235.
  * Checker 0x1235 builds a 28-byte key on the stack from four movabs immediates
    (with overlapping writes) and requires:
          key[i] XOR input[i] == i          for i in 0..27
    i.e.  input[i] = key[i] XOR i           (the inner bytes after "HTB{").
    So the full flag is:  "HTB{" + inner + ...  where inner[0..27] = key[i]^i.

This solver reconstructs the key buffer exactly the way the binary builds it
(overlapping stack writes), then derives the inner bytes.
"""

import struct

LIBRARY_PATH = r"..\files\extracted\rev_satellitehijack\library.so"

# ---------------------------------------------------------------------------
# 1) Recover the four movabs immediates straight out of the (decrypted) binary.
#    The checker (0x1235) sits inside the encrypted .text region
#    [0x11a9, 0x21a9).  At runtime the unpacker (0x23e3) memfrob()s that region
#    (XOR with 42).  We replicate the same decryption here, then read the
#    movabs immediates.  In this ELF, .text virtual address == file offset.
# ---------------------------------------------------------------------------
def decrypt_region(data):
    region = data[0x11a9:0x21a9]
    return bytes(b ^ 42 for b in region)


def read_movabs_immediates(path):
    data = open(path, "rb").read()
    dec = decrypt_region(data)
    constants = []
    # movabs instructions live at addresses 0x1235,0x123f,0x1253,0x125d, i.e.
    # at offsets 0x8c,0x96,0xaa,0xb4 inside the decrypted region. Encoding is
    # `48 b8 <imm8>` (REX.W + B8+rd), so imm starts 2 bytes in.
    for vaddr in (0x1235, 0x123f, 0x1253, 0x125d):
        rel = vaddr - 0x11a9
        imm = struct.unpack_from("<Q", dec, rel + 2)[0]
        constants.append(imm)
    return constants


# ---------------------------------------------------------------------------
# 2) Replicate the stack-buffer construction of the checker (0x1235).
#    The buffer lives at rsp-0x28. Four 8-byte writes happen:
#       [rsp-0x28] <- imm0      (offsets 0..7)
#       [rsp-0x20] <- imm1      (offsets 8..15)
#       [rsp-0x1b] <- imm2      (offsets 13..20)  -- overlaps imm1 tail
#       [rsp-0x13] <- imm3      (offsets 21..28)  -- zero pad at 28
# ---------------------------------------------------------------------------
def build_key(imms):
    key = bytearray(32)  # base pointer = index 0
    key[0:8] = struct.pack("<Q", imms[0])
    key[8:16] = struct.pack("<Q", imms[1])
    key[13:21] = struct.pack("<Q", imms[2])
    key[21:29] = struct.pack("<Q", imms[3])
    return bytes(key[:28])  # only bytes 0..27 are used by the check loop


# ---------------------------------------------------------------------------
# 3) Independent re-implementation of the checker to VERIFY the result.
# ---------------------------------------------------------------------------
def check(inner, key):
    for i in range(28):
        if (key[i] ^ inner[i]) != i:
            return False
    return True


def main():
    imms = read_movabs_immediates(LIBRARY_PATH)
    key = build_key(imms)

    inner = bytes(key[i] ^ i for i in range(28))
    flag = b"HTB{" + inner

    print("key   :", key.decode("latin-1"))
    print("inner :", inner.decode("latin-1"))
    print("flag  :", flag.decode())

    # ---- VERIFICATION -----------------------------------------------------
    assert check(inner, key), "checker verification failed!"
    assert flag.startswith(b"HTB{") and flag.endswith(b"}"), "bad flag format"
    assert len(inner) == 28
    print("\n[+] checker re-simulation passed (key[i]^inner[i]==i for i=0..27)")
    print("[+] flag format OK  HTB{...}")

    # Write flag for capture
    with open("final_flag.txt", "w", encoding="utf-8") as f:
        f.write(flag.decode() + "\n")
    print("[+] wrote final_flag.txt")


if __name__ == "__main__":
    main()
