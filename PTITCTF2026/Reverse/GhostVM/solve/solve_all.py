#!/usr/bin/env python3
"""Self-contained GhostVM solver."""
from __future__ import annotations

import pefile

BIN = r"D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe"
GOLDEN = 0x9E3779B97F4A7C15
M1 = 0xBF58476D1CE4E5B9
M2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF
KXOR = 0xA0761D6478BD642F
MUL1 = 0xD6E8FEB86659FD93
MUL2 = 0x9FB21C651E98DF25
SPREAD = 0x0101010101010101


def ks_byte(pc: int, seed: int) -> int:
    x = ((pc * GOLDEN + seed) & MASK64) ^ ((pc << 32) & MASK64)
    x ^= x >> 30
    x = (x * M1) & MASK64
    x ^= x >> 27
    x = (x * M2) & MASK64
    x ^= x >> 31
    return (x ^ (x >> 8) ^ (x >> 24) ^ (x >> 40)) & 0xFF


def rotl8(v: int, n: int) -> int:
    n &= 7
    v &= 0xFF
    if n == 0:
        return v
    return ((v << n) | (v >> (8 - n))) & 0xFF


def rol64(v: int, n: int) -> int:
    n &= 63
    v &= MASK64
    if n == 0:
        return v
    return ((v << n) | (v >> (64 - n))) & MASK64


def ror64(v: int, n: int) -> int:
    n &= 63
    v &= MASK64
    if n == 0:
        return v
    return ((v >> n) | (v << (64 - n))) & MASK64


def decode_op(b: int, t1: bytes, t2: bytes) -> int:
    return (t1[b] ^ rotl8(t2[b], b & 7) ^ 0xA5) & 0xFF


class Stream:
    def __init__(self, code: bytes, seed: int):
        self.code = code
        self.seed = seed
        self.pc = 0
        self.eof = False

    def fetch(self) -> int:
        if self.pc >= len(self.code):
            self.eof = True
            return 0
        b = self.code[self.pc] ^ ks_byte(self.pc, self.seed)
        self.pc += 1
        return b

    def fetch_u64(self) -> int:
        v = 0
        for i in range(8):
            v |= self.fetch() << (8 * i)
        return v

    def fetch_i32(self) -> int:
        v = 0
        for i in range(4):
            v |= self.fetch() << (8 * i)
        if v & 0x80000000:
            v -= 0x100000000
        return v


def mix64(x: int) -> int:
    x &= MASK64
    x ^= x >> 30
    x = (x * M1) & MASK64
    x ^= x >> 27
    x = (x * M2) & MASK64
    x ^= x >> 31
    return x


def make_perm() -> bytes:
    buf = list(range(256))
    r9 = 0x91C7A2D4E6385B0F
    r11 = 0x2545F4914F6CDD1D
    for r10 in range(255, 0, -1):
        r8 = buf[r10]
        rax = (r9 >> 12) ^ r9
        rcx = ((rax << 25) ^ rax) & MASK64
        r9 = ((rcx >> 27) ^ rcx) & MASK64
        rax = (r9 * r11) & MASK64
        rdx = rax % (r10 + 1)
        buf[r10] = buf[rdx]
        buf[rdx] = r8
    return bytes(buf)


