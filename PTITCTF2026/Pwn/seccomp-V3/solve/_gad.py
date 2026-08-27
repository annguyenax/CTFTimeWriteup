#!/usr/bin/env python3
from capstone import *
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\files\_ex\public\chall"
data=open(B,"rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
# search for lea rdi,[r14+imm], lea rdi,[rbp+imm], add/sub rdi, lea rdi,[rsi+imm]
for off in range(0x1000,0x2000):
    insns=list(md.disasm(data[off:off+16],off))
    for ins in insns:
        t=f"{ins.mnemonic} {ins.op_str}".strip()
        if t.startswith(("lea rdi, [","add rdi","sub rdi","add edi","sub edi")) and ("r14" in t or "rbp" in t or "rsi" in t or "rdi" in t or "rsp" in t or "rbx" in t):
            print(f"0x{ins.address:#x}: {t}")
