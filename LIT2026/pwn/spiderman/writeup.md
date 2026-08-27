# spiderman

## Overview
A simple function pointer overwrite challenge. The binary reads user input into a stack buffer and then calls a function pointer located slightly higher up on the stack.

## Analysis
Looking at the disassembly of `main`:
1. `main` initializes a function pointer at `[rbp-0x10]` to point to the `introduction` function.
2. It calls `gets([rbp-0x30])` to read user input.
3. It then executes `call QWORD PTR [rbp-0x10]`.

Since `gets` is unbounded, we can overflow the buffer at `[rbp-0x30]` and overwrite the function pointer at `[rbp-0x10]`. The distance is `0x30 - 0x10 = 0x20` (32 bytes).

A `win` function exists at `0x4011f6` which prints the flag. We simply overwrite the function pointer with the address of `win`.

## Solution
1. Connect to the service.
2. Wait for the `superhero?` prompt.
3. Send 32 bytes of padding followed by `p64(0x4011f6)` (the address of `win`).
4. `main` will call our injected function pointer instead of `introduction`, printing the flag.

```python
from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31778)
r.recvuntil(b"superhero?")

win = 0x4011f6
payload = b"A" * 0x20 + p64(win)
r.sendline(payload)
print(r.recvall(timeout=2))
```

**Flag:** `LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}`
