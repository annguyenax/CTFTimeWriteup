# world_cup_chat - LIT CTF 2026 (Web)

## 1. Yêu cầu bài toán
Khai thác lỗ hổng hoặc thu thập thông tin từ trang web challenge để lấy flag.

## 2. Kiến thức nền tảng
- Web protocols, SSRF, HTTP Headers, Cookies, Source Code inspection, Data decoding.

## 3. Quá trình phân tích & Giải
- Decoded HTML entities and subtracted the offset of 67 from each decimal value to get ASCII text.

## 4. Xác minh Flag
- Flag: LITCTF{ent1ty_m4g1c_1fj10d}
