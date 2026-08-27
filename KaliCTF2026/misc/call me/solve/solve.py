#!/usr/bin/env python3
"""
call me (KaliCTF2026 Misc) — spectrogram text + Morse hint

signal_037.wav:
  0-15s: flag painted into spectrogram
  16s+:  800 Hz CW Morse: "VVV VVV NEXT CHECK MY LINKEDIN TO GET PART2"

Flag recovered from spectrogram (leetspeak):
  KaliTeam{S1gn4l_h34rd_l0ud_4nd_c134r_part2}
"""
from __future__ import annotations

from pathlib import Path
import wave
import numpy as np
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
WAV = HERE.parent / "files" / "signal_037.wav"
OUT = HERE / "evidence" / "spectrogram_flag.png"


def make_spectrogram(wav_path: Path, out_path: Path, t_end: float = 15.0) -> str:
    with wave.open(str(wav_path), "rb") as w:
        fr = w.getframerate()
        sig = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    sig = sig[: int(t_end * fr)]
    win, hop = 4096, 256
    frames = []
    for i in range(0, len(sig) - win, hop):
        chunk = sig[i : i + win] * np.hanning(win)
        frames.append(np.abs(np.fft.rfft(chunk)))
    S = np.log1p(np.square(np.array(frames).T))
    lo, hi = np.percentile(S, [40, 99.5])
    S = np.clip((S - lo) / (hi - lo + 1e-9), 0, 1)
    freqs = np.fft.rfftfreq(win, 1 / fr)
    mask = (freqs >= 200) & (freqs <= 8000)
    img = (S[mask][::-1] * 255).astype(np.uint8)
    im = Image.fromarray(img).resize((img.shape[1] * 2, img.shape[0] * 3), Image.NEAREST)
    im = ImageOps.autocontrast(im)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path)
    return str(out_path)


def main() -> int:
    path = make_spectrogram(WAV, OUT)
    print("spectrogram:", path)
    print("Read text from spectrogram (visual):")
    print("KaliTeam{S1gn4l_h34rd_l0ud_4nd_c134r_part2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())