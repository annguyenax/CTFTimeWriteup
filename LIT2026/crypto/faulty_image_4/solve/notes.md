# faulty_image_4 — WORKING NOTES (status: PAUSED / unsolved)

> Chưa tái lập được flag thật. KHÔNG kết luận flag. Đây là bài khó nhất của series.

## Đề
- corrupt4.png (500×200 RGB, 241941 bytes, 4×IDAT, ảnh gần như không nén = nhiễu).
- "The flag you see isn't the flag you want... again. This time, the hacker
  corrupted some of the pixels, separating them from encoding information
  together as a whole."
- **Decoy nhìn thấy:** `LITCTF{fau1ty_I0uR_12ox!}` (vẽ chữ vàng trên nền nhiễu). Decoy = flag GIẢ.

## Quan sát
- Cấu trúc PNG hợp lệ (CRC ok), không tEXt/không chunk lạ, không dữ liệu sau IEND.
- Nền là **nhiễu mượt có tương quan không gian** (mean-abs-diff pixel kề ~17 « nhiễu trắng ~60)
  → nhiễu KHÔNG bị shuffle (loại giả thuyết hoán vị pixel).
- Kênh: R[30,199], G[20,198], B[0,90]. B hẹp vì decoy vàng đặt B≈0 tại chữ (đã giải thích, không phải lead).
- **Filter bytes (200 dòng) chỉ gồm {1,2}** — bất thường, nghi mã hoá nhị phân, NHƯNG:
  25 byte giải ra rác cho cả 4 ánh xạ (1/2→bit × MSB/LSB); tìm mẫu bit "LITCTF" ở mọi
  offset → KHÔNG có. → filter bytes không chứa flag ASCII trực tiếp.

## Đã thử và LOẠI TRỪ (chỉ hiện decoy hoặc nhiễu)
- 24 bit-plane (R/G/B × bit0..7); chỉ bit7 R/G có decoy.
- LSB bytestream kiểu zsteg: kênh R/G/B/RGB-interleaved × bit0..2 × hàng/cột × MSB/LSB → không có "LITCTF".
- Block-average mặt phẳng bit0 (phát hiện chữ vẽ ở LSB) → nhiễu đều 0.5, không chữ.
- Tổ hợp kênh: XOR (R^G, R^B, G^B, R^G^B), hiệu tuyệt đối/có dấu, tổng, parity LSB → chỉ decoy.
- So sánh kênh (R>G, G>B, R>B, B>R, ...) → chỉ decoy.
- Blur/high-pass (Gaussian)/histogram-equalize từng kênh → chỉ decoy; B luôn nhiễu.
- FFT magnitude từng kênh → chỉ biên tần số của decoy, không chữ ẩn.
- Render bỏ filter (None) → nhiễu residual màu.
- Pixel cực trị (==0/==255), pixel bất biến (R==G==B, low channel-std) → chỉ decoy.
- Periodicity (row/col shift) → không tuần hoàn. strings/trailing/tEXt → không có.

## Giả thuyết còn lại (NEXT STEPS)
1. **Encoding "together as a whole"**: kết hợp bit từ R+G+B của cùng pixel để tạo 1 byte/char
   theo một sơ đồ bit-split cụ thể (thử nhiều hoán vị bit R/G/B → byte, đọc N pixel đầu/hàng cụ thể).
2. **Filter bytes {1,2} nhưng XOR-encrypted**: thử XOR 25 byte suy từ filter với key ứng viên
   (decoy string, "codetiger", "haha", tên đề) — series này thích XOR.
3. Nhiễu là **random field từ PRNG có seed**: nếu tái tạo được nền (brute seed numpy/python),
   XOR ảnh − nền → lộ pixel flag. Cần xác định generator/seed (chưa có manh mối seed).
4. Xem lại có phải mỗi pixel = 1 ký tự qua công thức (vd (R+G+B) hoặc R*k+G) tại vùng/hàng cụ thể.
5. Cân nhắc zsteg thật (Kali/HexStrike) để quét tổ hợp bit/thứ tự rộng hơn tự động.

## Nguyên tắc
Không ghi flag cho tới khi có giải mã xác định. Decoy KHÔNG phải đáp án. Bài PAUSED.
