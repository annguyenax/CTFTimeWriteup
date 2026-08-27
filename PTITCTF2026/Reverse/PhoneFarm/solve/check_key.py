#!/usr/bin/env python3
import struct
import re
from pathlib import Path

so = Path(
    r"D:\download\ctf-scratch\ptitctf2026_phonefarm\apk_extract\lib\arm64-v8a\libOctopus.so"
).read_bytes()
print("magic", so[:4], "size", len(so))

idx = 0
while True:
    i = so.find(b"hell", idx)
    if i < 0:
        break
    print("hell ascii", hex(i), so[max(0, i - 16) : i + 16])
    idx = i + 1

pat = struct.pack("<I", 0x6C6C6568)
idx = 0
while True:
    i = so.find(pat, idx)
    if i < 0:
        break
    print("u32 hell", hex(i), so[max(0, i - 8) : i + 16].hex())
    idx = i + 1

# ELF dynsym
# e_shoff
e_shoff = struct.unpack_from("<Q", so, 0x28)[0]
e_shentsize = struct.unpack_from("<H", so, 0x3A)[0]
e_shnum = struct.unpack_from("<H", so, 0x3C)[0]
e_shstrndx = struct.unpack_from("<H", so, 0x3E)[0]
print("shoff", hex(e_shoff), "shnum", e_shnum)

shstr_off = e_shoff + e_shstrndx * e_shentsize
shstr_sh_offset = struct.unpack_from("<Q", so, shstr_off + 0x18)[0]
shstr_sh_size = struct.unpack_from("<Q", so, shstr_off + 0x20)[0]
shstr = so[shstr_sh_offset : shstr_sh_offset + shstr_sh_size]

dynstr = dynsym = None
for i in range(e_shnum):
    o = e_shoff + i * e_shentsize
    name_off = struct.unpack_from("<I", so, o)[0]
    name = shstr[name_off:].split(b"\0", 1)[0]
    sh_type = struct.unpack_from("<I", so, o + 4)[0]
    sh_addr = struct.unpack_from("<Q", so, o + 0x10)[0]
    sh_offset = struct.unpack_from("<Q", so, o + 0x18)[0]
    sh_size = struct.unpack_from("<Q", so, o + 0x20)[0]
    if name in (b".dynstr", b".strtab"):
        print(name, hex(sh_offset), hex(sh_size))
    if name == b".dynstr":
        dynstr = so[sh_offset : sh_offset + sh_size]
    if name == b".dynsym":
        dynsym = (sh_offset, sh_size, sh_addr)

if dynstr and dynsym:
    off, sz, _ = dynsym
    entsz = 24
    for i in range(sz // entsz):
        o = off + i * entsz
        st_name = struct.unpack_from("<I", so, o)[0]
        st_value = struct.unpack_from("<Q", so, o + 8)[0]
        name = dynstr[st_name:].split(b"\0", 1)[0]
        if b"change" in name.lower() or b"Key" in name or b"hello" in name.lower() or b"Main" in name:
            print("sym", name, hex(st_value))

# xref Invalid API Key
inv = so.find(b"Invalid API Key")
print("Invalid API Key at", hex(inv))

# capstone around changeDevice if we have address
import capstone

# find ELF exec segments
e_phoff = struct.unpack_from("<Q", so, 0x20)[0]
e_phentsize = struct.unpack_from("<H", so, 0x36)[0]
e_phnum = struct.unpack_from("<H", so, 0x38)[0]
loads = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type = struct.unpack_from("<I", so, o)[0]
    if p_type != 1:
        continue
    p_offset = struct.unpack_from("<Q", so, o + 0x8)[0]
    p_vaddr = struct.unpack_from("<Q", so, o + 0x10)[0]
    p_filesz = struct.unpack_from("<Q", so, o + 0x20)[0]
    loads.append((p_offset, p_vaddr, p_filesz))
    print("LOAD", hex(p_offset), hex(p_vaddr), hex(p_filesz))


def va_to_off(va):
    for off, vaddr, fsz in loads:
        if vaddr <= va < vaddr + fsz:
            return off + (va - vaddr)
    raise ValueError(hex(va))


md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
# subagent said 0x147a0
for addr in (0x147A0, 0x14700, 0x14000):
    try:
        off = va_to_off(addr)
    except Exception:
        continue
    print("==== disasm", hex(addr))
    code = so[off : off + 0x200]
    for ins in md.disasm(code, addr):
        print(hex(ins.address), ins.mnemonic, ins.op_str)
        if ins.address > addr + 0x180:
            break
