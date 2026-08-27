# image_fetcher - LIT CTF 2026 (Web)

## 1. Yêu cầu bài toán
Khai thác lỗ hổng hoặc thu thập thông tin từ trang web challenge để lấy flag.

## 2. Kiến thức nền tảng
- Web protocols, SSRF, HTTP Headers, Cookies, Source Code inspection, Data decoding.

## 3. Quá trình phân tích & Giải
- Exploited SSRF on /fetch endpoint to scan localhost ports 5000-6000. Found open port 5267 containing the flag.

## 4. Xác minh Flag
- Flag: LITCTF{55rf_p0r7s_8e52df31}