def run_vm1(pe_data: bytes) -> bytearray:
    t1 = pe_data[0x9280 : 0x9280 + 256]
    t2 = pe_data[0x9380 : 0x9380 + 256]
    code = pe_data[0x73A0 : 0x73A0 + 0x74]
    rom = pe_data[0x7420 : 0x7420 + 0x1E5C]
    seed = 0xD00DFEED11223344
    mem = bytearray(0x1E5C)
    regs = [0] * 8
    st = Stream(code, seed)
    flag = 0
    steps = 2_000_000
    halted = False
    while steps > 0 and not halted and not st.eof:
        steps -= 1
        raw = st.fetch()
        op = decode_op(raw, t1, t2)
        if op > 17:
            break
        if op == 1:
            dst = st.fetch()
            imm = st.fetch_u64()
            if dst < 8:
                regs[dst] = imm
        elif op == 2:
            dst, src = st.fetch(), st.fetch()
            if dst < 8 and src < 8:
                regs[dst] = regs[src]
        elif op == 3:
            dst, src = st.fetch(), st.fetch()
            idx = regs[src]
            if dst < 8 and idx < 0x1E5C:
                regs[dst] = rom[idx]
        elif op == 4:
            dst, src = st.fetch(), st.fetch()
            addr = regs[dst]
            if addr < len(mem):
                mem[addr] = regs[src] & 0xFF
        elif op == 5:
            dst, src = st.fetch(), st.fetch()
            regs[dst] = (regs[dst] ^ regs[src]) & MASK64
        elif op == 6:
            dst, src = st.fetch(), st.fetch()
            lo = (regs[dst] ^ regs[src]) & 0xFF
            regs[dst] = (regs[dst] & ~0xFF) | lo
        elif op == 7:
            dst, src = st.fetch(), st.fetch()
            regs[dst] = (regs[dst] + regs[src]) & MASK64
        elif op == 8:
            dst, src = st.fetch(), st.fetch()
            regs[dst] = (regs[dst] + (regs[src] & 0xFF)) & MASK64
        elif op == 9:
            dst = st.fetch()
            regs[dst] = (regs[dst] + st.fetch_u64()) & MASK64
        elif op == 10:
            dst = st.fetch()
            regs[dst] = (regs[dst] * st.fetch_u64()) & MASK64
        elif op == 11:
            dst, amt = st.fetch(), st.fetch()
            regs[dst] = rol64(regs[dst], amt)
        elif op == 12:
            dst = st.fetch()
            regs[dst] = mix64(regs[dst])
        elif op == 13:
            dst = st.fetch()
            regs[dst] = (regs[dst] + 1) & MASK64
        elif op == 14:
            dst, src = st.fetch(), st.fetch()
            flag = int(regs[dst] < regs[src])
        elif op == 15:
            rel = st.fetch_i32()
            if flag:
                st.pc += rel
        elif op == 16:
            rel = st.fetch_i32()
            st.pc += rel
        elif op == 17:
            halted = True
    return mem


