# long_division

## Overview
A simple logic puzzle challenge that asks you to divide two 32-bit signed integers.

## Analysis
The application computes `a / b` using 32-bit signed integers.
In C (and on x86 architecture), a signed integer division `INT_MIN / -1` will cause a hardware exception (Floating Point Exception / `SIGFPE`) because the result (`2147483648`) cannot be represented in a 32-bit signed integer (maximum is `2147483647`).

The application implements a signal handler for `SIGFPE` that prints the flag when this overflow occurs.

## Solution
1. Connect to the service.
2. When prompted for `a =`, input `-2147483648`.
3. When prompted for `b =`, input `-1`.
4. The service throws a signed division overflow and prints the flag.

```python
from pwn import *

r = remote('136.115.87.65', 31777)
r.recvuntil(b"a = ")
r.sendline(b"-2147483648")
r.recvuntil(b"b = ")
r.sendline(b"-1")
print(r.recvall(timeout=2).decode(errors='ignore'))
```

**Flag:** `LITCTF{1nt_div1si0n_0v3rflow}`
