# RSA Eclipse — Writeup (L3akCTF 2026, crypto)

- **Flag:** `L3AK{Th3_P3numbr4_H1d35_Th3_Fl4w_In_Th3_Mers3nne_V01d}`
- **Trạng thái:** ✅ Verified (`p·q == N` xác định + flag ASCII đúng khung)
- **Điểm/Solves:** 68 / 166 (dễ nhất nhóm crypto)
- **File:** `files/crypto_rsa-eclipse.tar.gz` → `chall.py`, `output.txt`

---

## 1. Đề bài yêu cầu gì

RSA "bình thường": `N = p·q`, `e = 65537`, mã hóa flag `c = m^e mod N`. `chall.py` chỉ ràng buộc:
```python
assert p.bit_length() == 607
assert q.bit_length() == 521
```
Tức hai prime **lệch cỡ** (607-bit và 521-bit). Nhiệm vụ: phân tích N để giải RSA.

## 2. Kiến thức nền

- **RSA:** biết `p, q` → `d = e⁻¹ mod (p−1)(q−1)` → `m = c^d mod N`.
- **Prime dạng Mersenne-ish:** prime gần lũy thừa 2, `p = 2ⁿ − a` với `a` nhỏ. Khi cả hai prime đều dạng này, `N` có **cấu trúc lộ liễu** trong biểu diễn nhị phân → phân tích được ngay, không cần thuật toán factoring nặng.

## 3. Phân tích — nhìn N ở dạng hex

Xuất N ra hex thấy mẫu rõ rệt:
```
ffffffff...ffff c957 ffff...ffff ea22 0000...0000 4ab2db
```
Chuỗi dài bit 1 (0xFF) ở đầu ⇒ N rất gần `2^1128` ⇒ cả `p, q` gần lũy thừa 2. Đặt:
```
p = 2^607 − a,   q = 2^521 − b     (a, b nhỏ)
N = p·q = 2^1128 − b·2^607 − a·2^521 + a·b
```

## 4. Lý do chọn kỹ thuật & các bước

Mọi số hạng trừ `a·b` đều là bội của `2^521`, nên:
```
N mod 2^521 = a·b          → a·b = 4895451  (nhỏ, lấy chính xác)
```
Và `2^1128 − N` bị chi phối bởi `b·2^607`, nên:
```
b ≈ (2^1128 − N) >> 607 = 1749
a = (a·b) / b = 4895451 / 1749 = 2799
```
Dựng lại `p = 2^607 − 2799`, `q = 2^521 − 1749`, kiểm tra `p·q == N` ✓, rồi giải RSA.

Solver: [solve/solve.py](../solve/solve.py). Chạy:
```bash
python solve/solve.py
# a=2799 b=1749 ; p*q==N: True ; flag: L3AK{...}
```

## 5. Cách xác minh flag

- `p·q == N` đúng **chính xác** (assert pass) ⇒ `p, q` là thừa số thật, không phải đoán.
- Flag giải ra ASCII sạch, đúng `L3AK{...}`, nội dung có nghĩa: *"The penumbra hides the flaw in the Mersenne void"* — xác nhận đúng ý đồ (prime kiểu Mersenne).

## 6. Bài học & lỗi thường gặp

- **Luôn nhìn N ở hex/binary** khi nghi RSA "lạ": chuỗi dài 0xFF/0x00 ⇒ prime gần lũy thừa 2 ⇒ phân tích cấu trúc, đừng phí thời gian ECM/Fermat.
- **Fermat KHÔNG chạy** ở đây (p, q lệch cỡ ~2^86, rất xa nhau) — đừng mặc định thử Fermat cho mọi RSA.
- **Mẹo modulo:** với `p=2ⁿ−a, q=2ᵐ−b` (m<n), `N mod 2ᵐ = a·b` cho ngay tích các phần nhỏ; phần cao của `2^(n+m)−N` cho `b`.
- Đừng tin file `solve/` có sẵn: bản cũ chỉ tạo `pub.key` (không phải lời giải) — phải tự kiểm chứng.

## 7. Đường đi nhanh lần sau

RSA + N toàn 0xFF ở đầu ⇒ đặt `p=2^bp−a, q=2^bq−b`, lấy `a·b = N mod 2^bq`, `b = (2^(bp+bq)−N)>>bp`. ~2 phút.
