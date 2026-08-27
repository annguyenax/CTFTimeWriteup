# Evidence manifest — faulty_image_2

| File | Claim supported | Source/Tool | Reproduction | Why kept |
|------|-----------------|-------------|--------------|----------|
| ../solve.py | Flag = XOR(tIGr body, key from tEXt); deterministic | solver | `python solve/solve.py files/corrupt2.png` | Reproduces flag |
| decoy_nothing_here.png | The visible IDAT image is a decoy ("Nothing here lol!") | PIL render | rebuild PNG from IDAT | Shows flag is not in pixels |

## Result
- corrupt2.png sha256 = d2f8404a2051ed0bd62efc13df0f3ef23ac45087f851972768517336b3428dab
- IHDR 400x150 RGB; IDAT intact -> decoy image "Nothing here lol!".
- tEXt: `XOR-Key = 636f64657469676572` = ascii "codetiger".
- Custom chunk `tIGr` (CRC intentionally wrong): [4-byte len=32][ciphertext].
- ciphertext XOR "codetiger" -> `LITCTF{c0d3t1g3r_w4s_h3r3_x0r!}` (null-padded to 32).

## Verification
Round-trip: re-XOR the recovered bytes with the key reproduces the tIGr body
exactly; flag ends with '}' and matches the declared length prefix.
