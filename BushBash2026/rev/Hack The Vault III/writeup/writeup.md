# Hack The Vault III — BushBash2026

- **Category:** rev
- **Points:** 350
- **Service:** `34.40.133.67:6002`
- **Flag:** `bushbash{th1rd-times-th3-chArM!}`

## Goal

Third entry in the "Moss Man vault" series. A stripped ELF64 (`vault`,
~14 KB) implements a tiny bookkeeping app with three commands: `write`,
`delete`, `auth`. Goal is to pass `auth` and get `flag.txt` printed.

## Enumeration

- `file`/hex header: ELF64 PIE, x86-64.
- `strings -n 6 vault` shows no plaintext password (unlike Vault I), but
  reveals the command set (`- write`, `- delete`, `- auth`), file names
  (`password.txt`, `flag.txt`), and the tell "Securely storing password in
  memory..." — a hint that the password lives on the heap, not `.rodata`.
- `objdump -d -M intel` (no debug symbols, but `.text` is small enough to
  read fully by hand) reveals a custom **sbrk-based allocator** shared
  between startup "decoy" allocations, the password buffer, and user
  messages.

## Root cause

At startup the binary allocates, in order, three chunks via a helper that
walks a single global freelist (head at `0x43a0`) and falls back to `sbrk`
when no free node is found:

| Chunk | Total size | Usable data | Purpose |
|-------|-----------:|------------:|---------|
| A | `0x38` (56) | `0x20` (32) | decoy, freed right after creation |
| B | `0x58` (88) | `0x40` (64) | decoy, freed right after creation |
| C | `0x38` (56) | `0x20` (32) | password buffer (`fopen`/`fread` of `password.txt`), **never freed** |

Because `sbrk` only ever grows the break and nothing runs between these
three allocations, A, B, and C are laid out **contiguously** in that exact
order in memory. A and B are marked free (their flag byte set) immediately
after allocation; C stays permanently "in use".

The `write` command's allocator reuses **any** freelist node with a
non-zero flag, **without ever checking that node's original size** against
the new message length, then does:

```c
strncpy(chunk_data, input, strlen(input) + 1);
```

Since A is freed and sits first in the freelist, the very first `write`
call reuses chunk A's 32-byte data buffer. Supplying a message longer than
32 bytes overflows straight through:

```
A_data(32) + B_header(24) + B_data(64) + C_header(24) = 144 bytes
```

...landing exactly at the start of C's data — the live password buffer —
letting us overwrite the stored password with any string of our choosing.

`strlen()`/`strncpy()` both stop at the **first NUL byte** in our own input,
so the payload must **not** contain a NUL before offset 144. Embedding a
literal NUL exactly at `144 + len(new_password)` truncates `strncpy`'s copy
count so it stops precisely after our replacement password, cleanly
NUL-terminating it without clobbering anything past chunk C. A trailing
`\n` (after the embedded NUL) is still required so the server's `fgets`
call actually returns.

## Exploitation

1. `write` → send `b"A"*144 + b"pwn3d" + b"\x00\n"`. This overflows chunks
   A → B → C, leaving the global password buffer set to `pwn3d\0`.
2. `auth` → send `pwn3d`. `strlen`/`strncmp` against the corrupted buffer
   now matches, printing `flag.txt`.

Script: [solve.py](../Hack%20The%20Vault%20III/solve/solve.py).

## Verification

```
$ python solve.py
...
Enter your message: 
Your message ID is 0.
> 
Enter your password to gain full access to the vault.
Welcome back, moss man.
bushbash{th1rd-times-th3-chArM!}
```

## Lessons / reusable pattern

- "Securely storing password in memory" (as opposed to a `.rodata`
  constant) is a strong signal the password lives on a heap/pool that user
  input can also reach — look for a custom allocator before brute-forcing.
- Custom allocators that recycle freelist nodes **by availability only**
  (ignoring the original chunk's size class) are a reliable
  bump-allocator overflow primitive: free a small object, then write a
  larger one into the same slot to spill into whatever was allocated right
  after it in `sbrk` order.
- `strlen`/`strncpy`-based copies driven off attacker-controlled input
  length can be *used* to precisely bound an overflow: embed a NUL at the
  exact target offset to stop the copy exactly where you want, instead of
  overflowing further than necessary.
