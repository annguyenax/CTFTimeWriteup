#!/usr/bin/env python3
"""Reconstruct the spoken message from spectre.png.

The PNG is an 80 dB, 192-bin mel power spectrogram.  Phase is absent, so this
script estimates it deterministically with Griffin-Lim.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from PIL import Image


EXPECTED_SHA256 = "e85821313acfb8f480eba24472917c670bbc0fb27d3d4356cf1705c59d8acbbf"


def count_spoken_units(gray: np.ndarray, threshold: int = 24) -> int:
    """Count stable time-localized energy groups in the rendered spectrum."""
    energy = np.percentile(gray, 90, axis=0)
    active = energy > threshold
    for _ in range(3):
        active[1:-1] |= active[:-2] & active[2:]

    runs = 0
    start: int | None = None
    for i, value in enumerate(active):
        if value and start is None:
            start = i
        if start is not None and (not value or i == len(active) - 1):
            end = i if not value else i + 1
            if end - start >= 3:
                runs += 1
            start = None
    return runs


def reconstruct(source: Path, destination: Path, seed: int) -> tuple[int, float]:
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"unexpected input SHA-256: {digest}")

    gray = np.asarray(Image.open(source).convert("L"), dtype=np.float32)
    if gray.shape != (192, 4494):
        raise SystemExit(f"unexpected image shape: {gray.shape}")

    units = count_spoken_units(gray)
    if units != 107:
        raise SystemExit(f"expected 107 spoken units, found {units}")

    # Images put high frequencies at the top, while librosa expects low to high.
    normalized = np.flipud(gray / 255.0)
    mel_power = librosa.db_to_power(-80.0 + 80.0 * normalized).astype(np.float32)
    magnitude = librosa.feature.inverse.mel_to_stft(
        mel_power,
        sr=22_050,
        n_fft=2_048,
        power=2.0,
        norm="slaney",
    )
    audio = librosa.griffinlim(
        magnitude,
        n_iter=24,
        hop_length=512,
        win_length=2_048,
        n_fft=2_048,
        random_state=seed,
    )
    audio *= 0.95 / max(float(np.max(np.abs(audio))), 1e-12)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sf.write(destination, audio, 22_050, subtype="PCM_16")
    return units, len(audio) / 22_050


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("recovered.wav"))
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    units, duration = reconstruct(args.image, args.output, args.seed)
    print(f"wrote={args.output}")
    print(f"spoken_units={units}")
    print(f"duration_seconds={duration:.6f}")


if __name__ == "__main__":
    main()
