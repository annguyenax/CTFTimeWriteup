# Evidence manifest — any_secrets_could_instantly_be_imparted

| File | Claim supported | Source/Tool | Reproduction command | Why kept |
|------|-----------------|-------------|----------------------|----------|
| ../solve.py | Ciphertext is Caesar +4 over raw ASCII; decrypts to the flag | hand-written solver | `python solve.py` | Deterministic solver + round-trip verification |

## Result
- Ciphertext: `HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y`
- Shift: +4 on each byte value (mod 256)
- Flag: `LITCTF{ASCII-jUl1us-c43s4r-gewowa}`

## Verification
`python solve.py` prints the flag and asserts that re-encrypting the flag with
shift -4 reproduces the original ciphertext byte-for-byte (strong verification:
decrypt then re-encrypt exact ciphertext).
