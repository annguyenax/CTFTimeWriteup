# Operation Midnight Drop

## Flag

```text
PTITCTF{v3nd0r_n0t1f13d_p4tch_d3pl0y3d_aec2b45793a5}
```

Remote: `144.79.188.39:37082`. Solver: `solve/win.py` / `solve/solve.py`.

## Bug

Custom "Threat Intel Engine v3.0" ASCII protocol (`type\nlen\nchecksum\npayload`).

RULE (`align8` at `0x155e`) does:

```text
size = ((rlen + 7) & 0xff) & ~7   // 8-bit truncate
if size == 0: size = 8
if size > 0x80: reject
malloc(size)
memcpy(slot, payload+2, rlen)     // uses rlen, not size
```

`rlen=0x100` → size wraps to 0 → malloc(8) but copies 256 bytes. Heap overflow.

ANALYZE always `puts("[+] running analyzer...")` then `report->fp(report, token^0xa55a1337)`.

## Exploit

1. AUTH: `token ^ 0xc0ffee00`
2. RULE create `rlen=0x80` (chunk before REPORT)
3. REPORT create; leak `'P'` = cookie(puts@GOT)
4. Overflow: command at slot+0xb0 (`= report+0`), `system` at slot+0xd0 (`= report+0x20`)
5. ANALYZE → `system("cat /home/ctf/flag.txt")`

Libc is **Ubuntu 24.04 glibc 2.39** (`puts=0x87cc0`, `system=0x58750`). Offset `0x83cc0` is glibc 2.29 — same page nibble `0xcc0`, wrong `system`. Direct `puts(report)` proved the fp overwrite; wrong `system` was the only miss.
