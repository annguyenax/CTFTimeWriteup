# Debug — Writeup (HTB Try Out / Hardware)

## 1. Tổng quan / Overview

- **Challenge:** Debug (Hardware, easy) — HTB Try Out (nguyên gốc Cyber Apocalypse 2023).
- **File:** `hw_debug.zip` → `hw_debug.sal` — capture logic analyzer **Saleae Logic 2**.
- **Mô tả:** một chảo vệ tinh bị lỗi; có tín hiệu serial trong chuỗi boot. Cần decode
  tín hiệu để tìm nguồn nhiễu → tìm flag.

## 2. Triage

- `.sal` thực chất là một **zip**: chứa `meta.json` + `digital-N.bin`.
- `meta.json` cho biết: thiết bị **Logic 8**, tốc độ **25 MS/s**, bật 2 kênh digital
  **TX (0)** và **RX (1)**, thời lượng 37.47 s.
- Có 2 kênh digital (TX/RX) → gợi ý giao thức **UART / Async Serial**.
- Các file `digital-*.bin` dùng **format nội bộ type=100** (mipmap render) của Logic 2,
  không phải export công khai (type=0), nên khó parse thô bằng tay.

## 3. Phân tích / Analysis

- Vì có kênh RX và mô tả "serial signal", sử dụng analyzer **Async Serial**.
- **Tính baud rate:** quan sát chu kỳ bit nhỏ nhất trong tín hiệu ≈ **8.68 µs**
  → `1 / 8.68e-6 ≈ 115200` bit/s. (Tại 25 MS/s, mỗi bit ≈ 217 mẫu.)
- Cấu hình Async Serial: **Baud = 115200, Data = 8, Parity = None, Stop = 1** trên kênh RX.
- Decode ra được log boot của thiết bị; trong log có flag được phân bố trong chuỗi text.

## 4. Exploit

Cách làm chuẩn:
1. Mở `hw_debug.sal` trong **Saleae Logic 2**.
2. Thêm **Async Serial** analyzer, chọn kênh **RX**, Baud **115200**, 8N1.
3. Đọc **Terminal** pane → log boot; ghép các phần text chứa `HTB{...}`.

Cách tự động (Python): `solve/solve.py` parse export digital binary (type 0) của kênh
RX, lấy mẫu UART 8N1 @ 115200 từ danh sách cạnh, giải mã thành chuỗi ASCII.

## 5. Flag

```
HTB{547311173_n37w02k_c0mp20m153d}
```

## 6. Bài học / Lessons

- File `.sal` của Saleae là zip; đọc `meta.json` để biết tốc độ mẫu, kênh và giao thức.
- Cách tính nhanh baud rate: đo chu kỳ bit nhỏ nhất trong sóng → `1 / period`.
- Kênh RX + dữ liệu serial → Async Serial 8N1, thử baud 115200 trước.
- Format nội bộ (type=100) khác export (type=0); dùng Logic 2 để export raw nếu cần parse thủ công.
- Flag không nằm trong chuỗi ASCII thô của .bin; phải decode đúng giao thức mới thấy.
