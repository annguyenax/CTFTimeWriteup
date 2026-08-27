# Evidence manifest — Sơn Tùng M-TP

| File | Claim supported | Source / tool | Reproduction | SHA-256 | Why retained |
|---|---|---|---|---|---|
| `spectrogram_flag.png` | The 15.2–18.85 kHz band spells the **decoy** `PTITCTF{n1c3_try_ju57_try_h4rd3r_i_gu355}` (not the flag). | `chall.wav`; NumPy Hann-window FFT in `../solve.py` | `python ../solve.py <path-to-chall.wav>` | `f4261c7d7514fb9612d4f0fc8c1c3f4b548133e51afc623cb3a8504915b495fe` | Visual evidence of the planted fake flag. |

Source integrity:

- Supplied archive SHA-256: `40d74ae84433c3c28579b117b3709231bf444e92905bffa996bc06e1c1b2d5cd`
- Extracted `chall.wav` SHA-256: `01a78ea1b28d71ca2b955d11048427e3acfe4d72ce6cfb15eb7e7581204dc713`
- WAV format: stereo signed 16-bit PCM, 48,000 Hz, 11,791,623 frames (245.6588125 s).