def run_vm2(mem, flag, t1, t2, sbox, dump_at=None):
    st = Stream(mem, 0x0BADC0FFEE0DDF00)
    regs = [0] * 16
    zf = 0
    halted = False
    success = False
    steps = 4_000_000
    dumped = None
    while steps > 0 and not halted and not st.eof:
        steps -= 1
        pc0 = st.pc
        if dump_at is not None and pc0 == dump_at:
            dumped = list(regs)
        raw = st.fetch()
        op = decode_op(raw, t1, t2)
        if op == 1:
            d = st.fetch()
            regs[d] = st.fetch_u64()
        elif op == 2:
            d, s = st.fetch(), st.fetch()
            regs[d] = regs[s]
        elif op == 3:
            d, idx = st.fetch(), st.fetch()
            regs[d] = flag[idx]
        elif op == 4:
            d, s = st.fetch(), st.fetch()
            regs[d] ^= regs[s]
            regs[d] &= MASK64
        elif op == 5:
            d = st.fetch()
            regs[d] ^= st.fetch_u64()
            regs[d] &= MASK64
        elif op == 6:
            d, s = st.fetch(), st.fetch()
            regs[d] = (regs[d] + regs[s]) & MASK64
        elif op == 7:
            d = st.fetch()
            regs[d] = (regs[d] + st.fetch_u64()) & MASK64
        elif op == 8:
            d, s = st.fetch(), st.fetch()
            regs[d] = (regs[d] - regs[s]) & MASK64
        elif op == 9:
            d, s = st.fetch(), st.fetch()
            regs[d] = (regs[d] * regs[s]) & MASK64
        elif op == 10:
            d = st.fetch()
            regs[d] = (regs[d] * st.fetch_u64()) & MASK64
        elif op == 11:
            d, amt = st.fetch(), st.fetch()
            regs[d] = rol64(regs[d], amt)
        elif op == 12:
            d, amt = st.fetch(), st.fetch()
            regs[d] = ror64(regs[d], amt)
        elif op == 13:
            d, s = st.fetch(), st.fetch()
            regs[d] = rol64(regs[d], regs[s])
        elif op == 14:
            d, amt = st.fetch(), st.fetch()
            regs[d] = (regs[d] >> (amt & 63)) & MASK64 if amt < 64 else 0
        elif op == 15:
            d, amt = st.fetch(), st.fetch()
            regs[d] = (regs[d] << amt) & MASK64 if amt < 64 else 0
        elif op == 16:
            d = st.fetch()
            regs[d] &= st.fetch_u64()
        elif op == 17:
            d, s = st.fetch(), st.fetch()
            regs[d] |= regs[s]
            regs[d] &= MASK64
        elif op == 18:
            d, s, sh, sl = st.fetch(), st.fetch(), st.fetch(), st.fetch()
            tmp = (regs[s] >> sh) & 0xFF
            regs[d] ^= (sbox[tmp] << sl) & MASK64
            regs[d] &= MASK64
        elif op == 19:
            d, s, sh = st.fetch(), st.fetch(), st.fetch()
            tmp = (regs[s] >> sh) & 0xFF
            regs[d] = sbox[tmp]
        elif op == 20:
            d, s = st.fetch(), st.fetch()
            zf = int(regs[d] == regs[s])
        elif op == 21:
            d, s = st.fetch(), st.fetch()
            zf = int(regs[d] != regs[s])
        elif op == 22:
            rel = st.fetch_i32()
            if zf:
                st.pc += rel
        elif op == 23:
            rel = st.fetch_i32()
            if not zf:
                st.pc += rel
        elif op == 24:
            rel = st.fetch_i32()
            st.pc += rel
        elif op == 25:
            d, s = st.fetch(), st.fetch()
            regs[d], regs[s] = regs[s], regs[d]
        elif op == 26:
            d = st.fetch()
            regs[d] = (~regs[d]) & MASK64
        elif op == 27:
            d, s = st.fetch(), st.fetch()
            if zf:
                regs[d] = regs[s]
        elif op == 28:
            halted = True
            success = True
        elif op == 29:
            halted = True
            success = False
        elif op == 30:
            raise RuntimeError(f"mix at {pc0:#x}")
        elif op > 30:
            raise RuntimeError(f"bad op {op} at {pc0:#x}")
    return success, regs, st.pc, dumped


# packing from disasm
PACK = [
    (0, 0, 19, 0x56),
    (0, 8, 2, 0xB6),
    (0, 16, 25, 0x38),
    (0, 24, 7, 0xC9),
    (0, 32, 14, 0x08),
    (0, 40, 30, 0xC4),
    (0, 48, 4, 0xA5),
    (0, 56, 22, 0x24),
    (1, 0, 1, 0xD2),
    (1, 8, 17, 0x79),
    (1, 16, 28, 0xFB),
    (1, 24, 11, 0x47),
    (1, 32, 5, 0x39),
    (1, 40, 24, 0x9E),
    (1, 48, 9, 0xD5),
    (1, 56, 31, 0x09),
    (2, 0, 13, 0xC3),
    (2, 8, 0, 0x63),
    (2, 16, 21, 0x2B),
    (2, 24, 6, 0xC7),
    (2, 32, 27, 0xA4),
    (2, 40, 16, 0x78),
    (2, 48, 3, 0x2E),
    (2, 56, 18, 0xC7),
    (3, 0, 29, 0x19),
    (3, 8, 10, 0xDD),
    (3, 16, 23, 0x14),
    (3, 24, 15, 0xD8),
    (3, 32, 8, 0x00),
    (3, 40, 26, 0x98),
    (3, 48, 12, 0x44),
    (3, 56, 20, 0xCE),
]

