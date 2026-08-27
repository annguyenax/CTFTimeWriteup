# BabyRF — Writeup (L3akCTF 2026, Beginner/hardware-rf) — ⏸️ PAUSED

- **Trạng thái:** ⏸️ Chưa hoàn tất (4/6 phần đã đọc/giải, 2 phần trong giọng nói cần nghe)
- **Flag:** *chưa kết luận* (thiếu evidence đủ 6 phần — không bịa)
- **Điểm/Solves:** 165 / 30 (khó nhất nhóm Beginner)
- **File:** `files/BabyRF.wav` — 96 kHz, mono, 16-bit, 51.2 s

---

## 1. Đề bài yêu cầu gì

"Cờ vỡ thành nhiều mảnh, gom hết vào file `.wav`. Flag gồm **6 phần** phân biệt hoa/thường; **phần thứ 4 toàn chữ hoa**." Nhiệm vụ: tìm 6 phần trong một file audio đa-mode.

## 2. Kiến thức nền

- **Spectrogram (phổ thời gian–tần số):** nhiều CTF vẽ chữ trực tiếp lên phổ; đọc bằng cách hiển thị spectrogram (Audacity/Sonic Visualiser/matplotlib).
- **Audio đảo ngược (reverse):** chữ vẽ trên audio đã đảo sẽ hiện **lật gương**; đảo lại thời gian là đọc được.
- **Morse OOK:** bật/tắt một tone (ở đây ~11.6kHz) theo dot/dash.
- **Nhận diện giọng nói trên phổ:** dải 0–4kHz có **fundamental (~200Hz) + các formant chuyển động** ⇒ đó là tiếng người, không phải nhiễu.

## 3. Phân tích & tiến trình (state machine tới VERIFY một phần)

Sampling 96kHz (băng tới 48kHz) là dấu hiệu nhồi nhiều tín hiệu. Spectrogram tổng quan cho thấy các "kênh" ở time/freq khác nhau:

| Vùng (forward) | Băng tần | Mode | Kết quả |
|---|---|---|---|
| 6–16 s | ~11.6 kHz | **Morse OOK** | `R3QU1RES` (all-uppercase) |
| 24–30 s | 8–14 kHz | Spectrogram text (**đảo audio**) | `Pr0c3ss1ng` |
| 31–41 s | 8–14 kHz | Spectrogram digits (forward) | `3851642` |
| 44–47 s | 26–33 kHz | Spectrogram text (forward) | `31337` |
| 0–22 s | 0–4 kHz | **Giọng nói** (+ nhiễu phủ) | *cần nghe* |
| 42–51 s | 0–4 kHz | **Giọng nói** (+ nhiễu phủ) | *cần nghe* |

- **Phát hiện chốt:** chữ ở 24–30s ban đầu hiện **lật gương** ⇒ đảo thời gian đoạn đó đọc ra `Pr0c3ss1ng`. Ngược lại `31337` và dãy số đọc đúng ở forward ⇒ mỗi đoạn có hướng riêng.
- **Morse:** giải mã tự động (dot 80ms / dash 250ms) ra `R3QU1RES` — vì toàn hoa nên khả năng là **phần 4**.
- **Vùng "nhiễu":** zoom 0–4kHz lộ rõ fundamental + formant ⇒ là **giọng người đọc flag**, bị phủ nhiễu rộng cho giống RF.

## 4. Cách tái lập phần đã giải

```bash
python solve/analyze.py files/BabyRF.wav
# [Morse @11.6kHz] -> R3QU1RES
# tách speech1_clean.wav, speech2_clean.wav để nghe
```
Các phần vẽ trên phổ: xem ảnh trong `solve/evidence/` (`read_processing_reversed.png`, `read_digits_3851642.png`, `morse_11k6_signal.png`, `speech_formants_proof.png`).

## 5. Vì sao PAUSED (trở ngại thật)

2 phần còn lại nằm trong **giọng nói** (0–22s, 42–51s). Cần **nghe hoặc ASR** để chép lại. Môi trường giải hiện tại **không có audio playback / ffmpeg / whisper** nên không tự transcribe được. Đã tách sẵn `speech1_clean.wav` + `speech2_clean.wav` (đã lowpass 3.8kHz, chuẩn hóa) để nghe.

Theo nguyên tắc **không bịa flag khi chưa tái lập đủ** ⇒ chưa kết luận. Đã có: `R3QU1RES` (P4), `Pr0c3ss1ng`, `3851642`, `31337`.

## 6. Ba bước tiếp theo

1. Nghe `speech1_clean.wav` và `speech2_clean.wav`, chép lại (chú ý hoa/thường, leetspeak).
2. Ghép 6 phần đúng thứ tự (dùng thời gian xuất hiện và gợi ý "phần 4 = R3QU1RES" để căn chỗ), thành `L3AK{p1_p2_p3_R3QU1RES_p5_p6}` (thứ tự cần xác nhận).
3. Kiểm tra ngữ nghĩa/format `L3AK{}` để verify.

## 7. Bài học

- 96kHz + nhiều "kênh" ở tần số khác nhau ⇒ nghĩ tới multi-mode; tách theo băng tần.
- Chữ **lật gương** trên phổ ⇒ đảo audio.
- Vùng trông như "nhiễu" ở 0–4kHz có thể là **giọng nói** bị phủ nhiễu — luôn zoom low-freq kiểm tra formant trước khi bỏ qua.
- Lỗi thường gặp: tưởng vùng nhiễu là filler và bỏ sót 2 phần.
