# baby-heap-V2

## Flag

```text
PTITCTF{y0u_h4v3_f0und_th3_g00d_p4rt_0f_51gn41_decb0010da61}
```

Remote `144.79.188.39:37415`. Solver: `solve/exploit.py`. Flag file on the box is `/flag.txt` (not `/home/ctf/flag.txt`).

The flag text itself (`51gn41`) looks like a breadcrumb for Crypto **Signaling**.

## Binary

PIE, Full RELRO, NX. Ubuntu 22.04 / **glibc 2.35** (no malloc hooks). 8 slots `{ptr,size}`, counters create=6 / edit=3 / delete=4. Size `1..0x520`.

- **Delete**: `free(ptr)` and does **not** NULL the slot → UAF + double-free.
- **Read**: `write(1, ptr, size)` — UAF leak of tcache fd / unsorted bk. Does **not** use FILE*.
- **Edit**: fopen `/proc/self/maps`, require `[heap]` range, then `read(0, ptr, size)` — UAF write / tcache poison. Rejects non-heap with `Only heap writes are allowed`.
- **Create**: malloc, **then** fopen maps (no range check on the write), then `read(0, ptr, size)` — so a tcache-poisoned chunk that lands in libc **is writable**.
- Menu I/O is raw `write(2)`, not `printf`/`puts`. The only FILE* use of stdout is SIGALRM: `puts("Session closed"); exit(0);` (~60s).

## Exploit

1. Allocate two `0xe0` tcache chunks, one `0x500` unsorted, one `0x20` guard (prevents top consolidation).
2. Free + Read `0xe0` → tcache fd = `chunk>>12` → heap page. Keep the tcache **key** at +8.
3. Free + Read `0x500` → unsorted `main_arena+96` = libc+`0x21ace0`.
4. Free the second `0xe0`, UAF-Edit fd to `stderr ^ (heap>>12)` (safe-linking).
5. Create dummy, Create House of Apple 2 payload onto `_IO_2_1_stderr_` (pwncli `house_of_apple2_execmd_when_exit`: flags `"  sh"`, `_wide_data=stderr-0x48`, `chain=system`, vtable=`_IO_wfile_jumps`).
6. Wait for SIGALRM. `puts` still uses intact **stdout**; `exit()` flushes **stderr** → `system("  sh")`.
7. `cat /flag.txt`.

Smashing **stdout** instead makes `puts("Session closed")` crash before `exit()` flush, so no shell.

## Failed paths

- FSOP on stdout + expect the next menu print to trigger: menu is `write(2)`, not FILE*.
- Recv timeout 5s: alarm is 60s.
- Alloc size `0xe0` is fine (fopen's `locked_FILE` is larger, does not steal the tcache bin). First-chunk offset is **not** `heap+0x2a0` (Create's fopen allocates in between); encoding still only needs the page.
- Padding a `0x180` write through stdout would clobber `.bss` after the FILE.
