# It's Oops PM — evidence

| File | Claim |
|------|-------|
| `01_backdoor.txt` | Trigger `1111111111101001` (0xFFE9), key `0110001111100001` (0x63E1) |
| `02_tpm_sim.txt` | Python simulation of tpm/encryption/backdoor matches hand-derived values |
| `03_zip_manifest.txt` | zip contains only 5 files (4 VHDL + schematic.png) |
| `schematic_ocr.txt` / `schematic_ocr_bw2x.txt` / `schematic_ocr_inv.txt` | Windows OCR of schematic: only labels INPUT/CRYPTO/LOGIC/MUX — no flag/hex text |
| `schematic_lsb_check.txt` | No HTB{...} in RGB/alpha LSBs of schematic.png |

| `03_remote.txt` | Live TCP: Output=key + flag | `solve.py --target 154.57.164.82:31090` |
| `04_verify_replay.txt` | Same flag on independent session | nc |

Flag verified: `HTB{4_7yp1c41_53cu23_TPM_ch1p}`
