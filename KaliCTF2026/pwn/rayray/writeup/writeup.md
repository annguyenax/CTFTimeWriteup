# rayray — Writeup (Kali Team CTF 26 / Pwn)

## 1. Đề bài yêu cầu gì?

- Binary PIE 64-bit + libc/loader + `flag.txt` mẫu.
- Prompt: *"I like hiding in a random pattern or is it ??"*
- In flag dạng `KaliTeam{...}` (local package: `KaliTeam{fake_flag}`).

## 2. Kiến thức nền

| Khái niệm | Vai trò |
|---|---|
| `srand` / `rand` (glibc) | PRNG quyết định vị trí flag |
| `time(NULL)` làm seed | Đồng bộ theo giây hiện tại |
| Mảng block cố định | Flag nằm đúng 1/100 ô |
| PIE | Không cần leak nếu không ROP |

## 3. Phân tích chương trình

`main` chỉ set buffer rồi gọi `vuln`.

Trong `vuln`:

1. In banner / gợi ý flag bị giấu.
2. Tạo **100 block** (mỗi block 0x40 byte) với chuỗi kiểu  
   `Block %d data: 0x%08X (No flag here)` — dùng `rand()` **trước** khi `srand`.
3. `srand(time(NULL))`.
4. `secret = rand() % 100`.
5. `fopen("./flag.txt")` + `fgets` **đè flag vào `blocks[secret]`**.
6. Hỏi `enter Block number: `, `read` tối đa 15 byte, `atoi`.
7. Nếu index ∈ [0, 99]: in `Reading block …` và `DATA: %s`.

Không cần buffer overflow để lấy flag (intended path).

## 4. Vì sao chọn dự đoán PRNG?

| Giả thuyết | Kết luận |
|---|---|
| Đoán bừa 0–99 | 1% — không đáng |
| BOF/ROP vì PIE | `read` chỉ 15 byte — không đủ overflow |
| **Predict `rand()%100` sau `srand(time)`** | Seed biết được (thời gian) → exact |

## 5. Các bước giải

1. Self-test glibc: `srand(1); rand() == 1804289383`.
2. Lấy `t0` trước khi start process, `t1` sau khi thấy prompt.
3. Với mỗi seed ∈ `[t0-1, t1+1]`, tính `rand()%100`, chọn index phổ biến nhất.
4. Gửi index dạng decimal.
5. Đọc `DATA: KaliTeam{...}`.

Remote: clock skew ±1–2 giây; mở rộng cửa sổ seed nếu cần.

## 6. Solver

`solve/solve.py`

```bash
python3 solve/solve.py
python3 solve/solve.py remote HOST PORT
```

Cốt lõi: class `GlibcRand` (TYPE_3) + `block_index(seed)`.

## 7. Xác minh

Local đã tái lập:

```text
Reading block 32...
DATA: KaliTeam{fake_flag}
```

(`32` phụ thuộc giây chạy; flag package luôn `fake_flag`.)

## 8. Bài học / lỗi hay gặp

| Lỗi | Ghi chú |
|---|---|
| Dùng `random` của Python | Khác glibc hoàn toàn |
| Quên warm-up 310 bước sau `srandom` | Sai toàn bộ chuỗi |
| Seed lệch giây | Thử `t-1..t+1` |
| Nhầm 100 lần `rand` đầu ảnh hưởng secret | Chúng chạy **trước** `srand(time)` |

## 9. Một dòng

**Flag nằm ở `blocks[rand()%100]` sau `srand(time(NULL))` — đoán seed theo đồng hồ, in đúng block.**
