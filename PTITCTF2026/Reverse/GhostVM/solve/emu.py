#!/usr/bin/env python3
"""GhostVM stream decoder + ISA disassembler / emulator."""
from __future__ import annotations

import struct
from pathlib import Path

EXE = Path(r"D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe")
GOLDEN = 0x9E3779B97F4A7C15
SM1 = 0xBF58476D1CE4E5B9
SM2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF

IMAGE_BASE = 0x140000000
BC1_VA = 0x1400073A0  # encrypted VM1 program
BC1_LEN = 0x1E5C
T1_VA = 0x140009480
T2_VA = 0x140009580
SEED1 = 0xD00DFEED11223344
SEED2 = 0x0BADC0FFEE0DDF00


def pe_map(data: bytes):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", data, coff + 2)[0]
    opt = coff + 20
    ohsz = struct.unpack_from("<H", data, coff + 16)[0]
    image_base = struct.unpack_from("<Q", data, opt + 24)[0]
    sec_off = opt + ohsz
    sects = []
    for i in range(nsec):
        o = sec_off + i * 40
        vsz, va, rsz, raw = struct.unpack_from("<IIII", data, o + 8)
        sects.append((va, vsz, raw, rsz))

    def va_to_off(va: int) -> int:
        rva = va - image_base
        for v, vsz, raw, rsz in sects:
            if v <= rva < v + max(vsz, rsz):
                return raw + (rva - v)
        raise ValueError(hex(va))

    return image_base, va_to_off


def splitmix_fold(idx: int, seed: int) -> int:
    rcx = ((idx * GOLDEN + seed) ^ ((idx << 32) & MASK64)) & MASK64
    rax = (rcx ^ (rcx >> 30)) & MASK64
    rax = (rax * SM1) & MASK64
    rcx = (rax ^ (rax >> 27)) & MASK64
    rcx = (rcx * SM2) & MASK64
    rdx = (rcx ^ (rcx >> 31)) & MASK64
    b = ((rdx >> 40) ^ (rdx >> 24) ^ (rdx >> 8) ^ rdx) & 0xFF
    return b


def rotl8(x: int, n: int) -> int:
    n &= 7
    x &= 0xFF
    return ((x << n) | (x >> (8 - n))) & 0xFF if n else x


class Stream:
    def __init__(self, blob: bytes, seed: int, t1: bytes, t2: bytes):
        self.blob = blob
        self.seed = seed
        self.t1 = t1
        self.t2 = t2
        self.pc = 0
        self.err = False

    def fetch(self) -> int:
        if self.pc >= len(self.blob):
            self.err = True
            return 0
        idx = self.pc
        self.pc += 1
        return (splitmix_fold(idx, self.seed) ^ self.blob[idx]) & 0xFF

    def fetch_u32(self) -> int:
        b0, b1, b2, b3 = self.fetch(), self.fetch(), self.fetch(), self.fetch()
        return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

    def fetch_i32(self) -> int:
        u = self.fetch_u32()
        return u - 0x100000000 if u >= 0x80000000 else u

    def fetch_u64(self) -> int:
        v = 0
        for i in range(8):
            v |= self.fetch() << (8 * i)
        return v

    def decode_op(self) -> int:
        raw = self.fetch()
        op = (self.t1[raw] ^ rotl8(self.t2[raw], raw & 7)) ^ 0xA5
        return op & 0xFF


OPNAMES = {
    0: "nop",
    1: "ldi",
    2: "mov",
    3: "ldb_in",
    4: "xor",
    5: "xori",
    6: "add",
    7: "addi",
    8: "sub",
    9: "mul",
    10: "muli",
    11: "rol",
    12: "ror",
    13: "rol2",
    14: "shr",
    15: "shl",
    16: "andi",
    17: "or",
    18: "xor_mem",
    19: "ldb_mem",
    20: "seq",
    21: "sne",
    22: "jnz",
    23: "jz",
    24: "jmp",
    25: "and",
    26: "not",
    27: "cmovz",
    28: "ret1",
    29: "ret0",
    30: "mix",
}


def disasm(blob: bytes, seed: int, t1: bytes, t2: bytes, limit=400):
    st = Stream(blob, seed, t1, t2)
    lines = []
    n = 0
    while st.pc < len(blob) and n < limit and not st.err:
        pc = st.pc
        op = st.decode_op()
        name = OPNAMES.get(op, f"?{op}")
        args = ""
        try:
            if op == 0:
                args = ""
            elif op in (1, 5, 7, 10, 16):
                r = st.fetch()
                imm = st.fetch_u64()
                args = f"r{r}, 0x{imm:x}"
            elif op in (2, 4, 6, 8, 9, 11, 12, 13, 14, 15, 17, 20, 21, 25, 27):
                a, b = st.fetch(), st.fetch()
                args = f"r{a}, r{b}"
            elif op == 3:
                a, b = st.fetch(), st.fetch()
                args = f"r{a}, in[{b}]"
            elif op in (18, 19):
                a, b = st.fetch(), st.fetch()
                extra = st.fetch()
                args = f"r{a}, r{b}, {extra}"
            elif op in (22, 23, 24):
                off = st.fetch_i32()
                args = f"{off:+d} -> {st.pc + off}"
            elif op == 26:
                r = st.fetch()
                args = f"r{r}"
            elif op in (28, 29):
                args = ""
            elif op == 30:
                a, b = st.fetch(), st.fetch()
                imm = st.fetch_u64()
                args = f"r{a}, r{b}, 0x{imm:x}"
            elif op > 30:
                args = f"INVALID {op}"
                st.err = True
            else:
                args = "?"
        except Exception as e:
            args = f"ERR {e}"
            st.err = True
        lines.append((pc, op, name, args, st.pc))
        n += 1
        if op in (28, 29) and n > 5:
            # keep going; program may have multiple
            pass
    return lines, st


def main():
    data = EXE.read_bytes()
    _, va_to_off = pe_map(data)

    def read_va(va, n):
        o = va_to_off(va)
        return data[o : o + n]

    t1 = read_va(T1_VA, 256)
    t2 = read_va(T2_VA, 256)
    blob1 = read_va(BC1_VA, BC1_LEN)

    # dump decrypted VM1 bytes
    dec1 = bytes(splitmix_fold(i, SEED1) ^ blob1[i] for i in range(len(blob1)))
    outdir = Path(__file__).resolve().parent
    (outdir / "vm1_dec.bin").write_bytes(dec1)

    lines, st = disasm(blob1, SEED1, t1, t2, limit=800)
    print(f"VM1 decoded {len(lines)} insns, end_pc={st.pc}/{len(blob1)} err={st.err}")
    opcount = {}
    for pc, op, name, args, npc in lines:
        opcount[name] = opcount.get(name, 0) + 1
        if len(lines) < 200 or op in (22, 23, 24, 28, 29, 3, 18, 19, 30) or pc < 80:
            print(f"  {pc:04x}: {name:8s} {args}")
    print("opcounts", sorted(opcount.items(), key=lambda x: -x[1]))

    # If VM1 is just encrypted VM2 bytecode (not a program), try treating dec1 as raw
    # Check first decoded ops validity
    invalid = sum(1 for _, op, *_ in lines if op > 30)
    print("invalid ops", invalid)


if __name__ == "__main__":
    main()
