# faulty_image_2 — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
> An anonymous user challenged the LIT team to find their identity, but they only
> sent us this image. Can you help us reveal them?

File: `corrupt2.png` (400×150). Cần "lộ diện" danh tính ẩn — tức tìm flag giấu trong file.

## 2. Kiến thức nền
- **PNG chunk & chunk phụ (ancillary).** Ngoài IHDR/IDAT/IEND, PNG cho phép các
  chunk phụ như `tEXt` (metadata text dạng `keyword\0value`). Tên chunk có thể tuỳ biến;
  chữ **thường ở byte đầu** = ancillary (không bắt buộc để hiển thị). Trình xem ảnh
  **bỏ qua** chunk lạ hoặc chunk có CRC sai → nơi lý tưởng để giấu dữ liệu.
- **XOR lặp khóa (repeating-key XOR).** `plain = cipher XOR key` với key lặp.

## 3. Quá trình phân tích
1. **Parse chunk:** IHDR (400×150 RGB) ok; **IDAT nguyên vẹn** (CRC đúng);
   thêm `tEXt` (CRC đúng) và một chunk lạ **`tIGr`** với **CRC sai** (cờ đỏ) rồi IEND.
2. **Render IDAT:** ảnh chỉ ghi *"Nothing here lol!"* → ảnh nhìn thấy là **mồi nhử**,
   flag không nằm ở pixel.
3. **Đọc tEXt:** `XOR-Key = 636f64657469676572`. Chuỗi hex này decode ra **"codetiger"**.
   (Tên chunk `tIGr` cũng ám chỉ *tiger* — nhất quán.)
4. **Phân tích tIGr (60 byte):** 4 byte đầu `00 00 00 20` = **length prefix** big-endian
   (0x20 = 32). Phần thân 32 byte tiếp theo là ciphertext.

## 4. Lý do chọn kỹ thuật
- CRC sai + tên chunk lạ = tín hiệu kinh điển "dữ liệu giấu ở đây".
- tEXt cung cấp thẳng "XOR-Key" ⇒ phép giải là XOR lặp khóa.
- Thử XOR từ byte 0 ra rác, nhưng bỏ 4 byte length đầu thì `tIGr[4:]` XOR "codetiger"
  cho ngay `LITCTF{` ⇒ xác nhận offset đúng.

## 5. Các bước giải
```python
# lấy tEXt -> key 'codetiger'; lấy tIGr -> [len=32][ciphertext]
key=b'codetiger'
n=struct.unpack('>I',tigr[:4])[0]         # 32
body=tigr[4:4+n]
flag=bytes(body[i]^key[i%len(key)] for i in range(n)).rstrip(b'\\x00')
```
Solver: `../solve/solve.py`.

## 6. Cách xác minh flag
- Length prefix (32) khớp số byte đã mã hoá (31 ký tự flag + 1 null padding).
- **Round-trip:** XOR lại kết quả với key tái tạo **đúng** thân `tIGr`.
- Flag kết thúc bằng `}`.

## 7. Flag
```
LITCTF{c0d3t1g3r_w4s_h3r3_x0r!}
```

## 8. Bài học & lỗi thường gặp
- **Đừng chỉ nhìn ảnh:** IDAT có thể là mồi nhử; hãy **liệt kê mọi chunk**, đặc biệt
  chunk lạ / CRC sai — đó thường là kho chứa dữ liệu ẩn.
- **tEXt hay lộ khóa/manh mối.** Value có thể là hex → nhớ decode.
- **Chú ý header/length prefix** trong payload: XOR từ byte 0 ra rác không có nghĩa
  sai khóa — có thể cần bỏ vài byte tiêu đề trước.
- Xác minh bằng **round-trip + length + dấu `}`**, không đoán bằng mắt.
