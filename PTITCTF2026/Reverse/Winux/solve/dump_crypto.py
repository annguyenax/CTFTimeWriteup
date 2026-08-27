#!/usr/bin/env python3
import pefile, capstone, struct, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pe = pefile.PE(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\lib\winuxsvc.dll")
img = bytearray(pe.get_memory_mapped_image())
base = pe.OPTIONAL_HEADER.ImageBase

def dump(va, n, name):
    off = va - base
    b = bytes(img[off:off+n])
    print(f"\n== {name} {hex(va)} len={n}")
    print(b.hex())
    # ascii
    s = "".join(chr(c) if 32 <= c < 127 else "." for c in b[:200])
    print(s)

dump(0x3665F7F40, 64, "xor_pad r12")
dump(0x3665F7B40, 64*16, "r13 table 64x16")
dump(0x3665F7340, 64*32, "hash table 64x32")
dump(0x3665F8060, 64, "xmm const 8060")
dump(0x3665F8070, 64, "xmm const 8070")

# strings at path table
for va in [0x3665F7036, 0x3665F703B, 0x3665F7041, 0x3665F7047, 0x3665F704D, 0x3665F7053, 0x3665F7059, 0x3665F7061]:
    off = va - base
    s = bytes(img[off:off+80]).split(b"\x00", 1)[0]
    print(hex(va), s)

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
print("\n===== hash 0x3665f48a0 =====")
off = 0x3665F48A0 - base
n = 0
for i in cs.disasm(bytes(img[off:off+0x400]), 0x3665F48A0):
    print(f"{i.address:08x}  {i.mnemonic:8} {i.op_str}")
    n += 1
    if n >= 80:
        break
print("\n===== cmp 0x3665f4b90 =====")
off = 0x3665F4B90 - base
n = 0
for i in cs.disasm(bytes(img[off:off+0x80]), 0x3665F4B90):
    print(f"{i.address:08x}  {i.mnemonic:8} {i.op_str}")
    n += 1
    if n >= 30:
        break