# round constants parsed from disasm
ROUNDS = [
    dict(Ca=0xEBFB276A021AA74B, rota=13, Cadda=0x94D049BB133111EB, Cb=0x63EA8774F3294536, rotb=3, Caddb=0x0B50828DD31E8E89),
    dict(Ca=0x2CDE6BFF7B5B8B0B, rota=20, Cadda=0x0AE730026C7B6DFE, Cb=0xE56E5F467DC9DC2A, rotb=10, Caddb=0xA9680D4B2C4B0A9C),
    dict(Ca=0x7145B83B1DB499C3, rota=27, Cadda=0xA8BEBAC9EDA5E9C1, Cb=0x53CA2519FD326188, rotb=53, Caddb=0xF7C19E78D2ABB6D3),
    dict(Ca=0x68ADB30AECE1522F, rota=34, Cadda=0x4E7624976EEE65D4, Cb=0xE51353AF2F73B5F8, rotb=60, Caddb=0x959918C653D432A6),
    dict(Ca=0xFBD3135D334CBA83, rota=41, Cadda=0xEC0DAF5EEE18E1BF, Cb=0xC6203CB2408FB5AB, rotb=31, Caddb=0x8C8EFBA7AE689E5D),
    dict(Ca=0x8623F2D9687D3447, rota=48, Cadda=0x83C529246F457D82, Cb=0x5733B244BD95135E, rotb=38, Caddb=0x2246626D2F951A20),
    dict(Ca=0xB7C755C3CBE1DA65, rota=55, Cadda=0x219C93E3E88FF995, Cb=0xB8AE126342526C30, rotb=17, Caddb=0x4F3FF712ADF58667),
    dict(Ca=0xC4F6871C6032A703, rota=62, Cadda=0xC7541DA968387578, Cb=0x9EB3126F37A42C53, rotb=24, Caddb=0xEEF771D82D3E024A),
    dict(Ca=0xCC1EFBE0BC120891, rota=5, Cadda=0x656B8470E962F143, Cb=0x61D218B2B93FCB6E, rotb=11, Caddb=0x3914B4D1D6EAAF51),
    dict(Ca=0x9F930AD7342F1A15, rota=12, Cadda=0x1B230E3E6AAF4D56, Cb=0x29180E6CF0580327, rotb=18, Caddb=0xDF2C3E9F56172B24),
    dict(Ca=0xE0375B0E4D2EE789, rota=19, Cadda=0xBAFA8885EBD9C939, Cb=0xD34D1BF42909DA9F, rotb=61, Caddb=0xE586404CD477D77B),
    dict(Ca=0x12F543ADB83322F6, rota=26, Cadda=0x58B273436B02450C, Cb=0x62762FA4FEE94A2C, rotb=4, Caddb=0x9B5DCA0A55A0534E),
    dict(Ca=0x7E00CCB468B24426, rota=33, Cadda=0xFE49FD0AE44CC117, Cb=0xC5DBB135ABEA0CF8, rotb=39, Caddb=0xB272ADEBD034BEE5),
    dict(Ca=0x230FD7ECE3E0F118, rota=40, Cadda=0x9C0167D065F95CFA, Cb=0x3CDE2F30CFD6368D, rotb=46, Caddb=0x500A17B151613AC8),
    dict(Ca=0x69EFF027F00BF12F, rota=47, Cadda=0x33D8E19FE523D8CD, Cb=0x50977F08990043C1, rotb=25, Caddb=0x7EE3B966D741A70F),
    dict(Ca=0x22A704B842AA8FF1, rota=54, Cadda=0xD1906865666C54D0, Cb=0x8A73B90ED0FD8C48, rotb=32, Caddb=0x1CBB232C508A2312),
]

CT = (
    0xFFE472913819FB83,
    0xFF12A1C6DFF42510,
    0xABA41A37D8F557EA,
    0xDF68174149473FC4,
)


def pack_flag(flag: bytes):
    r = [0, 0, 0, 0]
    for word, shift, idx, xorv in PACK:
        r[word] |= ((flag[idx] ^ xorv) & 0xFF) << shift
    return r


