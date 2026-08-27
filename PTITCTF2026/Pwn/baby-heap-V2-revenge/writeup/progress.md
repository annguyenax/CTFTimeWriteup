# baby-heap-V2-revenge — Analysis & Progress (SOLVED locally, verifying live)

## 1. Binary / protections
- x86_64, Ubuntu 22.04 / **glibc 2.35**, Full RELRO, PIE, NX, stack canary.
- Max 8 slots `{ptr,size}` at `PIE+0x4080`; max size `0x520`.
- **Operation limits** (empirically verified + confirmed in gdb):
  - create_limit = **6** (slots 0..5)
  - delete_limit = **4**
  - edit_limit  = **3**

## 2. Menu & primitives
- **1 Create**: `malloc(size<=0x520)`, enforce `heap_start <= ptr && ptr+size <= heap_end`
  (parsed fresh from `/proc/self/maps` each time); store `{ptr,size}`; read data.
- **2 Read**: `write(1, ptr, size)` — **no bounds check** (UAF read / leak).
- **3 Edit**: enforce same heap bounds, then `read_input(ptr,size)` — writes **stored size**
  bytes with only a heap-wide bound, so a small chunk's edit overflows past its own
  chunk into the next chunk's header if still inside `[heap_start,heap_end]`.
- **4 Delete**: `free(ptr)` then `ptr`/`size` NOT zeroed → **UAF + double-free**.

- **SIGALRM handler** (`0x1cd0`): `puts("== babyheap-V2_patch ==")` then `exit(0)`.
  `main` calls `alarm(60)` (mov $0x3c,%edi; call alarm) → **60 s after connect** the
  handler fires → `exit()` flushes stdio → walks `_IO_list_all` → **FSOP trigger**.

## 3. Leaks — VALIDATED offline
- **Heap leak**: free a small chunk to tcache, read mangled `next = heap>>12`.
- **Libc leak**: free a chunk of size `0x418`+ (skips tcache → unsorted) behind an
  in-use guard; read `fd` → `main_arena+0x60`; `libc_base = leak - 0x21ace0`.

## 4. Code execution — largebin attack (glibc 2.35)
Direct libc writes are blocked by the heap-bounds check, so use a glibc-internal
write: the **largebin attack**.
- Free p1 (`0x428`) → unsorted; `malloc(0x438)` sorts it into largebin.
- Free p2 (`0x418`) → unsorted.
- UAF-edit p1: `p1->bk_nextsize = _IO_list_all - 0x20`.
- `malloc(0x438)` inserts p2 → glibc runs `fwd->bk_nextsize->fd_nextsize = victim`,
  writing **`p2` chunk address to `_IO_list_all`**. Verified 100% (5/5), works live.

## 5. House of Apple 2 / FSOP (glibc 2.35) — WORKING
Fake `_IO_FILE_plus` at `p2_chunk` (in a single controlled largebin chunk):
- vtable = `_IO_wfile_jumps` (libc+0x2170c0); `_lock`, `_wide_data`, `_codecvt`
  pointers into the same chunk; `_IO_write_base=0`, `_IO_write_ptr=1` → dirty;
  zero buffer/chain/backup pointers so `_IO_free_wbackup_area` doesn't crash.
- `_IO_wfile_overflow` → `_IO_wdo_write` → `_IO_wdoallocbuf` →
  `_wide_vtable->__doallocate` = **system**.

**Key blocker found:** `_IO_wfile_overflow` returns WEOF immediately if
`fp->_flags & _IO_NO_WRITES (0x8)`. `_flags` = `p2_chunk+0` = chunk `prev_size`,
which was uncontrollable garbage `0x47474747` ("GGGG") with bit 3 set → nothing fired.

**Fix:** the guard chunk `g1` (create size 0x18) stores a 0x18-byte buffer, and
Edit writes 0x18 bytes from `g1_user` = `[g1_user, g1_user+0x18)`, which **overflows
0x10 bytes into `p2_chunk+0`**. So `edit(1, b"X"*0x10 + p64(0x687320))` sets
`_flags = " sh\0"`:
- clears `_IO_NO_WRITES` (0x20 has bit 3 clear), and
- `__doallocate = system(fp) = system(" sh")` → spawns an interactive `sh`.
Verified in gdb: `system` called with `rdi = p2_chunk` = string `" sh"`, shell forks.

## 6. Exploit flow (`solve/exploit.py`)
1. create p1(0x428), g1(0x18), p2(0x418), g2(0x18).
2. delete p1 → leak libc (unsorted fd).
3. create(0x438) consumes/sorts p1; delete p2 → unsorted.
4. UAF-edit p1 bk_nextsize = `_IO_list_all-0x20`; create(0x438) → largebin write
   `_IO_list_all = p2_chunk`.
5. read p2 raw → recover `p2_chunk = p1_chunk + 0x450`.
6. edit p2 → fake FILE (wide_data @+0x200, codecvt @+0x300, vtable @+0x380,
   `__doallocate=system` @fake_wide_vtable+0x68).
7. `edit(1, b"X"*0x10 + p64(0x687320))` → `_flags=" sh"`.
8. Remote: wait 60 s for alarm → `system(" sh")` shell → `cat /flag.txt`.

Offline result: shell spawned, `cat /flag.txt` → `PTITCTF{local_test_flag}`.

## 7. LIVE CAPTURE ✅
Against `144.79.188.39:43039` the exploit spawned the shell and `cat /flag.txt`
returned the real flag:
```
PTITCTF2026{17_w45_n07_dda2dc230a39_345y_r1gh7}
```
Key live numbers: `libc_base=0x7427c20e9000`, `p2_chunk=0x5a740ae4fd00`.
