# Dynastic — Writeup (HTB Try Out / Crypto)

## 1. Đề bài yêu cầu gì
Có `source.py` (hàm mã hoá) + `output.txt` (ciphertext). Khôi phục plaintext, bọc `HTB{...}`.

## 2. Kiến thức nền
- **Trithemius cipher** = Caesar nhưng lượng dịch TĂNG theo vị trí: ký tự thứ `i` dịch `+i`.
- Chỉ dịch chữ cái A–Z (`0x41`), ký tự khác (`_ ? !`) giữ nguyên.

## 3. Phân tích
`encrypt`: với alpha, `ech = chr((ord(ch)-0x41 + i) % 26 + 0x41)`; non-alpha giữ nguyên.
→ Đây là dịch cộng dồn theo index i (Trithemius).

## 4. Vì sao hướng này
Mô tả đề ("Roman emperor" = Caesar) + code cho thấy dịch theo vị trí → giải ngược tất định,
không cần brute-force.

## 5. Các bước
1. Đọc ciphertext trong output.txt.
2. Với mỗi alpha ở vị trí i: `plain = chr((ord(c)-0x41 - i) % 26 + 0x41)`; non-alpha giữ nguyên.
3. Kết quả: `DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER`.
4. Bọc `HTB{...}`.

## 6. Flag
```
HTB{DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER}
```
