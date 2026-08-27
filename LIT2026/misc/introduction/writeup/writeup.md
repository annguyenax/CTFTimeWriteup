# introduction - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Tìm cờ từ file helloworld.txt (nếu có cung cấp) hoặc chuỗi trong challenge.

## 2. Kiến thức nền tảng
- ROT13: Phép mã hóa thay thế Caesar với bước nhảy 13.

## 3. Quá trình phân tích & Giải
- File helloworld.txt chứa chuỗi YVGPGS{J3yp0z3_G0_Y1GPGS}.
- Nhận thấy YVGPGS lệch đúng 13 ký tự so với LITCTF. Giải ROT13 chuỗi này ta nhận được cờ.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- cat helloworld.txt | tr 'a-zA-Z' 'n-za-mN-ZA-M'

## 5. Xác minh Flag
- Flag: LITCTF{W3lc0m3_T0_L1TCTF}
