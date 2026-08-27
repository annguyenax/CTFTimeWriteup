#!/usr/bin/env python3
from capstone import *
data=open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\files\_ex\public\chall","rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
seen=set()
for off in range(0x1000,0x2000):
    for ins in md.disasm(data[off:off+12],off):
        t=f"{ins.mnemonic} {ins.op_str}".strip()
        key=(ins.address,t)
        if key in seen: continue
        # lea rdi,[r14/rbp/rsp/rbx/rsi/r13 ...]
        if t.startswith("lea rdi, [") and any(r in t for r in ["r14","rbp","rsp","rbx","rsi","r13"]):
            seen.add(key); print(f"0x{ins.address:#x}: {t}")
        elif t.startswith(("add rdi","sub rdi","add edi","sub edi","mov rdi, r14","mov rdi, rbp","mov rdi, rsp","mov rdi, rsi","mov rdi, r13")):
            seen.add(key); print(f"0x{ins.address:#x}: {t}")
