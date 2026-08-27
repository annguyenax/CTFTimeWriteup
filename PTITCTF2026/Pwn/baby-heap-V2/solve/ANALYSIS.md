# baby-heap-V2 — reverse analysis

Binary: PIE, Full RELRO (BIND_NOW), stripped, NX. Ubuntu 22.04 → **glibc 2.35** (no __free_hook/__malloc_hook).
Flag lives only in `/flag.txt` on the server (entrypoint writes it). Binary does NOT read it → need **RCE / arbitrary read**, then `cat /flag.txt`.

## Menu (== Heap Basic V2 ==)  slots at .bss 0x4080, struct = {void* ptr; size_t size} (16 bytes), 8 slots (index 0..7)
- Counters (limits): create=0x4018, edit=0x4014, delete=0x4010 (each decremented per op).
- **1 Create**: size via strtoul, check `1 <= size <= 0x520`; malloc(size); slot={ptr,size}; then custom read into chunk. (0x1990–0x19e1). A helper (0x1b80) uses /proc/self/maps `%lx-%lx` → likely prints a **heap/base leak**.
- **2 Read** (0x17b8): prints slot content.  → **UAF read** after delete = leak fd/bk.
- **3 Edit** (0x16b0): re-reads data into slot ptr (limited).  → **UAF write** after delete = tcache poison.
- **4 Delete** (0x1670): `free(slot->ptr)` at 0x168c but **does NOT null slot->ptr** → **UAF + double free**.

## Vulnerability
Use-After-Free (no clear-on-free) + double-free. Safe-linking present (2.32+) so tcache fd = target ^ (chunk>>12) → need heap leak (Create likely leaks it).

## Exploit plan (glibc 2.35)
1. **Heap leak**: from Create's printout (or UAF-read a tcache-freed chunk's mangled fd + recover with heap base).
2. **libc leak**: Create a chunk > 0x410 (e.g. 0x500 ≤ 0x520) so free() → unsorted bin; UAF **Read** it → leaked `main_arena+96` → libc base.
3. **Arbitrary write**: tcache poisoning via UAF-**Edit** the fd of a freed tcache chunk to `target ^ (heap>>12)`; two Creates return a chunk at `target`.
4. **RCE (no hooks in 2.35)** — pick one:
   - **FSOP / House of Apple 2**: overwrite `_IO_2_1_stdout_` (or stderr) vtable+_wide_data to hijack `_IO_flush_all` on exit/next puts → one-gadget or system.
   - or overwrite `__exit_funcs` (initial) with a mangled system-call frame.
   - or leak stack via `environ` (libc symbol) then tcache-poison onto a saved return address → ROP `open/read/write` or `system("cat /flag.txt")`.
5. `cat /flag.txt`.

## How to develop (needs local test + instance)
- `cd public && docker compose up -d` replicates the exact target (libc). Pull its libc/ld for pwntools.
- Develop `exploit.py` against local `nc localhost 6301`, then point `REMOTE` at the instance.
