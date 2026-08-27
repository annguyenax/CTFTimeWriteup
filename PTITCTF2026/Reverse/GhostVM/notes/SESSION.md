# GhostVM (PTITCTF2026 Reverse) — session notes

Binary: `D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe` (44032 bytes)  
Flag (verified by emulator + live `GhostVM.exe`): `PTITCTF{vm_1s_ju5t_4_sh4d0w_r3!}`

Challenge flavor: a lost horror film that adds a new scene each play; in the last frame a ghost whispers something.

## 1. PE / strings triage

- PE32+ x64, MSVC C++ console (`Subsystem=3`), ImageBase `0x140000000`, EP `0x140006280` (CRT).
- Sections: `.text` 0x5dd8, `.rdata` 0x3efa, tiny `.data`/`.pdata`/`.rsrc`/`.reloc`.
- Imports: iostream (`cin`/`cout`), CRT heap, `memcpy`/`memset`. No crypto APIs.
- User strings are XOR-obfuscated. Decrypt `out[i] = enc[i] ^ ((i*0x11 + key) & 0xff)`:
  - `"Enter flag: "` (key `0xb7`, len 12 @ VA `0x140007368`)
  - `"Correct flag!"` (key `0x97`, len 13 @ `0x140007378`)
  - `"Wrong flag!"` (key `0x97`, len 11 @ `0x140007388`)
- `main` @ `0x140001CD0`: print prompt, `cin >> string`, require **length == 0x20**, run checker `0x140005BA0`.

## 2. Two-stage custom VM

The checker is not a single interpreter. Stage 1 “develops the film” (decrypts inner bytecode into a 0x1E5C-byte buffer). Stage 2 plays that film against the 32-byte flag.

### Shared stream cipher (per-PC byte)

```
x  = (pc * 0x9E3779B97F4A7C15 + seed) ^ (pc << 32)
x ^= x >> 30;  x *= 0xBF58476D1CE4E5B9
x ^= x >> 27;  x *= 0x94D049BB133111EB
x ^= x >> 31
ks = (x ^ x>>8 ^ x>>24 ^ x>>40) & 0xFF
plain = enc[pc] ^ ks
```

Opcode decode (after decrypting one byte `b`):

```
op = (T1[b] ^ ROL8(T2[b], b&7) ^ 0xA5)
```

Different T1/T2 tables and seeds per stage.

### Stage 1 — loader / “film developer” (`0x1400026A0`)

- Seed `0xD00DFEED11223344`, program @ `0x1400073A0` size **0x74**.
- Tables `T1=0x140009280`, `T2=0x140009380`.
- 8 regs, 18 opcodes (0..17).
- ROM blob @ `0x140007420` (0x1E5C bytes of ciphertext).
- Loop 0x1E5C times: `k = mix64(i * 0xD1342543DE82EF95 ^ state)`; `mem[i] = ROM[i] ^ k_lo`; update ARX state (`+golden`, `ROL 9`, xor constants).
- Result: inner bytecode in `mem[0x1E5C]`.

### Stage 2 — flag checker (`0x1400039B0`)

- Seed `0x0BADC0FFEE0DDF00`, **runs `mem` as bytecode**.
- Tables `T1=0x140009480`, `T2=0x140009580`.
- 16 regs, 31 opcodes (0..30).
- Extra argument: Fisher–Yates S-box from seed `0x91C7A2D4E6385B0F` / mul `0x2545F4914F6CDD1D` (`0x140001F60`). **Must mask xorshift to 64 bits in Python.**
- I/O: `LOAD_INPUT rD, flag[imm8]`.
- `SUCCESS` (op 28) / `FAIL` (op 29).

Dead decoy code between rounds (`CMP_EQ r12,r12; JNZ; FAIL` and `JMP` over `NOT/SWAP/FAIL`) is never taken — “new scene each play” flavor.

## 3. Inner program (the whisper)

1. **Pack** 32 flag bytes into r0..r3 with a permutation + XOR constants, e.g.  
   `r0 |= (flag[19]^0x56) | (flag[2]^0xB6)<<8 | ...` (full map in `solve/solve_all.py` `PACK`).
2. **16-round Feistel** on two 128-bit halves `(r0||r1)` / `(r2||r3)`.  
   Round function (per 64-bit half) is ARX + 4 S-box nibble inserts + two odd 64-bit muls:
   - `MUL1 = 0xD6E8FEB86659FD93`
   - `MUL2 = 0x9FB21C651E98DF25`
   - `KXOR = 0xA0761D6478BD642F`  
   Then `new_R = old_L ^ F(old_R)`, swap halves.
3. **Compare** final words to:
   - `r0 == 0xFFE472913819FB83`
   - `r1 == 0xFF12A1C6DFF42510`
   - `r2 == 0xABA41A37D8F557EA`
   - `r3 == 0xDF68174149473FC4`  
   Any mismatch JZ’s off the end of the program (fail); fall-through is `SUCCESS`.

## 4. Extraction

Feistel inverse is just “compute F on the current left half, XOR into right, unswap” (F itself is not inverted). Unpack the 256-bit plaintext with the same permutation/XOR map.

Recovered: `PTITCTF{vm_1s_ju5t_4_sh4d0w_r3!}` (exactly 32 bytes).

## 5. Evidence

- Static disasm of handlers: `solve/vm1_interp.asm`, `solve/vm2_interp.asm`.
- Inner listing: `solve/vm2_disasm.txt` (ends `CMP_EQ r0..r3` then `SUCCESS`).
- Solver: `solve/solve_all.py` — VM2 emu of recovered flag produces the four ciphertext words and returns success.
- Live run:

```
Enter flag: Correct flag!
```

## Flag

```
PTITCTF{vm_1s_ju5t_4_sh4d0w_r3!}
```
