#!/usr/bin/env python3
import struct
from pathlib import Path
import capstone

so = Path(
    r"D:\download\ctf-scratch\ptitctf2026_phonefarm\apk_extract\lib\arm64-v8a\libOctopus.so"
).read_bytes()
e_phoff = struct.unpack_from("<Q", so, 0x20)[0]
e_phentsize = struct.unpack_from("<H", so, 0x36)[0]
e_phnum = struct.unpack_from("<H", so, 0x38)[0]
loads = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type = struct.unpack_from("<I", so, o)[0]
    if p_type != 1:
        continue
    p_offset = struct.unpack_from("<Q", so, o + 8)[0]
    p_vaddr = struct.unpack_from("<Q", so, o + 0x10)[0]
    p_filesz = struct.unpack_from("<Q", so, o + 0x20)[0]
    loads.append((p_offset, p_vaddr, p_filesz))


def va_to_off(va):
    for off, vaddr, fsz in loads:
        if vaddr <= va < vaddr + fsz:
            return off + (va - vaddr)
    raise ValueError(hex(va))


md = capstone.Cs(capstone.CS_ARCH_AARCH64, capstone.CS_MODE_ARM)
addr = 0x147A0
off = va_to_off(addr)
code = so[off : off + 0x400]
print("==== changeDevice ====")
for ins in md.disasm(code, addr):
    print(f"{ins.address:08x}  {ins.mnemonic:8s} {ins.op_str}")
    if ins.address > addr + 0x3C0:
        break
