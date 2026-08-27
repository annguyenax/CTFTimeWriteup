#!/usr/bin/env python3
import pefile, capstone, struct, re, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load(path):
    pe = pefile.PE(path)
    img = bytearray(pe.get_memory_mapped_image())
    base = pe.OPTIONAL_HEADER.ImageBase
    text = None
    for s in pe.sections:
        name = s.Name.split(b"\x00", 1)[0].decode("latin1", "replace")
        print(f"  sect {name:8} va={hex(s.VirtualAddress)} vs={s.Misc_VirtualSize} raw={s.SizeOfRawData}")
        if name == ".text":
            text = (base + s.VirtualAddress, s.Misc_VirtualSize)
    return pe, img, base, text

def disasm_range(img, base, va, size, title):
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs.detail = False
    off = va - base
    print(f"\n===== {title} @ {hex(va)} =====")
    n = 0
    for i in cs.disasm(bytes(img[off:off+size]), va):
        print(f"  {i.address:08x}  {i.mnemonic:8} {i.op_str}")
        n += 1
        if n >= 120:
            print("  ...")
            break

def find_ascii(img, base, needle):
    b = bytes(img)
    hits = []
    start = 0
    nb = needle.encode() if isinstance(needle, str) else needle
    while True:
        i = b.find(nb, start)
        if i < 0:
            break
        hits.append(base + i)
        start = i + 1
    return hits

dll = r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\lib\winuxsvc.dll"
print("DLL", dll)
pe, img, base, text = load(dll)
print("imagebase", hex(base), "mapped", len(img))
print("WnxService rva", hex(pe.DIRECTORY_ENTRY_EXPORT.symbols[0].address), "abs", hex(base+pe.DIRECTORY_ENTRY_EXPORT.symbols[0].address))

for s in ["flag.txt", "corrupted package key", "real_password", "license.db", "WUX2", "winux_policy", "cookie:v2", "char:v3"]:
    hs = find_ascii(img, base, s)
    print("str", repr(s), [hex(x) for x in hs])

# xref-ish: search lea/rip relative later; first disasm export
exp = base + pe.DIRECTORY_ENTRY_EXPORT.symbols[0].address
disasm_range(img, base, exp, 0x400, "WnxService")
