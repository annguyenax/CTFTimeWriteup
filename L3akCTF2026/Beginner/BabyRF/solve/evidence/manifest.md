# Evidence manifest — BabyRF (PAUSED)

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| morse_11k6_signal.png | Tín hiệu OOK ở ~11.6kHz (6–16s) là Morse | matplotlib specgram | `python solve/analyze.py files/BabyRF.wav` | Chứng minh mode Morse |
| read_processing_reversed.png | Spectrogram text "Pr0c3ss1ng" (đọc khi ĐẢO audio) | specgram reversed | analyze.py + crop | Phần đọc bằng mắt |
| read_digits_3851642.png | Dãy số vẽ "3 8 5 1 6 4 2" (forward) | specgram forward | crop 30–42s | Phần đọc bằng mắt |
| speech_formants_proof.png | Vùng 0–4kHz là GIỌNG NÓI (fundamental+formant) | specgram low-freq | crop 0.9–4s | Chứng minh 2 vùng speech |
| speech1_clean.wav | Vùng speech 1 (0–22s) đã lowpass, cần nghe | FFT lowpass 3.8kHz→16kHz | analyze.py | Để nghe lấy phần còn lại |
| speech2_clean.wav | Vùng speech 2 (42–51s) đã lowpass, cần nghe | như trên | analyze.py | Để nghe lấy phần còn lại |

## Đã giải (tái lập được)

- **Morse @11.6kHz (6–16s):** `python solve/analyze.py` → **`R3QU1RES`** (all-uppercase → khả năng là **phần 4**). Timing sạch: dot=80ms, dash=250ms, gap chữ=260ms.
- **Spectrogram text (đảo audio, ~24–30s):** **`Pr0c3ss1ng`**
- **Spectrogram digits (forward, ~31–41s):** **`3851642`**
- **Spectrogram text (forward, dải cao 26–33kHz, ~44–47s):** **`31337`**

## Còn thiếu (BLOCKED offline)

- Hai vùng **giọng nói** (0–22s và 42–51s, băng 0–4kHz, bị phủ nhiễu rộng tới 48kHz) đọc ra các phần flag còn lại. Cần **nghe/ASR** — môi trường hiện tại không có audio playback/ffmpeg/whisper. Clip đã tách sẵn: `speech1_clean.wav`, `speech2_clean.wav`.

## Ghi chú xác minh

Chưa đủ 6 phần → **KHÔNG kết luận flag**. Trạng thái: needs_verification.
Artifact gốc: `files/BabyRF.wav` — SHA-256 `f0ff1d468102ff294c8d7f66b8977f8de273252ae97b0973d23aece825ed87dd`
