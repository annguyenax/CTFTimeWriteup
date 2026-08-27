#!/usr/bin/env python3
"""Render the ultrasonic spectrogram decoy (nice-try text, not the flag)."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import wave

import numpy as np
from PIL import Image, ImageEnhance


EXPECTED_WAV_SHA256 = "01a78ea1b28d71ca2b955d11048427e3acfe4d72ce6cfb15eb7e7581204dc713"
DECOY = "PTITCTF{n1c3_try_ju57_try_h4rd3r_i_gu355}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def render(wav_path: Path, output_path: Path) -> None:
    with wave.open(str(wav_path), "rb") as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (2, 2, 48000):
            raise ValueError("expected stereo, signed 16-bit PCM at 48 kHz")
        frame_count = min(wav.getnframes(), wav.getframerate() * 20)
        samples = np.frombuffer(wav.readframes(frame_count), dtype="<i2")

    mono = samples.reshape(-1, 2).astype(np.float32).mean(axis=1)
    nfft, hop = 2048, 96
    count = 1 + (len(mono) - nfft) // hop
    frames = np.lib.stride_tricks.as_strided(
        mono,
        shape=(count, nfft),
        strides=(mono.strides[0] * hop, mono.strides[0]),
    ).copy()
    frames *= np.hanning(nfft)

    spectrum_db = 20 * np.log10(
        np.maximum(np.abs(np.fft.rfft(frames, axis=1)), 1e-7)
    )
    frequencies = np.fft.rfftfreq(nfft, 1 / 48000)
    times = (np.arange(count) * hop + nfft / 2) / 48000
    crop = spectrum_db[
        (times >= 1.7) & (times <= 19.2)
    ][:, (frequencies >= 15200) & (frequencies <= 18850)].T

    pixels = np.clip((crop - 65) * 255 / 45, 0, 255).astype(np.uint8)
    image = Image.fromarray(np.flipud(pixels), mode="L")
    image = image.resize(
        (image.width * 2, image.height * 3), Image.Resampling.NEAREST
    )
    image = ImageEnhance.Contrast(image).enhance(1.35)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wav", type=Path, help="chall.wav extracted from the supplied 7z")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).parent / "evidence" / "spectrogram_flag.png",
    )
    args = parser.parse_args()

    actual_hash = sha256(args.wav)
    if actual_hash != EXPECTED_WAV_SHA256:
        raise SystemExit(
            f"unexpected WAV SHA-256: {actual_hash}\nexpected: {EXPECTED_WAV_SHA256}"
        )

    render(args.wav, args.output)
    print(f"WAV SHA-256: {actual_hash}")
    # Avoid legacy Windows console encoding failures on the accented challenge path.
    print(f"Spectrogram written: {args.output.name}")
    print(f"DECOY visible in spectrogram (do not submit): {DECOY}")


if __name__ == "__main__":
    main()
