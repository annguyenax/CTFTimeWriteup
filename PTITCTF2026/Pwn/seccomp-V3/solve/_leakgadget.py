#!/usr/bin/env python3
from capstone import *
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\files\_ex\public\chall"
data=open(B,"rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
# find gadgets in text that set rdi from rbp/r14/rsi/rsp and call puts(0x1150/0x1154) or ret
import re
# scan for call 0x1150 (puts) and check preceding rdi setup
print("=== puts call sites & rdi setup ===")
for off in range(0x1000,0x2000):
    insns=list(md.disasm(data[off:off+20],off))
    for i in range(len(insns)):
        ins=insns[i]
        if ins.mnemonic=='call' and ('0x1150' in ins.op_str or '0x1154' in ins.op_str):
            # look back 3 insns for rdi setup
            ctx=[f"{x.mnemonic} {x.op_str}".strip() for x in insns[max(0,i-3):i+1]]
            print(f"0x{ins.address:#x}: {' ; '.join(ctx)}")
# search for mov rdi, rbp / mov rdi, r14 / lea rdi,[rbp/r14/rsp]
print("\n=== rdi from rbp/r14/rsi/rsp ===")
for off in range(0x1000,0x2000):
    insns=list(md.disasm(data[off:off+12],off))
    for ins in insns:
        t=f"{ins.mnemonic} {ins.op_str}".strip()
        if t.startswith("mov rdi") and any(r in t for r in ["rbp","r14","rsi","r15","rsp","r13"]):
            print(f"0x{ins.address:#x}: {t}")
        if t.startswith("lea rdi, [") and any(r in t for r in ["rbp","r14","rsi","rsp","r13","r15"]):
            print(f"0x{ins.address:#x}: {t}")
