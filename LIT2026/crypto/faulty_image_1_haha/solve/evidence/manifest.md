# Evidence manifest — faulty_image_1_haha

| File | Claim supported | Source/Tool | Reproduction | Hash (sha256) | Why kept |
|------|-----------------|-------------|--------------|---------------|----------|
| ../solve.py | Repair = remove 4-byte 'haha' inserted every 104 bytes; IDAT then decompresses to 180150 bytes | solver | `python solve/solve.py files/corrupt.png out.png` | — | Deterministic reconstruction |
| recovered.png | Reconstructed valid PNG rendering the flag text | solver output | see above | 16167c28…3b23 | Shows the flag |
| flag_zoom.png | Zoomed crop confirming exact flag characters | PIL crop/upscale | — | — | Character-level verification |

## Result
- Corruption: `b'haha'` (68 61 68 61) inserted every 100 original bytes (stride 104), starting at file offset 100.
- After removing the markers, IDAT (len 2155) decompresses to 180150 = 150×(1+400×3) bytes.
- Flag (image text): `LITCTF{y0u_f1x3d_m3_85hf91j!}`

## Verification
Deterministic: `python solve/solve.py` on the original corrupt.png always yields
the same valid PNG whose pixels render the flag; decompressed raw size matches
the exact expected size for a 400×150 8-bit RGB image.
