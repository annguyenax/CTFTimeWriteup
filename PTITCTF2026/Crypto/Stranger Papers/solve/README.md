# Stranger Papers — SOLVED

**Flag:** `PTITCTF{21.0286_105.8356}`

## Cách chạy

1. Chuỗi ciphertext đã có sẵn: `..\notes\seq.txt` (dòng 1, 502 ký hiệu A..V).
2. Build corpus tiếng Việt (nếu chưa có): scrape `vi.wikipedia.org`, bỏ dấu, lưu `vi_corpus.txt` cạnh `solve.py`.
3. `python solve.py` → in ra key + plaintext tiếng Việt.

## Tóm tắt

- 502 ảnh → 22 unique → substitution đơn bảng.
- Plaintext là **tiếng Việt không dấu** (22 chữ, không f/j/w/z) — không phải tiếng Anh.
- Quadgram tiếng Việt + simulated annealing phá substitution.
- Plaintext tả **Văn Miếu – Quốc Tử Giám** → tọa độ `21.0286, 105.8356`.

## File

- `solve.py` — solver substitution tiếng Việt (cần `vi_corpus.txt`).
- `plaintext.txt` — plaintext đã giải (bỏ dấu).
