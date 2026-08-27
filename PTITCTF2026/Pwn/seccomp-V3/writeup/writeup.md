# seccomp-V3 — Writeup

**Event:** PTIT CTF 2026 · **Category:** Pwn · **Points:** 104/129
**Binary:** `chall` (x86_64 ELF, Ubuntu 22.04 / glibc 2.35)

## TL;DR

Menu option **5) Audit** has a stack overflow caused by a **16-bit truncation**
in the size check (`cmp ax, 0x60`) while `read(0, buf, size)` uses the full
64-bit size. With Full RELRO + NX + PIE and no canary, we:

1. Leak the **PIE base** via a 2-byte partial overwrite of the saved `r12`
   register (which holds the menu string pointer `PIE+0x2101`) so the menu's
   `puts(r12)` prints the `.init_array` entry at `PIE+0x3d40` (= `PIE+0x1c10`).
2. With PIE known, do a classic `puts(GOT.puts)` leak to get **libc**.
3. ROP an ORW chain (binary PLT + libc `pop rdx`) to read `/flag.txt`.

## 1. Vulnerability

`sub_1d10` (menu option 5 "Audit"):

```
sub rsp, 0xa8
lea rbp, [rsp+0x40]          ; note buffer
...
call strtoull                 ; r12 = full 64-bit size
cmp  ax, 0x60                 ; <-- 16-bit compare only
ja   reject
...
syscall(SYS_read, 0, rbp, r12) ; read r12 bytes (64-bit!) into 96-byte buffer
```

Passing `size=65600` (`0x10040`) makes `ax=0x40 ≤ 0x60` pass the check while
the `read` writes 65600 bytes into the stack.

**Stack layout** (buffer base = `rbp = rsp+0x40`):

| offset | contents |
|--------|----------|
| 0x00..0x5f | note buffer (zeroed, 96 B) |
| 0x60..0x67 | padding |
| 0x68 | saved RBP |
| 0x70 | saved R12 |
| 0x78 | return address |

## 2. PIE leak (partial overwrite of saved r12)

`saved r12` = the `" 5) Audit"` string pointer = `PIE + 0x2101`. The menu loop
calls `puts(r12)` every iteration. A **2-byte partial overwrite** of `saved r12`
redirects that `puts` to an arbitrary low-16-bit offset.

> ⚠️ **Critical detail:** a 2-byte overwrite sets `r12 = (PIE & ~0xffff) | X`.
> This equals `PIE + X` **only when the low 16 bits of PIE are 0x0000**, i.e.
> with probability 1/16 (6.25%) under ASLR. Otherwise the high bits of the
> offset are lost and `r12` lands at a wrong/unmapped address (crash).
> The exploit therefore **retries on fresh connections** until the leak is a
> valid page-aligned pointer.

We point `r12` at `PIE+0x3d40`, the `.init_array[0]` entry, which holds the
`R_X86_64_RELATIVE` relocation `PIE+0x1c10`. So:

```
leak = u64(bytes) ; PIE = leak - 0x1c10
```

The menu reprints after the overflow (return address is untouched), so the
process stays alive for the next stages.

## 3. libc leak + ORW (classic)

With PIE known, run a full ROP that calls `puts(GOT.puts)` then returns to
`main`, leaking libc (glibc 2.35: `puts = 0x80e50`). Then an ORW chain using
the binary's PLT and the libc `pop rdx; pop rbx; ret` gadget (`0x904a9`):

```
read(0, bss, 16)      -> "/flag.txt"
open(bss, 0)
read(3, bss+0x30, 0x100)
puts(bss+0x30)
```

No seccomp filter is ever installed (option 3 is never chosen), so open/read/
write/execve all remain allowed.

## 4. Verification

Validated **offline** in the `public-seccomp_v3` Docker container (Ubuntu 22.04,
socat): `local_final.py` prints `PTITCTF{local_test_flag}`. The remote exploit
(`solve_remote.py`) implements the full leak→ORW chain with retries; the flag is
confirmed only by a successful live run (the original instance expired before
capture — renew it and rerun).

## 5. Files

- `solve/solve_remote.py` — remote exploit (retries; needs a live instance)
- `solve/_dbg/local_final.py` — offline proof (uses /proc/pid/maps for PIE)
- `files/_ex/public/` — challenge source artifacts
