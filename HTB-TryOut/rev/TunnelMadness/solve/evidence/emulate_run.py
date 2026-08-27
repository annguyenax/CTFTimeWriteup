# Emulate the tunnel ELF's main() with unicorn to verify that a given
# direction sequence reaches the exit (success puts at 0x157c).
# libc calls are hooked: scanf feeds from input string, puts/putchar/printf no-op,
# fopen -> NULL (no /flag.txt offline), exit stops emulation.
import struct
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (UC_X86_REG_RIP, UC_X86_REG_RSP, UC_X86_REG_RDI,
                               UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RSI)

BIN = r'D:\download\CTFTimeWriteup\HTB-TryOut\rev\TunnelMadness\files\_work\rev_tunnelmadness\tunnel'
data = open(BIN, 'rb').read()

LOAD = 0x0              # map at base 0 so VA == file offset (PIE base 0)
STACK = 0x7ffff000
STACK_SIZE = 0x10000

mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(LOAD, 0x24000)
mu.mem_write(LOAD, data[:0x24000])
mu.mem_map(STACK, STACK_SIZE)
mu.mem_map(0x600000, 0x20000)
# __ctype_toupper_loc returns int** -> store table pointer at 0x610000
mu.mem_write(0x610000, struct.pack('<Q', 0x610100))
for i in range(256):
    v = i - 0x20 if 0x61 <= i <= 0x7a else i
    mu.mem_write(0x610100 + i * 4, struct.pack('<I', v))

H_scanf = 0x10a0
H_putchar = 0x1040
H_puts = 0x1050
H_printf = 0x1070
H_fopen = 0x1090
H_fgets = 0x1080
H_fclose = 0x1060
H_exit = 0x10b0
H_toupper = 0x1030

input_buf = bytearray()
input_idx = [0]
success_flag = [False]

def popret(uc):
    sp = uc.reg_read(UC_X86_REG_RSP)
    ra = struct.unpack('<Q', uc.mem_read(sp, 8))[0]
    uc.reg_write(UC_X86_REG_RSP, sp + 8)
    return ra

def hook_code(uc, address, size, user_data):
    if address == H_scanf:
        if input_idx[0] < len(input_buf):
            c = input_buf[input_idx[0]]
            input_idx[0] += 1
            uc.mem_write(uc.reg_read(UC_X86_REG_RSI), bytes([c]))
            uc.reg_write(UC_X86_REG_RAX, 1)
        else:
            uc.reg_write(UC_X86_REG_RAX, 0)
        uc.reg_write(UC_X86_REG_RIP, popret(uc))
    elif address == H_toupper:
        uc.reg_write(UC_X86_REG_RAX, 0x610000)
        uc.reg_write(UC_X86_REG_RIP, popret(uc))
    elif address == H_puts:
        rdi = uc.reg_read(UC_X86_REG_RDI)
        s = b''
        try:
            p = rdi
            while True:
                b = uc.mem_read(p, 1)[0]
                if b == 0:
                    break
                s += bytes([b]); p += 1
        except Exception:
            pass
        if b'break into the vault' in s:
            success_flag[0] = True
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.reg_write(UC_X86_REG_RIP, popret(uc))
    elif address in (H_putchar, H_printf, H_fopen, H_fgets, H_fclose):
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.reg_write(UC_X86_REG_RIP, popret(uc))
    elif address == H_exit:
        uc.emu_stop()
    elif address == 0x157c:
        # reached only if current cell value == 3 (exit cell)
        success_flag[0] = True
    elif address == 0x159c:
        uc.emu_stop()

mu.hook_add(UC_HOOK_CODE, hook_code)

def run(moves):
    global input_buf
    input_buf = bytearray((moves + 'Q').encode())
    input_idx[0] = 0
    success_flag[0] = False
    mu.reg_write(UC_X86_REG_RSP, STACK + STACK_SIZE - 0x10)
    mu.reg_write(UC_X86_REG_RIP, 0x1538)
    mu.reg_write(UC_X86_REG_RBX, 0)
    try:
        mu.emu_start(0x1538, 0, count=0, timeout=0)
    except Exception:
        pass
    return success_flag[0]

shortest = 'UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR'
hamilton = 'UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRFRBDRURRFRR'
for name, p in [('corrected-shortest(59)', shortest), ('hamiltonian(63)', hamilton), ('bad(10x U)', 'U' * 10)]:
    print(name, '-> reaches exit:', run(p))
