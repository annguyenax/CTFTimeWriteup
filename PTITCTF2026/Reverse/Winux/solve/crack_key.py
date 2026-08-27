#!/usr/bin/env python3
import pefile, struct, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pe = pefile.PE(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\lib\winuxsvc.dll")
img = bytearray(pe.get_memory_mapped_image())
base = pe.OPTIONAL_HEADER.ImageBase

def at(va, n):
    return bytes(img[va - base : va - base + n])

iv = at(0x3665F81A0, 32)
print("IV", iv.hex())
print("SHA256 IV?", iv[:4].hex())

xor_pad = at(0x3665F7F40, 64)
salts = at(0x3665F7B40, 64 * 16)
hashes = at(0x3665F7340, 64 * 32)

prefix = b"winux:char:v3"
print("prefix len", len(prefix))

key = bytearray(64)
for i in range(64):
    salt = salts[i * 16 : (i + 1) * 16]
    expect = hashes[i * 32 : (i + 1) * 32]
    found = None
    for c in range(256):
        xored = c ^ xor_pad[i]
        h = hashlib.sha256(prefix + struct.pack("<I", i) + salt + bytes([xored])).digest()
        if h == expect:
            found = c
            break
    if found is None:
        print("FAIL pos", i)
        # try without xor
        for c in range(256):
            h = hashlib.sha256(prefix + struct.pack("<I", i) + salt + bytes([c])).digest()
            if h == expect:
                print("  matched raw", c, chr(c) if 32 <= c < 127 else "?")
                found = c ^ xor_pad[i]  # maybe
                break
        if found is None:
            key[i] = ord("?")
            continue
    key[i] = found
    ch = chr(found) if 32 <= found < 127 else "?"
    print(i, hex(found), ch)

print("KEY", bytes(key))
print("KEY ascii", bytes(key).decode("latin1", "replace"))
open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\solve\package_key.txt", "w").write(bytes(key).decode("latin1", "replace") + "\n")
