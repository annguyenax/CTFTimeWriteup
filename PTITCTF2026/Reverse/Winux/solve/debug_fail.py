#!/usr/bin/env python3
import pefile, struct, hashlib, itertools, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pe = pefile.PE(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\lib\winuxsvc.dll")
img = bytearray(pe.get_memory_mapped_image())
base = pe.OPTIONAL_HEADER.ImageBase
def at(va, n):
    return bytes(img[va - base : va - base + n])

xor_pad = at(0x3665F7F40, 64)
salts = at(0x3665F7B40, 64 * 16)
hashes = at(0x3665F7340, 64 * 32)
prefix = b"winux:char:v3"

def try_one(i, variants=True):
    salt = salts[i * 16 : (i + 1) * 16]
    expect = hashes[i * 32 : (i + 1) * 32]
    print(f"\n== i={i} expect={expect.hex()} salt={salt.hex()} pad={xor_pad[i]:02x}")
    # verify formula on known
    for c in range(256):
        xored = c ^ xor_pad[i]
        h = hashlib.sha256(prefix + struct.pack("<I", i) + salt + bytes([xored])).digest()
        if h == expect:
            print("  MATCH c", hex(c), chr(c) if 32<=c<127 else "")
            return
    print("  no match standard")
    # variants of input
    cands = []
    for c in range(256):
        xored = bytes([c ^ xor_pad[i]])
        raw = bytes([c])
        blobs = [
            prefix + struct.pack("<I", i) + salt + xored,
            prefix + struct.pack("<I", i) + salt + raw,
            prefix + struct.pack(">I", i) + salt + xored,
            prefix + bytes([i]) + salt + xored,
            prefix + struct.pack("<I", i) + xored + salt,
            prefix + salt + struct.pack("<I", i) + xored,
            b"winux:char:v3\x00" + struct.pack("<I", i) + salt + xored,
            prefix + struct.pack("<Q", i)[:4] + salt + xored,
        ]
        for bi, blob in enumerate(blobs):
            if hashlib.sha256(blob).digest() == expect:
                print("  MATCH variant", bi, "c", hex(c), chr(c) if 32<=c<127 else "")
                return
    # maybe expect is truncated or hash is first 16
    print("  expect nonzero", expect != bytes(32), "last4", expect[-4:].hex())

for i in [0, 7, 59, 60, 61, 62, 63]:
    try_one(i)

print("\nhash table around 59-63:")
for i in range(58, 64):
    print(i, hashes[i*32:(i+1)*32].hex())
