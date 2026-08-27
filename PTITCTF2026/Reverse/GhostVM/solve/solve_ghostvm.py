#!/usr/bin/env python3
"""PTITCTF2026 GhostVM — two-stage custom VM."""
from __future__ import annotations

import struct
from pathlib import Path

EXE = Path(r"D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe")
GOLDEN = 0x9E3779B97F4A7C15
SM1 = 0xBF58476D1CE4E5B9
SM2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF
IMAGE_BASE = 0x140000000


def pe_va_to_off(data: bytes):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", data, coff + 2)[0]
    opt = coff + 20
    ohsz = struct.unpack_from("<H", data, coff + 16)[0]
    ib = struct.unpack_from("<Q", data, opt + 24)[0]
    sec_off = opt + ohsz
    sects = []
    for i in range(nsec):
        o = sec_off + i * 40
        vsz, va, rsz, raw = struct.unpack_from("<IIII", data, o + 8)
        sects.append((va, vsz, raw, rsz))

    def va_to_off(va: int) -> int:
        rva = va - ib
        for v, vsz, raw, rsz in sects:
            if v <= rva < v + max(vsz, rsz):
                return raw + (rva - v)
        raise ValueError(hex(va))

    return va_to_off


def splitmix_fold(idx: int, seed: int) -> int:
    rcx = ((idx * GOLDEN + seed) ^ ((idx << 32) & MASK64)) & MASK64
    rax = (rcx ^ (rcx >> 30)) * SM1 & MASK64
    rcx = (rax ^ (rax >> 27)) * SM2 & MASK64
    rdx = (rcx ^ (rcx >> 31)) & MASK64
    return ((rdx >> 40) ^ (rdx >> 24) ^ (rdx >> 8) ^ rdx) & 0xFF


def rotl8(x: int, n: int) -> int:
    n &= 7
    x &= 0xFF
    return x if n == 0 else ((x << n) | (x >> (8 - n))) & 0xFF


def rotl64(x: int, n: int) -> int:
    n &= 63
    x &= MASK64
    return x if n == 0 else ((x << n) | (x >> (64 - n))) & MASK64


def ror64(x: int, n: int) -> int:
    n &= 63
    x &= MASK64
    return x if n == 0 else ((x >> n) | (x << (64 - n))) & MASK64


def mix64(x: int) -> int:
    """splitmix64 avalanche (no increment)."""
    z = x & MASK64
    z = (z ^ (z >> 30)) * SM1 & MASK64
    z = (z ^ (z >> 27)) * SM2 & MASK64
    return (z ^ (z >> 31)) & MASK64


class Stream:
    def __init__(self, blob: bytes, seed: int):
        self.blob = blob
        self.seed = seed
        self.pc = 0
        self.err = False

    def fetch(self) -> int:
        if self.pc >= len(self.blob):
            self.err = True
            return 0
        idx = self.pc
        self.pc += 1
        return (splitmix_fold(idx, self.seed) ^ self.blob[idx]) & 0xFF

    def fetch_i32(self) -> int:
        u = self.fetch() | (self.fetch() << 8) | (self.fetch() << 16) | (self.fetch() << 24)
        return u - 0x100000000 if u >= 0x80000000 else u

    def fetch_u64(self) -> int:
        v = 0
        for i in range(8):
            v |= self.fetch() << (8 * i)
        return v


def decode_op(raw: int, t1: bytes, t2: bytes) -> int:
    return (t1[raw] ^ rotl8(t2[raw], raw & 7)) ^ 0xA5


def make_sbox() -> bytes:
    buf = list(range(256))
    x = 0x91C7A2D4E6385B0F
    for i in range(255, 0, -1):
        x ^= x >> 12
        x &= MASK64
        x ^= (x << 25) & MASK64
        x ^= x >> 27
        x &= MASK64
        rnd = (x * 0x2545F4914F6CDD1D) & MASK64
        j = rnd % (i + 1)
        buf[i], buf[j] = buf[j], buf[i]
    return bytes(buf)


