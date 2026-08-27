# The Wellness Ring Bypass

## Flag

```text
PTITCTF{h3y_th1s_r1ng_1s_y0ur_c0ngr4tul4t10n_8f9f9eee06eb}
```

Remote `144.79.188.39:39807`. Solver: `solve/exploit.py` / `_work/win.py`. Flag file `/home/oura/flag.txt`.

## Binary

PIE, Full RELRO, Canary, NX, CET note (IBT+SHSTK). Ubuntu 24.04 **glibc 2.39-0ubuntu8.8** (`puts=0x87cc0`, `system=0x58750`). The libc shipped in the zip is an older 2.39 (`puts=0x87bd0`) — leak nibble `0xcc0` identifies the live one.

Custom firmware heap: 16 size-class pools. Menu 10 **returns from main**; libc then `exit()`.

## Bug

Context descriptor is 0x80 bytes; menu 6/7/8 read `obj+0x80..+0xb8`. Context alloc also mallocs a lost 0x80 `rx-guard` sentinel, so naive `ctx then cache` makes OOB hit the sentinel.

Free-list FIFO: alloc cache0+cache1, **free cache0**, then alloc context. Context reuses off 0; sentinel goes to bump; live cache1 sits at `context+0x80`.

Menu 7/8: `p=*(desc+0x10); src=*p; dest=*(p+8)`. Size at `desc+0x28` must be **>=** dump length. Hex dump is prefixed `fw-sleep-stage-window: `.

## Exploit

1. Overlap cache1 with context OOB → leak heap + PIE (menu 6).
2. Fake desc + `{src,dest}` pair in later caches → arbitrary R/W ≤ 0x80.
3. Two writes of House of Apple 2 onto `_IO_2_1_stderr_` (leave stdout intact; menu uses `printf`).
4. Menu 10 → `exit()` flushes stderr → `system("  sh")` → `cat /home/oura/flag.txt`.

ROP on main's saved RIP is the wrong first try: CET SHSTK may fire, and the zip libc `0x2a264` is the init return not main (`0x2a1ca`).
