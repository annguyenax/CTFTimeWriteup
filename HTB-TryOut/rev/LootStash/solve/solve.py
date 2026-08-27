#!/usr/bin/env python3
# LootStash (HTB CTF Try Out, rev / very easy) — solver
# The flag is embedded as a plaintext item inside the binary's .rodata
# "loot stack" (a table of item names printed by main). It is recoverable
# by a deterministic string scan + raw-byte verification at a known offset.

import re
import sys
import os

BIN = os.path.join(os.path.dirname(__file__), "..", "files", "_work",
                   "rev_lootstash", "stash")

def main():
    data = open(BIN, "rb").read()

    # 1) String scan for the flag pattern
    candidates = re.findall(rb"HTB\{[^}]+\}", data)
    print(f"[*] HTB{{...}} candidates in binary: {[c.decode() for c in candidates]}")
    assert len(candidates) == 1, "expected exactly one HTB string"

    flag = candidates[0].decode()

    # 2) Independent raw-byte verification: exact match at a fixed offset
    idx = data.find(flag.encode())
    assert idx != -1
    assert data[idx:idx + len(flag)].decode() == flag
    print(f"[*] flag bytes found verbatim at file offset {idx} (0x{idx:x})")

    # 3) Confirm the region is .rodata (ELF section parse, cheap)
    import struct
    shoff = struct.unpack_from("<Q", data, 0x28)[0]
    shentsize = struct.unpack_from("<H", data, 0x3A)[0]
    shnum = struct.unpack_from("<H", data, 0x3C)[0]
    shstrndx = struct.unpack_from("<H", data, 0x3E)[0]
    strtab_off = struct.unpack_from("<Q", data, shoff + shstrndx * shentsize + 0x18)[0]

    def cstr(o):
        e = data.index(b"\x00", o)
        return data[o:e].decode()

    sec = None
    for i in range(shnum):
        base = shoff + i * shentsize
        off = struct.unpack_from("<Q", data, base + 0x18)[0]
        size = struct.unpack_from("<Q", data, base + 0x20)[0]
        if off <= idx < off + size:
            name_off = struct.unpack_from("<I", data, base)[0]
            sec = cstr(strtab_off + name_off)
            break
    print(f"[*] flag resides in section: {sec}")
    assert sec == ".rodata"

    print(f"[+] FLAG: {flag}")
    return flag

if __name__ == "__main__":
    f = main()
    out = os.path.join(os.path.dirname(__file__), "..", "final_flag.txt")
    with open(out, "w") as fh:
        fh.write(f + "\n")
    print(f"[*] wrote {os.path.normpath(out)}")
