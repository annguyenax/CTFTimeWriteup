# Sơn Tùng M-TP — re-exam (attempt-limited)

`chalenge.md` empty. Artefact: `files/Forensics - Sơn tùng M-TP.7z` → `chall.wav` (48 kHz stereo PCM, 245.6588125 s).

## Spectrogram is a decoy, and the old writeup misread it

Visible at 15.2–18.85 kHz, t ≈ 1.7–19.2 s (L, R, and residual after song subtract):

```text
PTITCTF{n1c3_try_ju57_try_h4rd3r_i_gu355}
```

= “nice try just try harder i guess”. **Do not submit** while the board has a try limit.

Previous `final_flag.txt` / writeup claimed `PTITCTF{N0T_JUST_MUSIC_BUT_A_MASTERPIECE}`. That string is **not** in the spectrogram — it was a misread of the same glyphs. The PNG in `solve/evidence/spectrogram_flag.png` already showed the decoy text.

## Cover song

After the overlay, tempo-median ≈ 95.7 BPM and duration 4:06 match **Hãy Trao Cho Anh** (Sơn Tùng M-TP ft. Snoop Dogg).

Official MV audio (`knW7-x7Y7RE`) aligns with NCC ≈ 0.995 at offset **+12.340 s**. Residual after gain-matched subtract still shows **only** the decoy banner; the rest is AAC codec error following the mix. No second spectrogram line.

## Dead ends (not the real flag)

- Raw `PTITCTF{` / `flag{` in the WAV: none
- RIFF extra chunks / trailing bytes: none
- LSB 1–2 bit: entropy 7.9999, no zip/png/zlib payload
- Side / L-R / phase / dphase: decoy is mid (both channels)
- Time-reverse: mirrored decoy only
- Morse 0–400 Hz: kick/beat, not CW
- SSTV 1.2–2.3 kHz / 1900 Hz leader: music, not vis-code
- QR on high-res residual spectrogram: none
- Later 15–19 kHz / whole-file overview: no other painted text

## Status

Unsolved. Real flag not recovered. Do not spend a board attempt on either the decoy or `MASTERPIECE`.
