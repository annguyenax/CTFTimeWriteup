# Sơn Tùng M-TP (re-exam)

## Kết quả

**Chưa solve.** Không nộp flag khi board còn số lần thử hạn chế.

Spectrogram siêu âm **không phải flag**. Nó vẽ đúng:

```text
PTITCTF{n1c3_try_ju57_try_h4rd3r_i_gu355}
```

(“nice try just try harder i guess”). Writeup cũ ghi `PTITCTF{N0T_JUST_MUSIC_BUT_A_MASTERPIECE}` là **đọc nhầm glyph** trên cùng một ảnh — chuỗi đó không có trong phổ.

## Artefact

- `files/Forensics - Sơn tùng M-TP.7z`: SHA-256 `40d74ae84433c3c28579b117b3709231bf444e92905bffa996bc06e1c1b2d5cd`
- `chall.wav`: SHA-256 `01a78ea1b28d71ca2b955d11048427e3acfe4d72ce6cfb15eb7e7581204dc713`
- RIFF/WAVE: stereo PCM 16-bit, 48 kHz, 245.6588125 s; chỉ `fmt ` + `data`

## Decoy

T = 1.7–19.2 s, 15.2–18.85 kHz, cả hai kênh (mid). Time-reverse chỉ lật gương cùng chuỗi. Residual sau khi trừ **Hãy Trao Cho Anh** (MV `knW7-x7Y7RE`, NCC ≈ 0.995, offset +12.340 s) vẫn chỉ còn banner đó.

Cover: tempo-median ≈ 95.7 BPM, dài 4:06 — khớp Hãy Trao Cho Anh, không khớp 128 BPM (harmonic giả của beat tracker).

## Đã loại

LSB/entropy max, không magic zip/png; Morse/SSTV/phase/QR; không banner phổ nào khác trên toàn bài; RIFF không chunk ẩn.

## Việc còn lại

Lớp thật chưa tách được. Residual so với AAC 128 kbps YouTube còn ~−20 dB noise theo mix — payload rất nhỏ có thể bị che. Cần bản lossless cùng mix, hoặc hướng khác ngoài phổ/LSB.
