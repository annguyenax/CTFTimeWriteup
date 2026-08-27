# Comprehensive Analysis & Exploitation Guide: baby-heap-V2-revenge

## 1. Overview & Triage
- **Challenge Name:** `baby-heap-V2-revenge`
- **Environment:** Ubuntu 22.04 LTS (`glibc 2.35`), x86_64, socat fork
- **Binary Protections:**
  - Full RELRO
  - Stack Canary found
  - NX enabled
  - PIE enabled
- **Heap Limits & Globals:**
  - `slots[8]` at offset `0x4080` (each slot contains `{void *ptr, size_t size}`)
  - Max allocations: 8 chunks concurrently
  - Max size: `0x520` bytes (Fastbin / Tcache / Smallbin range)
  - Allocation counter / Edit counter / Delete counter

## 2. Reverse Engineering Findings & Vulnerability Analysis

### A. Environment & Initialization (`main` @ `0x12c0`)
1. Reads `NOTE_PROFILE` environment variable (if set) and calculates a rolling hash.
2. Opens `/proc/self/maps`, parses the `[heap]` segment line, and stores:
   - `heap_start` @ `0x4070`
   - `heap_end` @ `0x4078`
3. Sets up `SIGALRM` (60 seconds).

### B. Menu Functions & Vulnerabilities
1. **Create (Option 1):**
   - Reads index (0-7), checks `slots[idx].ptr == NULL`.
   - Reads size (must be `> 0` and `<= 0x520`).
   - `malloc(size)`.
   - **Boundary Enforcement:** Validates `heap_start <= chunk_addr` and `chunk_addr + size <= heap_end`. If check fails, `free` and abort.
   - Reads data via `read_input` (`sub_1d00`).
2. **Read (Option 2):**
   - Validates index (0-7), checks `slots[idx].ptr != NULL`.
   - Writes `slots[idx].size` bytes from `slots[idx].ptr` to stdout via `write(1, ptr, size)`.
3. **Edit (Option 3):**
   - Checks global edit counter.
   - Validates index and `slots[idx].ptr != NULL`.
   - Reads new data into `slots[idx].ptr` up to `slots[idx].size`.
   - **Boundary Check on Edit:** Validates destination address is within `[heap_start, heap_end]`.
4. **Delete (Option 4) -> CRITICAL VULNERABILITY:**
   - Validates index (0-7).
   - Retrieves `rdi = slots[idx].ptr`. If not NULL:
     - `free(slots[idx].ptr)`.
     - Decrements delete counter.
     - **BUG:** `slots[idx].ptr` and `slots[idx].size` are **NEVER ZEROED OUT**!
     - **Result:** Pure **Use-After-Free (UAF)** and **Double Free** on all heap slots.

## 3. Exploit Strategy & Roadmap (Glibc 2.35)

### Step 1: Heap Leak (Safe-Linking Bypass)
- Allocate 2 chunks: Chunk A (`0x200`), Chunk B (`0x200`).
- Free Chunk A -> goes into Tcache bin (`0x210`).
- Read Chunk A (Option 2) -> leaks the mangled `next` pointer `P >> 12`.
- `heap_base = (leaked_val) << 12`.

### Step 2: Libc Leak (Smallbin / Unsortedbin)
- Glibc 2.35 allocates `tcache` up to count 7 per bin.
- Fill the tcache list for size `0x420` (alloc 8 chunks, free 7 to fill tcache).
- Free the 8th chunk -> goes into **Unsorted Bin**.
- Read 8th chunk via Option 2 -> leaks `main_arena + 96` (`fd`/`bk` pointers).
- Calculate `libc_base = main_arena_leak - offset`.

### Step 3: Circumventing Heap Bound Check & Arbitrary Write / Code Exec
- In `glibc 2.35`:
  - `__free_hook` and `__malloc_hook` are removed.
  - Target: **FSOP (File Structure OOP)** via `_IO_list_all` / `_IO_2_1_stdout_` or **ROP via `environ` stack leak**.
  - Since edit/create validates heap bounds `[heap_start, heap_end]`, we can:
    1. Leak `environ` pointer in libc to get stack address (using UAF read on a crafted chunk in heap or tcache poisoning within heap).
    2. Overwrite target function pointers, or craft a House of Apple 2 / House of Emma payload on the heap, and trigger `exit()` or `puts()`.
    3. Alternatively, trigger `__environ` read -> calculate return address of `main` / `read_input` on the stack.

## 4. Grok Prompt & Solve Script Template
```python
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# Connect
# r = process('./chall')
# r = remote('host', port)

def create(idx, size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'Index: ', str(idx).encode())
    r.sendlineafter(b'Size: ', str(size).encode())
    r.sendafter(b'Data: ', data)

def read(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'Index: ', str(idx).encode())
    r.recvuntil(b'Data: ')
    return r.recvline()

def edit(idx, data):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'Index: ', str(idx).encode())
    r.sendafter(b'Data: ', data)

def delete(idx):
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b'Index: ', str(idx).encode())
```
