# faulty_image_1_haha — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
> haha Someone tampered with an image haha, and now we can't view it haha!
> Help the LIT team recover the image haha!

File đề: `corrupt.png` (400×150). Ảnh chứa flag nhưng mở lên bị lỗi. Nhiệm vụ: sửa file để xem lại ảnh.

## 2. Kiến thức nền

**Cấu trúc PNG.** Một file PNG gồm:
- 8 byte chữ ký: `89 50 4E 47 0D 0A 1A 0A`.
- Chuỗi **chunk**, mỗi chunk = `length(4) | type(4) | data(length) | CRC(4)`.
  - `IHDR`: width, height, bit depth, color type... (color type 2 = RGB).
  - `IDAT`: dữ liệu điểm ảnh đã nén bằng **zlib/DEFLATE**.
  - `IEND`: kết thúc.
- CRC là mã kiểm tra toàn vẹn của mỗi chunk.

**Cách ảnh được nén.** Các scanline (mỗi dòng có 1 byte filter + width×channels byte màu) được ghép lại rồi nén zlib. Ảnh 400×150 RGB ⇒ raw = `150 × (1 + 400×3) = 180150` byte.

**Ý nghĩa "tampered".** Nếu vài byte trong luồng nén bị đổi/chèn, zlib sẽ báo lỗi và không giải nén được ⇒ không xem được ảnh.

## 3. Quá trình phân tích
1. **Parse chunk + kiểm CRC:** IHDR hợp lệ (400×150, RGB). **IDAT có CRC sai** và **thiếu IEND** ở vị trí chuẩn.
2. **Thử giải nén IDAT:** zlib báo `invalid literal/lengths set` ngay ở ~byte 116 ⇒ luồng nén bị hỏng sớm.
3. **Tìm dấu vết tamper:** đề lặp từ "haha". Tìm chuỗi byte `68 61 68 61` ("haha") trong file → xuất hiện tại các offset **100, 204, 308, 412, …** cách đều nhau **104 byte**.
   → Kết luận: kẻ tấn công **chèn 4 byte "haha" sau mỗi 100 byte** dữ liệu gốc (bước nhảy 104). Chính các "haha" này phá luồng DEFLATE.

## 4. Lý do chọn kỹ thuật
Corruption có **quy luật đều đặn** (mỗi 104 byte) và marker rõ ràng ("haha"). Vì đây là **chèn thêm** byte (không phải ghi đè mất dữ liệu), ta có thể **đảo ngược hoàn hảo** bằng cách gỡ đúng các byte đã chèn — không mất mát thông tin gốc.

## 5. Các bước khai thác / giải
1. Duyệt file: giữ 100 byte, nếu 4 byte tiếp theo là `"haha"` thì **bỏ**, lặp lại đến hết.
2. Sau khi gỡ, IDAT (length gốc 2155) **giải nén sạch** ra đúng 180150 byte.
3. Đóng gói lại thành PNG hợp lệ (IHDR + IDAT + IEND với CRC đúng) và mở bằng trình xem ảnh.

```python
d=open('corrupt.png','rb').read()
out=bytearray(); i=0
while i<len(d):
    out+=d[i:i+100]; i+=100
    if d[i:i+4]==b'haha': i+=4
# out là PNG gốc; IDAT decompress OK -> render ra ảnh chứa flag
```
Solver đầy đủ: `../solve/solve.py`. Ảnh khôi phục: `../solve/evidence/recovered.png`.

## 6. Cách xác minh flag
- Raw giải nén dài đúng **180150** byte = `150×(1+400×3)` → đúng kích thước ảnh 400×150 RGB.
- Chạy lại solver luôn cho ra **cùng một** ảnh (tất định).
- Mở ảnh đọc được flag; phóng to (`flag_zoom.png`) để xác nhận từng ký tự.

## 7. Flag
```
LITCTF{y0u_f1x3d_m3_85hf91j!}
```
Nội dung "you fixed me" xác nhận đúng hướng: ta đã *sửa* lại file.

## 8. Bài học & lỗi thường gặp
- **Đọc kỹ đề:** từ "haha" lặp lại chính là marker của byte được chèn — manh mối lộ liễu.
- **Phân biệt "chèn" vs "ghi đè":** chèn thì đảo ngược được hoàn hảo; ghi đè thì mất dữ liệu. Ở đây khoảng cách đều 104 và marker cố định ⇒ chắc chắn là chèn.
- **Đừng hoảng vì zlib lỗi:** lỗi giải nén thường do vài byte sai. Hãy soi cấu trúc chunk, CRC và tìm mẫu bất thường trước.
- **Byte nén của vùng màu phẳng có thể lặp lại** (ví dụ `70 83 60 01` lặp) — đó là bình thường, đừng nhầm là corruption.
- Kích thước raw sau giải nén là "checksum tự nhiên": khớp `h×(1+w×channels)` nghĩa là cấu trúc ảnh đúng.
