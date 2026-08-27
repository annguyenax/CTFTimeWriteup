# double_disguise — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
> Oopps, I accidentally ran an encryption program on my flag. Now I only have:
> **`ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==`**
> Can you help me [recover] the original flag?

Nhiệm vụ: khôi phục flag từ chuỗi mã hoá trên.

## 2. Kiến thức nền

**Base64.** Cách mã hoá **nhị phân → văn bản** bằng bảng 64 ký tự `A–Z a–z 0–9 + /`. Dấu hiệu nhận biết rất mạnh:
- Chỉ gồm các ký tự trong bảng đó,
- Kết thúc bằng `=` hoặc `==` (padding),
- Độ dài là bội số của 4.
Chuỗi `...9aVw==` khớp cả ba dấu hiệu → gần như chắc chắn là Base64.

**XOR một byte (single-byte XOR).** Mỗi byte plaintext được XOR với **cùng một** byte khóa `k`: `c = p ^ k`. Vì XOR đối xứng nên `p = c ^ k`. Nếu biết một đoạn plaintext (ở đây là tiền tố flag `LITCTF{`), ta lấy `k = c ^ p` cho từng vị trí; nếu tất cả ra **cùng một giá trị** thì đúng là single-byte XOR và ta có ngay khóa.

**"double disguise" = hai lớp nguỵ trang.** Base64 chỉ là *mã hoá* (ai cũng giải được), nên nó chỉ là lớp ngoài; bên trong còn một lớp *mã hoá thật* — đây là XOR.

## 3. Quá trình phân tích
1. Nhìn hình dạng chuỗi → nghi Base64 → giải Base64 ra 22 byte:
   `66 63 7e 69 7e 6c 51 6c 1b 4c 4b 75 7d 1a 58 46 4e 75 49 5f 5a 57`.
   Các byte này **không** phải văn bản đọc được → còn một lớp nữa (khớp "double").
2. Áp known-plaintext: XOR 22 byte đầu với `LITCTF{`:
   `raw[i] ^ 'LITCTF{'[i]` → `[42, 42, 42, 42, 42, 42, 42]` — **hằng số 42**.
   → single-byte XOR với khóa `0x2A` (42, ký tự `*`).
3. XOR toàn bộ 22 byte với 42 → ra flag đọc được.

## 4. Lý do chọn kỹ thuật
- Hình dạng chuỗi ⇒ Base64 là bước đầu bắt buộc.
- Sau Base64 vẫn là byte "rác" ⇒ còn một phép biến đổi. Với known-plaintext `LITCTF{`, thử **single-byte XOR** là rẻ nhất; việc các key byte trùng nhau xác nhận giả thuyết ngay lập tức.

## 5. Các bước giải
```python
import base64
raw = base64.b64decode('ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==')  # lớp 1
key = raw[0] ^ ord('L')                                     # = 0x2A
flag = bytes(b ^ key for b in raw).decode()                # lớp 2
print(flag)  # LITCTF{F1fa_W0rld_cup}
```
Solver đầy đủ: `../solve/solve.py`.

## 6. Cách xác minh flag
Xác minh mạnh bằng **mã hoá lại**: XOR flag với `0x2A` rồi Base64 phải cho ra **đúng** chuỗi gốc.
```
python solve.py
# xor key = 42 (0x2a)
# flag    = LITCTF{F1fa_W0rld_cup}
# round-trip re-encryption OK
```

## 7. Flag
```
LITCTF{F1fa_W0rld_cup}
```

## 8. Bài học & lỗi thường gặp
- **Nhận diện Base64 qua hình dạng** (charset + padding `=` + bội số 4). Đừng nhầm Base64 là "mã hoá an toàn" — nó chỉ là encoding.
- **Sau khi giải Base64 mà vẫn là byte rác → còn lớp nữa.** Tên đề "double" là gợi ý số lớp.
- **Known-plaintext là vũ khí mạnh:** biết `LITCTF{` đủ để lộ khóa XOR ngay. Nếu các key byte đồng nhất → single-byte XOR; nếu lặp theo chu kỳ → repeating-key XOR (Vigenère byte).
- Luôn **xác minh bằng round-trip** thay vì tin vào "trông giống flag".
