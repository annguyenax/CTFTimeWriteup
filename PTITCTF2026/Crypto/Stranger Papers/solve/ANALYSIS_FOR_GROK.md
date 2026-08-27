# Stranger Papers — phân tích & lời giải (cho grok)

Theme: Stranger Things / Hawkins Lab 1983. Zip 502 ảnh (455 jpg + 47 HEIC), **chỉ 22 ảnh unique (22 hash)**.

## Mô hình (đã xác định chắc — xem notes/SESSION.md)
- Chuỗi 502 ảnh = **ciphertext trên bảng chữ 22 ký hiệu** (`notes/seq.txt`, nhãn first-seen A=U00…V=U21).
- Mỗi glyph = 1 chữ/số vẽ to trên giấy rồi gấp (chỉ thấy nét mép) — **KHÔNG cần OCR ảnh gấp**.
- **IC = 0.078 → substitution đơn bảng (monoalphabetic), gần English.** 22 symbol = English thiếu ~4 chữ hiếm.
- Tần suất: U06=70 (>) U03=67 U05=46 U02=41 U00=39 U07=39 U12=34 U01=32 ... → U06/U03 ~ 'E'/'T'/space.

## Lời giải: crack substitution tự động trên seq.txt
Không cần đụng ảnh nữa. Chạy **hill-climbing với English quadgram scoring** map 22 glyph → chữ cái.

```python
# 1) load ciphertext (chuỗi 502 nhãn A..V trên 1 dòng)
ct = open("notes/seq.txt").read().split("\n")[0].strip()   # A..V, mỗi ký tự 1 glyph
# 2) English quadgram log-prob (tải file english_quadgrams.txt, hoặc dùng lib 'ngram_score')
#    hoặc dùng thư viện: pip install cipher-solver / hoặc quipqiup online.
# 3) hill-climb: khởi tạo key ngẫu nhiên (22 glyph -> 22 chữ), swap 2 chữ, giữ nếu score tăng,
#    random restart nhiều lần. Bảng chữ đích = 26 chữ (glyph chỉ dùng 22, 4 chữ English hiếm bỏ).
```
**Cách nhanh nhất:** dán `seq.txt` (đã map A..V) vào **quipqiup.com** (auto substitution solver) — nó xử monoalphabetic 502 ký tự dễ dàng. Nếu có space (U06 nếu là space) thì tách từ trước khi dán.

## Lưu ý quan trọng
- Kiểm tra U06 (freq 70, cao bất thường): nếu là **space** thì plaintext có phân từ → quipqiup ăn ngay.
  Nếu không, để continuous, hill-climb quadgram vẫn ra.
- Plaintext là văn bản English (nhật ký Hawkins) chứa **toạ độ** + flag `PTITCTF{...}`.
  Flag có thể là 1 đoạn viết hoa/format riêng trong plaintext → sau khi giải substitution, tìm PTITCTF hoặc toạ độ.
- 502 = 2×251: không phải lưới; đừng cố transposition. Đây thuần substitution.

## Nếu hill-climb ra English nhưng flag "lạ"
- Có thể flag nằm ở phần toạ độ (số) — glyph số cũng nằm trong 22 symbol. Map cả chữ+số.
- Cross-check bằng cách OCR 1-2 glyph unique dễ đọc (mở `notes/unique/U06_*.jpg`) để neo 1-2 ánh xạ, tăng tốc hill-climb.