def unpack_flag(words):
    flag = [0] * 32
    for word, shift, idx, xorv in PACK:
        flag[idx] = ((words[word] >> shift) & 0xFF) ^ xorv
    return bytes(flag)


def sbox_mix_half(x, other, sbox, xor_c, rot, add_c):
    r = (x ^ xor_c) & MASK64
    r6 = rol64((other ^ KXOR) & MASK64, rot)
    r = (r + r6) & MASK64
    r7 = r
    r ^= (sbox[(r7 >> 0) & 0xFF] << 56) & MASK64
    r ^= (sbox[(r7 >> 16) & 0xFF] << 32) & MASK64
    r ^= (sbox[(r7 >> 40) & 0xFF] << 8) & MASK64
    r8 = (sbox[(other >> 24) & 0xFF] * SPREAD) & MASK64
    r = (r + r8) & MASK64
    r = (r * MUL1) & MASK64
    r6 = (r + other) & MASK64
    r8 = ((r >> 58) & 0x1F) + 5
    r6 = rol64(r6, r8)
    r ^= r6
    r = (r + add_c) & MASK64
    r ^= r >> 23
    r = (r * MUL2) & MASK64
    r ^= r >> 29
    r = (r + rol64(other, 17)) & MASK64
    r ^= r >> 32
    return r & MASK64


def F(r2, r3, rnd, sbox):
    r4 = sbox_mix_half(r2, r3, sbox, rnd["Ca"], rnd["rota"], rnd["Cadda"])
    r5 = sbox_mix_half(r3, r2, sbox, rnd["Cb"], rnd["rotb"], rnd["Caddb"])
    return r4, r5


def feistel_forward(r0, r1, r2, r3, sbox):
    for rnd in ROUNDS:
        r4, r5 = F(r2, r3, rnd, sbox)
        r10 = r0 ^ r4
        r11 = r1 ^ r5
        r0, r1, r2, r3 = r2, r3, r10, r11
    return r0, r1, r2, r3


def feistel_inverse(r0, r1, r2, r3, sbox):
    for rnd in reversed(ROUNDS):
        L0, L1 = r0, r1
        r4, r5 = F(L0, L1, rnd, sbox)
        r0, r1, r2, r3 = (r2 ^ r4) & MASK64, (r3 ^ r5) & MASK64, L0, L1
    return r0, r1, r2, r3


def main():
    pe = pefile.PE(BIN)
    data = pe.get_memory_mapped_image()
    mem = run_vm1(data)
    t1 = data[0x9480 : 0x9480 + 256]
    t2 = data[0x9580 : 0x9580 + 256]
    sbox = make_perm()
    print("sbox[:16]", sbox[:16].hex())

    flag = (b"PTITCTF{" + b"A" * 23 + b"}")[:32]
    packed = pack_flag(flag)
    print("packed", [hex(x) for x in packed])

    success, regs, pc, dumped = run_vm2(mem, flag, t1, t2, sbox, dump_at=0x312)
    print("emu dump@0x312", None if dumped is None else [hex(x) for x in dumped[:4]])
    print("emu final r0-3", [hex(regs[i]) for i in range(4)], "pc", hex(pc), "success", success)

    fout = feistel_forward(*packed, sbox)
    print("F out", [hex(x) for x in fout])
    print("F vs emu final", list(fout) == [regs[i] for i in range(4)])

    pt = feistel_inverse(*CT, sbox)
    print("inv words", [hex(x) for x in pt])
    rec = unpack_flag(pt)
    print("recovered", rec)
    try:
        print("ascii", rec.decode("ascii"))
    except Exception:
        print("latin1", rec.decode("latin1"))

    # verify recovered through emu
    if all(32 <= b < 127 for b in rec):
        ok, regs2, pc2, _ = run_vm2(mem, rec, t1, t2, sbox)
        print("verify emu success", ok, [hex(regs2[i]) for i in range(4)])


if __name__ == "__main__":
    main()
