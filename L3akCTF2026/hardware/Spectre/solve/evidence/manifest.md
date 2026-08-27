# Evidence manifest

## `reconstruction.txt`

- Claim supported: the original PNG deterministically yields a 104.327256-second WAV containing 107 spoken units; two phase seeds and two ASR model sizes agree on the recovered message.
- Source/tool: `files/spectre.png`, `solve/reconstruct.py`, librosa 0.11.0, Whisper `tiny.en` and `base.en`.
- Reproduction: see `writeup/writeup.md`, section “Cách giải tối thiểu”.
- SHA-256: `afdbe67469d464a97d8481f4fd181df255278a17184c1075ab0b86e2efd3cce2`.
- Retention reason: concise, decisive verification data; no model, cache, or generated WAV needs to be committed.

## `../reconstruct.py`

- Claim supported: deterministic conversion of the original PNG into a playable WAV and an invariant count of 107 spoken units.
- Source/tool: Python, Pillow, librosa 0.11.0 and soundfile.
- Reproduction: `python .\solve\reconstruct.py .\files\spectre.png -o recovered.wav --seed 0`.
- SHA-256: `c7c52e046e2d1dbdb863e3ab0423d73396c1130c6c701a2f239cbf8e55ed9206`.
- Retention reason: minimal final solver.