def run_vm1(blob: bytes, t1: bytes, t2: bytes, table: bytes) -> bytearray:
    st = Stream(blob, 0xD00DFEED11223344)
    regs = [0] * 8
    out = bytearray(0x1E5C)
    flag = 0
    steps = 0
    max_steps = 2_000_000
    trace = []
    while steps < max_steps:
        steps += 1
        if st.err or st.pc >= len(blob):
            raise RuntimeError(f"vm1 stream err pc={st.pc} steps={steps}")
        op = decode_op(st.fetch(), t1, t2)
        if op > 17:
            raise RuntimeError(f"vm1 bad op {op} at {st.pc}")
        if op == 0:
            continue
        if op == 1:  # ldi
            r = st.fetch()
            imm = st.fetch_u64()
            if r >= 8:
                raise RuntimeError("r>=8 ldi")
            regs[r] = imm
        elif op == 2:  # mov dst, src
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 mov")
            regs[dst] = regs[src]
        elif op == 3:  # r[dst] = table[r[src]]
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 ld")
            idx = regs[src]
            if idx >= 0x1E5C:
                raise RuntimeError(f"table oob {idx}")
            regs[dst] = table[idx]
        elif op == 4:  # out[r[dst]] = r[src] as byte
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 st")
            idx = regs[dst]
            if idx >= len(out):
                raise RuntimeError(f"out oob {idx}")
            out[idx] = regs[src] & 0xFF
        elif op == 5:  # xor
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 xor")
            regs[dst] = (regs[dst] ^ regs[src]) & MASK64
        elif op == 6:  # xor low byte
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 xorb")
            lo = (regs[dst] ^ (regs[src] & 0xFF)) & 0xFF
            regs[dst] = (regs[dst] & ~0xFF) | lo
        elif op == 7:  # add
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 add")
            regs[dst] = (regs[dst] + regs[src]) & MASK64
        elif op == 8:  # add byte
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 addb")
            regs[dst] = (regs[dst] + (regs[src] & 0xFF)) & MASK64
        elif op == 9:  # addi
            r = st.fetch()
            imm = st.fetch_u64()
            if r >= 8:
                raise RuntimeError("r>=8 addi")
            regs[r] = (regs[r] + imm) & MASK64
        elif op == 10:  # muli
            r = st.fetch()
            imm = st.fetch_u64()
            if r >= 8:
                raise RuntimeError("r>=8 muli")
            regs[r] = (regs[r] * imm) & MASK64
        elif op == 11:  # rol r, imm8
            r = st.fetch()
            n = st.fetch()
            if r >= 8:
                raise RuntimeError("r>=8 rol")
            regs[r] = rotl64(regs[r], n & 0x3F)
        elif op == 12:  # mix64(r)
            r = st.fetch()
            if r >= 8:
                raise RuntimeError("r>=8 mix")
            regs[r] = mix64(regs[r])
        elif op == 13:  # inc
            r = st.fetch()
            if r >= 8:
                raise RuntimeError("r>=8 inc")
            regs[r] = (regs[r] + 1) & MASK64
        elif op == 14:  # setb r[dst] < r[src]
            dst, src = st.fetch(), st.fetch()
            if dst >= 8 or src >= 8:
                raise RuntimeError("r>=8 cmp")
            flag = int(regs[dst] < regs[src])
        elif op == 15:  # jcc (if flag)
            off = st.fetch_i32()
            if flag:
                npc = st.pc + off
                if npc < 0 or npc > len(blob):
                    raise RuntimeError(f"bad jmp {npc}")
                st.pc = npc
        elif op == 16:  # jmp
            off = st.fetch_i32()
            npc = st.pc + off
            if npc < 0 or npc > len(blob):
                raise RuntimeError(f"bad jmp {npc}")
            st.pc = npc
        elif op == 17:  # halt
            break
        if steps <= 40 or op in (4, 15, 16, 17):
            trace.append((steps, st.pc, op, list(regs)))
    print(f"VM1 done steps={steps} pc={st.pc} err={st.err} flag={flag}")
    print("regs", [hex(x) for x in regs])
    return out, trace, steps


def main():
    data = EXE.read_bytes()
    va_to_off = pe_va_to_off(data)

    def read_va(va, n):
        o = va_to_off(va)
        return data[o : o + n]

    t1 = read_va(0x140009280, 256)
    t2 = read_va(0x140009380, 256)
    blob = read_va(0x1400073A0, 0x1E5C)
    table = read_va(0x140007420, 0x1E5C)
    print("t1", t1[:16].hex(), "t2", t2[:16].hex())
    print("blob", blob[:16].hex())
    print("table[0:16]", table[:16].hex())

    names = {
        0: "nop", 1: "ldi", 2: "mov", 3: "ldtab", 4: "stb", 5: "xor",
        6: "xorb", 7: "add", 8: "addb", 9: "addi", 10: "muli", 11: "rol",
        12: "mix", 13: "inc", 14: "setb", 15: "jc", 16: "jmp", 17: "halt",
    }
    st = Stream(blob, 0xD00DFEED11223344)
    print("VM1 disasm (first 80):")
    for i in range(80):
        if st.err or st.pc >= len(blob):
            break
        pc = st.pc
        op = decode_op(st.fetch(), t1, t2)
        name = names.get(op, f"?{op}")
        args = ""
        if op in (1, 9, 10):
            r = st.fetch(); imm = st.fetch_u64(); args = f"r{r}, 0x{imm:x}"
        elif op in (2, 3, 4, 5, 6, 7, 8, 14):
            a, b = st.fetch(), st.fetch(); args = f"r{a}, r{b}"
        elif op == 11:
            r, n = st.fetch(), st.fetch(); args = f"r{r}, {n}"
        elif op in (12, 13):
            r = st.fetch(); args = f"r{r}"
        elif op in (15, 16):
            off = st.fetch_i32(); args = f"{off:+d} -> {st.pc+off}"
        print(f"  {pc:04x}: {name:6s} {args}")
        if op == 17:
            break

    out, trace, steps = run_vm1(blob, t1, t2, table)
    outdir = Path(__file__).resolve().parent
    (outdir / "vm2_bytecode.bin").write_bytes(out)
    print("out entropy-ish unique", len(set(out)), "first32", out[:32].hex())
    print("nonzero", sum(1 for b in out if b), "/", len(out))


if __name__ == "__main__":
    main()
