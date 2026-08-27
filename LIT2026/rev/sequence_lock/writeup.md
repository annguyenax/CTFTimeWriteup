# sequence_lock

## Overview
A binary that checks if our input (inside the `LITCTF{}` format) is correct. The inner flag has a length of 20 bytes.

## Analysis
The binary loops over the 20 bytes of our input. For each byte at index `i`, it calculates the `i`-th element of a Fibonacci-like sequence in a 32-bit register `ecx`. 
It then adds our input byte to `cl` (the lowest 8 bits of `ecx`), and XORs the entire 32-bit `ecx` into an accumulator register `r9d` (which starts at `0xffffffaa`).
Finally, it compares the lowest byte of the accumulator `r9b` with a hardcoded target byte array at `0x2140` in `.rodata`.

Since the update is just:
`r9b_new = r9b_prev ^ cl_new`
`cl_new = (Fib(i) & 0xff) + input[i]`
and we check if `r9b_new == target[i]`, we can reverse this step-by-step. 
Knowing `r9b_prev` and `target[i]`, we can compute `cl_new`. Then `input[i] = cl_new - (Fib(i) & 0xff)`. We can then update the full 32-bit `r9d` accumulator and proceed to the next byte.

## Solution
We dump the 20 target bytes from `0x2140` and write a short python script to reverse the check byte-by-byte.

```python
target_bytes = [205, 255, 155, 233, 154, 166, 214, 174, 37, 179, 15, 247, 234, 64, 144, 222, 66, 60, 245, 17]

r9d = 0xffffffaa

flag = []
for i in range(20):
    edx = 0
    eax = 1
    esi = 1
    ecx = 1
    while edx != i:
        ecx = eax
        eax = (eax + esi) & 0xffffffff
        edx += 1
        esi = ecx
        
    fib_val = ecx
    cl_new = target_bytes[i] ^ (r9d & 0xff)
    input_char = (cl_new - (fib_val & 0xff)) % 256
    flag.append(input_char)
    
    ecx_new = (fib_val & 0xffffff00) | cl_new
    r9d = (r9d ^ ecx_new) & 0xffffffff
    
print("Flag: LITCTF{" + bytes(flag).decode() + "}")
```

**Flag:** `LITCTF{f1bon4cci_ch41ns_ftw}`
