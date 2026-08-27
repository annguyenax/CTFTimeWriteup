# Evidence manifest — double_disguise

| File | Claim supported | Source/Tool | Reproduction command | Why kept |
|------|-----------------|-------------|----------------------|----------|
| ../solve.py | Ciphertext = Base64(single-byte XOR(flag)); key 0x2A recovers flag | hand-written solver | `python solve.py` | Deterministic solver + round-trip verification |

## Result
- Ciphertext (Base64): `ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==`
- Layer 1: Base64 decode
- Layer 2: single-byte XOR, key = 0x2A (42, '*')
- Flag: `LITCTF{F1fa_W0rld_cup}`

## Verification
`python solve.py` recovers the flag and asserts that re-encrypting it
(XOR 0x2A then Base64) reproduces the original ciphertext string exactly.
