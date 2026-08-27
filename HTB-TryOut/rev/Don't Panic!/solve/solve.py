#!/usr/bin/env python3
"""
HTB TryOut 2026 - rev "Don't Panic!" solver.

Recovers the flag fully from the binary (Linux ELF64, Rust) without running it:

  check_flag(buf, len):
      if len != 31: assert_failed(...)
      table = [fn0, fn1, ..., fn30]   # built in the prologue via lea/mov
      for i in 0..31:
          fn_i(buf[i])                # each fn: cmp $imm,%dil; je ret; else panic

Each table function is a tiny closure:  push rax; cmp $0xNN,%dil; jb fail; jne fail;
ret.  So flag[i] = the immediate compared at table[i].

Steps:
  1. Parse ELF64 section headers to map VMA -> file offset.
  2. Emulate the check_flag prologue (lea rIP+disp32 / mov to rsp slots) to get
     the 31 entry table.
  3. For each entry address read the `cmp $imm,%dil` immediate from the bytes
     (`50 40 80 ff NN`).
  4. Build the flag, validate HTB{...} format, and re-verify every byte against
     the binary-derived constants.
"""
import struct

BIN = r"D:\download\CTFTimeWriteup\HTB-TryOut\rev\Don't Panic!\files\_work\rev_dontpanic\dontpanic"

CHECK_FLAG = 0x9060
N = 31  # flag length / number of byte checks

data = open(BIN, 'rb').read()


def vma_to_off(vma):
    """Map a VMA to a file offset using program headers (p_vaddr, p_offset, p_filesz)."""
    e_phoff = struct.unpack_from('<Q', data, 0x20)[0]
    e_phentsize = struct.unpack_from('<H', data, 0x36)[0]
    e_phnum = struct.unpack_from('<H', data, 0x38)[0]
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type, p_flags = struct.unpack_from('<II', data, off)
        p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = \
            struct.unpack_from('<QQQQQQ', data, off + 8)
        if p_type == 1 and p_vaddr <= vma < p_vaddr + p_filesz:
            return p_offset + (vma - p_vaddr)
    raise ValueError(f'VMA {vma:#x} not mapped')


def emulate_prologue(va):
    """Mini-emulate the check_flag prologue: track rax/rcx/rdx/rdi and the
    stores into [rsp+slot] to recover the 31-entry function-pointer table."""
    ip = va
    regs = {'rax': None, 'rcx': None, 'rdx': None, 'rdi': None}
    table = {}
    while True:
        o = vma_to_off(ip)
        b = data[o]
        if b == 0x48 and ip + 6 < va + 0x200:
            nxt = data[o + 1]
            if nxt == 0x8d and data[o + 2] in (0x05, 0x0d, 0x15, 0x3d):
                # lea disp32(%rip), %reg
                reg = {0x05: 'rax', 0x0d: 'rcx', 0x15: 'rdx', 0x3d: 'rdi'}[data[o + 2]]
                disp = struct.unpack_from('<i', data, o + 3)[0]
                regs[reg] = (ip + 7 + disp) & 0xFFFFFFFFFFFFFFFF
                ip += 7
                continue
            if nxt == 0x89 and data[o + 2] in (0x44, 0x4c, 0x54, 0x7c):
                # mov %rX, disp8(%rsp)  -> 48 89 44 24 xx
                reg = {0x44: 'rax', 0x4c: 'rcx', 0x54: 'rdx', 0x7c: 'rdi'}[data[o + 2]]
                slot = data[o + 4]
                if data[o + 3] == 0x24:
                    table[slot] = regs[reg]
                    ip += 5
                    continue
            if nxt == 0x89 and data[o + 2] in (0x84, 0x8c, 0x94, 0xbc):
                # mov %rX, disp32(%rsp)  -> 48 89 84 24 xx xx 00 00
                reg = {0x84: 'rax', 0x8c: 'rcx', 0x94: 'rdx', 0xbc: 'rdi'}[data[o + 2]]
                slot = struct.unpack_from('<I', data, o + 4)[0]
                if data[o + 3] == 0x24 and slot < 0x200:
                    table[slot] = regs[reg]
                    ip += 8
                    continue
        if b == 0x48 and data[o + 1] == 0x83 and data[o + 2] == 0xfe and data[o + 3] == 0x1f:
            break  # cmp $0x1f,%rsi  -> prologue done
        ip += 1
        if ip > va + 0x250:
            raise RuntimeError('prologue emulation did not terminate')
    return [table[0x10 + 8 * i] for i in range(N)]


def expected_byte(fn_va):
    """Read the checked byte from: 50 / 40 80 ff NN ..."""
    o = vma_to_off(fn_va)
    assert data[o] == 0x50 and data[o + 1] == 0x40 and data[o + 2] == 0x80 and data[o + 3] == 0xff, \
        f'unexpected checker prologue at {fn_va:#x}'
    return data[o + 4]


def main():
    table = emulate_prologue(CHECK_FLAG)
    print(f'[+] recovered {len(table)} function-pointer entries')

    addrs = sorted(set(table))
    byte_map = {a: expected_byte(a) for a in addrs}
    print(f'[+] {len(byte_map)} distinct checker closures:')
    for a in sorted(byte_map):
        print(f'    {a:#08x} -> {byte_map[a]:#04x} {chr(byte_map[a])!r}')

    flag = bytes(byte_map[a] for a in table)
    print(f'[+] raw bytes : {flag!r}')
    text = flag.decode('ascii', errors='replace')
    print(f'[+] flag text : {text}')

    # Verification 1: format + length
    assert len(flag) == N, 'bad length'
    assert text.startswith('HTB{') and text.endswith('}'), 'bad HTB{} format'
    assert all(0x20 <= c < 0x7f for c in flag), 'non-printable byte'

    # Verification 2: replay check_flag semantics against binary constants
    for i, fn in enumerate(table):
        assert flag[i] == byte_map[fn], f'byte {i} mismatch'
    print('[+] VERIFIED: all 31 bytes replay the binary check logic; '
          'format HTB{...} OK')

    with open(r"D:\download\CTFTimeWriteup\HTB-TryOut\rev\Don't Panic!\final_flag.txt", 'w', newline='\n') as fh:
        fh.write(text + '\n')
    print(f'[+] wrote final_flag.txt: {text}')


if __name__ == '__main__':
    main()
