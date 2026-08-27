#!/usr/bin/env python3
"""Full VM2 interpreter for GhostVM inner bytecode."""
import pefile

from emu import (
    MASK64,
    Stream,
    decode_op,
    make_perm,
    rol64,
    ror64,
    run_vm1,
)

BIN = r"D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe"


def run_vm2(mem: bytes, flag: bytes, t1: bytes, t2: bytes, sbox: bytes, verbose=False):
    assert len(flag) == 32
    st = Stream(mem, 0x0BADC0FFEE0DDF00)
    regs = [0] * 16
    zf = 0
    halted = False
    success = False
    steps = 4_000_000
    ops_run = []

    def fetch():
        return st.fetch()

    def fetch_u64():
        return st.fetch_u64()

    def fetch_i32():
        return st.fetch_i32()

    while steps > 0 and not halted and not st.eof:
        steps -= 1
        pc0 = st.pc
        raw = st.fetch()
        op = decode_op(raw, t1, t2)
        if op > 30:
            raise RuntimeError(f"bad op {op} at {pc0:#x}")

        if op in (0,):
            continue
        elif op == 1:
            d = fetch()
            regs[d] = fetch_u64()
        elif op == 2:
            d, s = fetch(), fetch()
            regs[d] = regs[s]
        elif op == 3:
            d, idx = fetch(), fetch()
            if idx >= 32:
                raise RuntimeError("input oob")
            regs[d] = flag[idx]
        elif op == 4:
            d, s = fetch(), fetch()
            regs[d] = (regs[d] ^ regs[s]) & MASK64
        elif op == 5:
            d = fetch()
            regs[d] = (regs[d] ^ fetch_u64()) & MASK64
        elif op == 6:
            d, s = fetch(), fetch()
            regs[d] = (regs[d] + regs[s]) & MASK64
        elif op == 7:
            d = fetch()
            regs[d] = (regs[d] + fetch_u64()) & MASK64
        elif op == 8:
            d, s = fetch(), fetch()
            regs[d] = (regs[d] - regs[s]) & MASK64
        elif op == 9:
            d, s = fetch(), fetch()
            regs[d] = (regs[d] * regs[s]) & MASK64
        elif op == 10:
            d = fetch()
            regs[d] = (regs[d] * fetch_u64()) & MASK64
        elif op == 11:
            d, amt = fetch(), fetch()
            regs[d] = rol64(regs[d], amt)
        elif op == 12:
            d, amt = fetch(), fetch()
            regs[d] = ror64(regs[d], amt)
        elif op == 13:
            d, s = fetch(), fetch()
            regs[d] = rol64(regs[d], regs[s] & 0x3F)
        elif op == 14:
            d, amt = fetch(), fetch()
            if amt >= 64:
                regs[d] = 0
            else:
                regs[d] = (regs[d] >> amt) & MASK64
        elif op == 15:
            d, amt = fetch(), fetch()
            if amt >= 64:
                regs[d] = 0
            else:
                regs[d] = (regs[d] << amt) & MASK64
        elif op == 16:
            d = fetch()
            regs[d] = (regs[d] & fetch_u64()) & MASK64
        elif op == 17:
            d, s = fetch(), fetch()
            regs[d] = (regs[d] | regs[s]) & MASK64
        elif op == 18:
            d, s, sh, sl = fetch(), fetch(), fetch(), fetch()
            tmp = (regs[s] >> sh) & 0xFF
            regs[d] ^= (sbox[tmp] << sl) & MASK64
            regs[d] &= MASK64
        elif op == 19:
            d, s, sh = fetch(), fetch(), fetch()
            tmp = (regs[s] >> sh) & 0xFF
            regs[d] = sbox[tmp]
        elif op == 20:
            d, s = fetch(), fetch()
            zf = int(regs[d] == regs[s])
        elif op == 21:
            d, s = fetch(), fetch()
            zf = int(regs[d] != regs[s])
        elif op == 22:  # JNZ if zf
            rel = fetch_i32()
            if zf:
                st.pc += rel
        elif op == 23:  # JZ if not zf
            rel = fetch_i32()
            if not zf:
                st.pc += rel
        elif op == 24:
            rel = fetch_i32()
            st.pc += rel
        elif op == 25:
            d, s = fetch(), fetch()
            regs[d], regs[s] = regs[s], regs[d]
        elif op == 26:
            d = fetch()
            regs[d] = (~regs[d]) & MASK64
        elif op == 27:
            d, s = fetch(), fetch()
            if zf:
                regs[d] = regs[s]
        elif op == 28:
            halted = True
            success = True
            break
        elif op == 29:
            halted = True
            success = False
            break
        elif op == 30:
            d, src, add = fetch(), fetch(), fetch_u64()
            # wait I had operand order issues. Skip unless used.
            rot = fetch()
            mul = fetch_u64()
            # based on asm: dst first? Let's see if we hit this
            raise RuntimeError(f"MIX used at {pc0:#x}")
        if verbose and pc0 < 0x320:
            ops_run.append((pc0, op, list(regs[:5])))

    return success, regs, st.pc, 4_000_000 - steps, ops_run


def main():
    pe = pefile.PE(BIN)
    data = pe.get_memory_mapped_image()
    mem, _, _ = run_vm1(data)
    t1 = data[0x9480 : 0x9480 + 256]
    t2 = data[0x9580 : 0x9580 + 256]
    sbox = make_perm()
    flag = b"PTITCTF{" + b"A" * 23 + b"}"
    # 32 bytes
    flag = (b"PTITCTF{" + b"A" * 23 + b"}")[:32]
    print("flaglen", len(flag), flag)
    success, regs, pc, steps, _ = run_vm2(mem, flag, t1, t2, sbox)
    print("success", success, "pc", hex(pc), "steps", steps)
    print("r0-r3", [hex(regs[i]) for i in range(4)])
    print("expected ct", hex(0xFFE472913819FB83), hex(0xFF12A1C6DFF42510), hex(0xABA41A37D8F557EA), hex(0xDF68174149473FC4))


if __name__ == "__main__":
    main()
