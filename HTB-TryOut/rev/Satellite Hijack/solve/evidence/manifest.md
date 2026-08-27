# Manifest — Satellite Hijack (HTB TryOut / rev)

## Artifacts
| File | Type | SHA-256 |
|------|------|---------|
| `files/extracted/rev_satellitehijack/satellite` | ELF 64-bit LSB PIE, x86-64 | `6F07D3F664F5BB1962F0069A9315DC5FFD6A1A3830DB10E1DFE71D2813334E1B` |
| `files/extracted/rev_satellitehijack/library.so` | ELF 64-bit LSB PIE, x86-64 (shared object) | `4127782D0B1973A6B8ACB9FF3CE8A63C8B23AA625D92DE33EC58850D5D1833C5` |

## Deliverables
- `solve/solve.py` — reproducible solver (reads library.so, decrypts region, extracts key,
  derives flag, re-simulates checker).
- `solve/evidence/analysis_notes.txt` — analysis write-up.
- `solve/evidence/manifest.md` — this manifest.
- `solve/final_flag.txt` — `HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}`
- `writeup/writeup.md` — Vietnamese write-up.

## Key evidence excerpts (from objdump of decrypted region)
```
1235: movabs $0x37593076307b356c,%rax
123f: movabs $0x3a7c3e753f665666,%rdx
1253: movabs $0x784c7c214f3a7c3e,%rax
125d: movabs $0x663b2c6a246f21,%rdx
...
1280: movzbl (%rdi,%rax,1),%edx     ; dl = input[i]
1284: xor    (%rax,%rcx,1),%dl      ; dl ^= key[i]
128b: cmp    %rax,%rdx              ; == i ?
128e: jne    12ac                   ; mismatch -> return 0
1299: cmp    $0x1c,%rax             ; i == 28 ?
129f: mov    $1,%eax                ; valid
```
Unpacker trigger: `send_satellite_message` stub reads env `SAT_PRODENVIRONMENT`;
if set, calls 0x23e3 which mmap+memcpy+memfrob (XOR 42) of .text [0x11a9,0x21a9).

## Verification
1. Solver re-simulation of checker (assert key[i]^inner[i]==i, i=0..27) — PASS.
2. Manual cross-check of movabs constants + XOR loop vs objdump — MATCH.
