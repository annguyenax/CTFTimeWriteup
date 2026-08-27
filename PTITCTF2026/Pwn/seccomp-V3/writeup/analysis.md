# Comprehensive Analysis & Exploitation Guide: seccomp-V3

## 1. Overview & Triage
- **Challenge Name:** `seccomp-V3`
- **Environment:** Ubuntu 22.04 LTS (`glibc 2.35`), x86_64, socat fork
- **Binary Protections:**
  - Full RELRO
  - No Stack Canary (`Canary: Disabled`)
  - NX enabled
  - PIE enabled

## 2. Reverse Engineering Findings & Program Logic

### A. Menu System & Options (`main` @ `0x1240`)
The program provides an interactive Seccomp BPF management and testing interface:
- **0) New:** Loads custom BPF filter instructions (`sock_filter` struct array, max size `0x2000` bytes = 1024 instructions).
- **1) Disasm:** Prints the disassembly of the loaded BPF filter instructions.
- **2) Emulate:** Evaluates the user-supplied syscall number and arguments through an internal BPF emulator (`sub_1c20`).
- **3) Install:** Validates whether the BPF filter allows `SYS_open` (2), `SYS_read` (0), and `SYS_write` (1). If allowed, installs the filter via `prctl(PR_SET_NO_NEW_PRIVS, 1)` and `prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, ...)`.
- **4) Probe:** Probes allowed/blocked status of common syscalls.
- **5) Audit (`sub_1d10`) -> CRITICAL VULNERABILITY:**
  - Asks for `size?` (reads up to `0x60` bytes).
  - Reads `size` bytes into a stack buffer at `[rsp + 0x40]`.
  - **Notice Stack Layout:** The function stack frame allocated is `0xa8` bytes.
  - Since stack canary is **DISABLED**, writing beyond `0x40` bytes allows controlling saved `RBP` and the **Return Address (`RIP`)**!

## 3. Vulnerability Details & BPF Seccomp Bypass

### A. Stack Buffer Overflow in Option 5 (`Audit`)
- Buffer starts at `rsp + 0x40`.
- Return address is located at `rsp + 0xa8`.
- Writing `0x60` bytes gives overwrite control of local variables, and depending on size logic / signedness, lets us hijack control flow directly.

### B. Seccomp Restriction & Architecture Filter Bypass
- `Install` checks whether `open` (2), `read` (0), `write` (1) return `ALLOW` in 64-bit mode.
- We can craft a dual-mode / architecture-aware BPF rule or use standard Open-Read-Write (ORW) shellcode.
- Because `execve` (59) might be filtered or forbidden by seccomp rules, our standard payload will be a pure **ORW (Open-Read-Write) ROP Chain**.

## 4. Exploit Strategy & Step-by-Step Roadmap

### Step 1: Leak Base Addresses (PIE / Libc / Stack)
- Use Option 2 (`Emulate`) or Option 5 (`Audit` uninitialized stack reads / prints) to leak libc / binary PIE base.
- Notice `sub_1d10` performs `write` of the stack buffer without null-terminating if short read or uninitialized memory exists.

### Step 2: Craft Permissive Seccomp Filter
- Load a BPF filter that satisfies the verification check (`open`, `read`, `write` allowed) while keeping architecture flags permissive for our payload.

### Step 3: Trigger Stack Buffer Overflow -> ORW ROP Chain
- Construct ROP chain:
  1. `open("flag", O_RDONLY)` or `openat(AT_FDCWD, "flag", 0)`
  2. `read(fd, bss_addr, 0x100)`
  3. `write(1, bss_addr, 0x100)`
- Send ROP chain via Option 5 (`Audit`).

## 5. Grok Prompt & Solve Script Template
```python
from pwn import *

context.arch = 'amd64'

# Connect
# r = process('./chall')
# r = remote('host', port)

def input_rule(rules):
    r.sendlineafter(b'-1) exit\n', b'0')
    r.sendlineafter(b'1) use examples\n', b'0')
    r.sendlineafter(b'size?\n', str(len(rules)).encode())
    r.sendafter(b'note?\n', rules)

def install():
    r.sendlineafter(b'-1) exit\n', b'3')

def audit(size, payload):
    r.sendlineafter(b'-1) exit\n', b'5')
    r.sendlineafter(b'size?\n', str(size).encode())
    r.sendafter(b'note?\n', payload)
```
