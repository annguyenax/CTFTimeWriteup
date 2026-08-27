# Signaling

**Status: PAUSED — no candidate flag.** Nothing here is a verified flag.

## Challenge

- Event/category: PTITCTF2026 / Crypto
- Description: `How roblox expects us to talk to eachother`
- Artifact: `files/Signaling.zip` -> video-only `Signaling.mp4`
- Expected format: `PTITCTF{...}`

```text
EB4714FAEBCE1DB06AA6ADF1105FE378033A1CE221EA87D0A23778A5634B19FE  Signaling.zip
795BF643D34AF589B23CF62B439F2D7CC3E25B0C6FF05CF0115387360E7812B8  Signaling.mp4
```

## Correct model

The video is a clock-like signaling animation, not a lighthouse. It has two hands in eight directions and two highlighted outer sectors. The long hand ends near radius 164 px, the short hand near 114 px, while static clock ticks begin near 171 px.

The old angular histogram confused cardinal ticks with hands. Measuring the continuous bright run from the hub fixes this and preserves long/short ordering.

## Reproducible extraction

```powershell
python .\solve\extract_ordered_hands.py
```

```text
stable_symbols=47
semaphore_ciphertext=HWRNUQZQKJEXRMUWBKRIUPFCRMUJHNXWMRLNHUCVOTMOLRK
```

The solver samples each stable hold, selects exactly one long and one short ray, applies one fixed mirror/rotation, and looks up standard semaphore. All 47 symbols are valid under the same transform, strongly verifying this first layer.

Public descriptions of ABM's `次元通信 (Signaling)` MV explicitly identify semaphore and hidden messages. That supports the technique but does not solve the second layer.

## Remaining blocker

The 47-letter result is still ciphertext. The outer ring contains 42 genuine two-sector symbols and probably controls the second transformation, but the convention is unresolved.

Ruled out with bounded tests:

- Morse, base-4, and direct semaphore plaintext;
- packed 6-bit XOR/add/subtract;
- coordinate-wise angular compensation and fixed cross-pairing;
- Vigenere combinations and obvious keyword Vigenere;
- fixed delay/permutation between channels;
- appended MP4 payload and shallow LSB extraction.

## Next actions

1. Recover the exact two-channel convention from the original MV/creator context.
2. Model each outer pair as a constrained per-symbol reference frame.
3. Require deterministic replay and a valid `PTITCTF{...}` result before creating `final_flag.txt`.

## Sources

- [Semaphore Flag Signalling System](https://www.cpbr.gov.au/flags/semaphore.html): alphabet mapping.
- [ABM — 次元通信 (Signaling)](https://www.youtube.com/watch?v=PqpCRSOUuIE): likely visual provenance.
