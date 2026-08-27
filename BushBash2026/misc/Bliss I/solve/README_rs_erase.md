# `rs_erase_decode.py` — soft Data Matrix + RS erase

## Run

```powershell
cd "D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I"

# 1) analyze recovered.png only (fast)
python solve/rs_erase_decode.py --from-recovered

# 2) coarse search on bliss.png
python solve/rs_erase_decode.py --quick

# 3) denser search (slower)
python solve/rs_erase_decode.py
```

## Outputs (`solve/evidence/`)

| File | Meaning |
|------|---------|
| `matrix_18_from_recovered.txt` | 18×18 module ASCII |
| `cw_18_from_recovered.hex` | 32 codewords hex |
| `rs_erase_results.txt` | all trusted hits |
| `rs_corrected_dm.png` | if a flagish hit exists |

## Findings so far

- **Symbol size:** 18×18 (timing alternation perfect), **not** 20×20.
- ECC200: **18 data + 14 ECC** codewords (`nsym=14`).
- `recovered.png` already forms a **valid** RS codeword (`erased=0`, `agree=1`).
- ZXing text: `\x01DQR3LWR@NGF4\x05C/H671\x1b` — **valid barcode, wrong payload**
  (modules wrong enough to land in another codeword; ECC cannot “fix” further).
- Soft grid search on `bliss.png` produces many **false** zxing strings when
  `erased ≈ nsym` — filtered out (`erased ≤ nsym/2` required unless flag-like).

## Homography L-finder (geometry)

```powershell
python solve/homography_recover.py --size 18 --quick
python solve/homography_recover.py --size 18 --quick --de   # + differential evolution
python solve/homography_recover.py --size 18                # denser (slower)
```

Evidence: `homo_overlay_*.png`, `homo_best_matrix_*.txt`, `homo_corners_*.npy`, `homo_results.txt`.

Status: box locks onto the soft cloud DM; finder/timing score improves (~1.0+); interior
modules still too soft for a trusted `bushbash{…}` decode. `recovered.png` remains a
**valid-but-wrong** ECC codeword (`\x01DQR3…`).

## Next if still stuck

1. Soft bit LLRs + targeted flips guided by phone-scanned partial modules.
2. Phone Lens / high-contrast photo of the cloud region.
3. Do **not** treat media-query / runes path as Bliss I (that is Bliss II).
