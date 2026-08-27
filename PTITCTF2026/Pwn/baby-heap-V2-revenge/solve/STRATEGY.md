# Analysis of NOTE_PROFILE & Counters in baby-heap-V2-revenge

## Target: `144.79.188.39:40838`

### Binary Counters in `.data`:
- `delete_limit` @ `0x4010` = initial `4`
- `edit_limit` @ `0x4014` = initial `3`
- `create_limit` @ `0x4018` = initial `6`

### Initialization in `main`:
1. `NOTE_PROFILE` is checked.
2. If `NOTE_PROFILE` is not set, it reads `/proc/self/comm` and XORs `comm` hash into `delete_limit` @ `0x4010` (`0x1406: xor [0x4060], eax`) and `create_limit` @ `0x4018` (`0x141e: xor [0x4060], eax`).
3. If `/proc/self/comm` is `"chall"`, the hash modifies `create_limit` and `delete_limit`!

### Exploit Strategy with 6 Allocations, 4 Deletes, 3 Edits:
- Alloc 0: `0x500` (Unsorted Bin chunk)
- Alloc 1: `0x20` (Guard chunk against Top consolidation)
- Delete 0: chunk 0 goes to **Unsorted Bin** (only if tcache is bypassed or size > 0x410 / tcache count limit).
  - In Glibc 2.35, tcache handles chunks up to `0x410` (chunk size `0x420`).
  - Size `0x500` (> `0x410`) **NEVER goes to tcache**! It goes **DIRECTLY to the Unsorted Bin** on the very first delete!
- Read 0: Leaks `main_arena + 96` (`libc_base = leak - 0x21ace0`).
- Alloc 2: `0xe0`
- Alloc 3: `0xe0`
- Delete 2: Leaks Heap (`heap_base = (leak << 12)`).
- Delete 3: UAF Edit chunk 3 to poison tcache or forge House of Apple 2 on heap.
- Trigger shell!
