# GhostVM

- **Event:** PTITCTF2026
- **Category / tags:** Reverse / custom VM / Feistel
- **Flag format:** `PTITCTF{...}`
- **Attachments:** `GhostVM.zip` → `GhostVM.exe` (PE32+, 44032 bytes)
- **Status:** solved
- **Techniques used:** stacked custom VM, splitmix keystream, Feistel inverse

## Prompt (verbatim)

Một bộ phim kinh dị bị thất lạc vừa được tìm thấy trong kho lưu trữ cũ. Không ai nhớ từng xem nó, nhưng mọi bản ghi đều cho thấy bộ phim luôn có thêm một cảnh mới sau mỗi lần phát.

Trong khung hình cuối, một bóng ma đứng sau màn ảnh và thì thầm một câu không ai nghe rõ.

Hãy tìm ra lời thì thầm đó trước khi bộ phim gọi tên bạn.

## Recon

PE32+ MSVC iostream crackme. `main` at `0x140001CD0` prints XOR-obfuscated `Enter flag: `, reads a string, requires **length 32**, then runs checker `0x140005BA0`.

User strings decrypt as `out[i] = enc[i] ^ ((i*0x11 + key) & 0xff)` (`Enter flag:` / `Correct flag!` / `Wrong flag!`).

## Vulnerability / insight

Two stacked VMs. Shared per-PC stream:

```
x  = (pc * 0x9E3779B97F4A7C15 + seed) ^ (pc << 32)
x  = splitmix64_mix(x)
plain = enc[pc] ^ fold_to_byte(x)
op    = T1[b] ^ ROL8(T2[b], b&7) ^ 0xA5
```

- **VM1** (`0x1400026A0`, 8 regs, 18 ops, seed `0xD00DFEED11223344`): 0x74-byte program decrypts ROM at `0x140007420` into a 0x1E5C buffer.
- **VM2** (`0x1400039B0`, 16 regs, 31 ops, seed `0x0BADC0FFEE0DDF00`): runs that buffer against the 32-byte input plus a Fisher–Yates S-box from `0x140001F60`.

VM2 packing: permute/XOR the 32 input bytes into `r0..r3`, then **16 Feistel rounds** on the 256-bit state `(A,B)=( (r0,r1), (r2,r3) )`:

```
(A', B') = (B, A XOR F(B))
```

`F` is ARX + S-box inserts + two odd 64-bit multiplies. Final compare:

```
r0 == 0xffe472913819fb83
r1 == 0xff12a1c6dff42510
r2 == 0xaba41a37d8f557ea
r3 == 0xdf68174149473fc4
```

Feistel inverse does not need `F` inverted: `(A,B) = (B' XOR F(A'), A')`. Unpack the recovered 256-bit plaintext with the same permutation/XOR map.

## Solver

```bash
python solve/solve_ghostvm.py    # VM1 → vm2_bytecode.bin
python solve/disasm_vm2.py       # VM2 listing
python solve/invert_feistel.py   # recover 32-byte flag
```

## Flag

```
PTITCTF{vm_1s_ju5t_4_sh4d0w_r3!}
```

## Verification

- `invert_feistel.py`: inverse then forward matches the four ciphertext words.
- Live `GhostVM.exe` stdin of that 32-byte string prints `Correct flag!`.

## Dead ends

- Treating VM1 ciphertext as VM2 bytecode (wrong tables at `0x9480` vs `0x9280`).
- Treating `8`-`56` shift operands as register indices (they are immediates).
- Opcode-decoding every stream byte including immediates.

## What to reuse next time

- Two-stage VM: outer program is often a short decrypt loop; dump its output before reversing the inner ISA.
- 256-bit “hash” with swap+XOR of a round function is Feistel: invert from the compare constants without inverting F.
