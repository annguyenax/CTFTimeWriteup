# call me — Writeup (Kali Team CTF 26 / Misc)

## 1. Đề bài yêu cầu gì?

- File: `signal_037.wav`
- Prompt: *"so ezzz"* (author SHADOW / LinkedIn `ali-hloul`)
- Flag: `KaliTeam{...}`

## 2. Kiến thức nền

| Khái niệm | Vai trò |
|---|---|
| Spectrogram (FFT theo thời gian) | Nhìn chữ ẩn trong tần số |
| Morse (CW on/off) | Thông điệp gợi ý |
| Leetspeak | Đọc flag dạng S1gn4l, h34rd, ... |

## 3. Phân tích

- WAV PCM mono 16-bit, 44100 Hz, ~47 s.
- **0–15 s:** năng lượng rải trên dải tần (không phải Morse) → vẽ chữ trên spectrogram.
- **~16–47 s:** âm ~**800 Hz** bật/tắt → Morse.

### Morse (unit ≈ 80 ms)

`	ext
VVV VVV NEXT CHECK MY LINKEDIN TO GET PART2
`

### Spectrogram (0–15 s)

Đọc được rõ:

`	ext
KaliTeam{S1gn4l_h34rd_l0ud_4nd_c134r_part2}
`

Leetspeak: *Signal heard loud and clear part2*.

## 4. Vì sao chọn spectrogram?

| Giả thuyết | Kết quả |
|---|---|
| DTMF phone | Không ổn định / không ra flag |
| Morse only | Chỉ ra hướng dẫn LinkedIn |
| **Spectrogram text** | Flag đầy đủ |
| LSB stego | Không có chuỗi có nghĩa |

## 5. Các bước

1. Mở WAV bằng Audacity / Sonic Visualiser (spectrogram) **hoặc** script FFT → PNG.
2. Đọc chữ ở đoạn đầu file.
3. (Tuỳ chọn) Decode Morse 800 Hz để thấy gợi ý LinkedIn.

## 6. Solver

`solve/solve.py` — tạo `evidence/spectrogram_flag.png`.

`ash
python solve/solve.py
`

## 7. Xác minh

- Ảnh spectrogram lưu trong `solve/evidence/`.
- Flag khớp trực quan trên ảnh (không suy diễn).

## 8. Bài học

| Lỗi | Ghi chú |
|---|---|
| Chỉ decode Morse | Bỏ lỡ flag trên spectrogram |
| DTMF cứng nhắc | "call me" dễ đánh lừa |
| Ngưỡng Morse sai | unit phải ~80 ms (không lấy spike 10 ms) |

## 9. Một dòng

**Chữ flag vẽ trên spectrogram 0–15 s; Morse 800 Hz chỉ gợi ý LinkedIn/part2.**