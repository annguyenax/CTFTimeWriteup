#!/usr/bin/env python3
import pefile, capstone, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pe = pefile.PE(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\lib\winuxsvc.dll")
img = bytearray(pe.get_memory_mapped_image())
base = pe.OPTIONAL_HEADER.ImageBase
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def dis(va, nins=200, title=""):
    print(f"\n===== {title} {hex(va)} =====")
    off = va - base
    n = 0
    for i in cs.disasm(bytes(img[off:off+0x800]), va):
        print(f"{i.address:08x}  {i.mnemonic:8} {i.op_str}")
        n += 1
        if n >= nins:
            break

# continue WnxService after magic check
dis(0x3665F18D0, 220, "after WUX2 parse")

# find rip-relative loads near flag strings
# search for lea that point to rdata strings around 0x3665f7015
print("\n===== xrefs-ish to flag strings (disp32 in lea) =====")
# scan .text for 48 8d 15 / 48 8d 0d (lea rdx/rcx [rip+disp])
text_va = base + 0x1000
text = bytes(img[0x1000:0x1000+20192])
import struct
targets = {0x3665F7015, 0x3665F701F, 0x3665F70B2, 0x3665F7000, 0x3665F7230}
for i in range(len(text)-7):
    # lea r64, [rip+disp32]  48 8d XX disp32  or 4c 8d
    b0 = text[i]
    if b0 in (0x48, 0x4C) and text[i+1] == 0x8D:
        modrm = text[i+2]
        if (modrm & 0xC7) == 0x05:  # rip rel
            disp = struct.unpack_from("<i", text, i+3)[0]
            insn_va = text_va + i
            absva = insn_va + 7 + disp
            if absva in targets or (0x3665F7000 <= absva <= 0x3665F7300):
                print(f"  {hex(insn_va)} -> {hex(absva)}")
