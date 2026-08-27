# BabyLCG — Writeup (L3akCTF 2026, Beginner/crypto)

- **Flag:** `L3AK{n3v3r_trU5t_b4s1c_LCG5_frfr}`
- **Trạng thái:** ✅ Verified (giải xác định + kiểm tra hồi quy LCG)
- **Điểm/Solves:** 58 / 341 (dễ nhất trong Beginner)
- **File:** `files/beginner_baby-lcg.tar.gz` → `chall.py`, `output.txt`

---

## 1. Đề bài yêu cầu gì

Ban tổ chức chặn được một "script mã hóa tự chế". Nó dùng phép toán cơ bản làm bộ sinh số ngẫu nhiên (RNG) để tạo khóa che flag. Nhiệm vụ: phá RNG đó để lấy lại flag.

Nội dung `chall.py` (rút gọn):

```python
class LCG:
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

m   = <số 256-bit>
rng = LCG(m)
s0 = rng.next(); s1 = rng.next(); s2 = rng.next()   # công khai
key = rng.next()                                     # BÍ MẬT
ciphertext = flag_int ^ key                          # công khai
```

`output.txt` cho ta biết `m, s0, s1, s2, ct`. Ẩn số là `key` (giá trị `next()` thứ 4).

## 2. Kiến thức nền

**LCG (Linear Congruential Generator)** là RNG đơn giản nhất, công thức:

```
state_{n+1} = (a · state_n + c) mod m
```

với `a` (multiplier), `c` (increment), `m` (modulus). Đây **không phải** RNG an toàn mật mã: nếu biết `m` và một vài đầu ra liên tiếp, ta khôi phục được `a`, `c` rồi **dự đoán mọi đầu ra tương lai**.

Kiến thức toán cần: số học modulo và **nghịch đảo modulo** (modular inverse) — với `x` và `m` nguyên tố cùng nhau, tồn tại `x⁻¹` sao cho `x·x⁻¹ ≡ 1 (mod m)`. Python 3.8+ có sẵn `pow(x, -1, m)`.

## 3. Phân tích & lý do chọn kỹ thuật

Ta có hai phương trình đã biết đầy đủ trừ `a, c`:

```
s1 = (a·s0 + c) mod m
s2 = (a·s1 + c) mod m
```

Trừ hai vế để **triệt tiêu `c`**:

```
s2 − s1 = a·(s1 − s0) mod m
⟹ a = (s2 − s1) · (s1 − s0)⁻¹ mod m
```

Có `a` rồi thì `c = (s1 − a·s0) mod m`.

Có `a, c` thì tính được đầu ra thứ 4 chính là khóa:

```
key = (a·s2 + c) mod m
flag_int = ct XOR key
```

Đây là kỹ thuật chuẩn "phá LCG khi biết modulus" — chọn nó vì đề cho lộ trực tiếp `m` cùng 3 đầu ra liên tiếp, đúng điều kiện cần và đủ.

## 4. Các bước khai thác

1. Đọc `m, s0, s1, s2, ct` từ `output.txt`.
2. Tính `a = (s2 − s1)·pow(s1 − s0, −1, m) mod m`.
3. Tính `c = (s1 − a·s0) mod m`.
4. **Kiểm tra**: `a·s0 + c ≡ s1` và `a·s1 + c ≡ s2` (mod m) — nếu sai thì tham số sai.
5. Tính `key = (a·s2 + c) mod m`.
6. `flag = (ct XOR key)` đổi sang bytes.

Solver tối thiểu: xem [solve/solve.py](../solve/solve.py). Chạy:

```bash
python solve/solve.py
# flag = L3AK{n3v3r_trU5t_b4s1c_LCG5_frfr}
```

## 5. Cách xác minh flag

- **Kiểm tra hồi quy:** hai assertion `a·s0+c≡s1`, `a·s1+c≡s2` pass → `a, c` khôi phục đúng (không đoán mò).
- **Kiểm tra ngữ nghĩa:** flag giải ra là ASCII sạch, đúng khung `L3AK{...}`, dài 33 byte khớp độ dài `FLAG` trong `chall.py`, và nội dung có nghĩa: *"never trust basic LCGs frfr"* — chính là bài học của challenge.

## 6. Bài học & lỗi thường gặp

- **Bài học:** LCG (và các RNG tuyến tính) tuyệt đối không dùng làm keystream/mật mã. Biết `m` + 3 output là đủ phá; thậm chí không biết `m` vẫn có thể khôi phục bằng cách lấy GCD của các định thức.
- **Lỗi #1 — dùng nhầm `m`:** `chall.py` hard-code một `m` mẫu, nhưng giá trị **thật** nằm trong `output.txt` (dynamic mỗi lần chạy). Luôn lấy tham số từ output, không từ source.
- **Lỗi #2 — độ dài flag > số byte của m:** flag 33 byte (264 bit) dài hơn `m` (~256 bit), nên `flag_int` có thể lớn hơn `m`. XOR vẫn đúng vì ta khôi phục `key` rồi XOR ngược; đừng vội mod `flag_int` theo `m`.
- **Lỗi #3 — `s1−s0` không khả nghịch:** nếu `gcd(s1−s0, m) ≠ 1` thì `pow(...,-1,m)` lỗi; ở đây `m` cho `gcd = 1` nên ổn. Trường hợp tổng quát cần xử lý ước chung.

## 7. Đường đi nhanh lần sau

Thấy "LCG + biết m + ≥3 output liên tiếp" → áp thẳng công thức `a = Δs2·Δs1⁻¹`, `c = s1−a·s0`, predict next. Xong trong ~2 phút.
