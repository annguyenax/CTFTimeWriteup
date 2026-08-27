# Immiscible — Writeup (L3akCTF 2026, crypto)

- **Flag:** `L3AK{Oil_4ND_v1N3g4r_WitH0ut_Mix1nG_Sp1LL5_eV3rYth1ng}`
- **Trạng thái:** ✅ Verified (`eval_public(sig)==target` + AES giải sạch)
- **Điểm/Solves:** 79 / 112
- **File:** `files/crypto_immiscible/chal.py`, `solve/public.json`

---

## 1. Đề bài yêu cầu gì

Câu chuyện dài về hai chất lỏng "không trộn lẫn" (immiscible) rồi tách ra. `chal.py`:
- Trường `F_79`. `V=4` vinegar, `O=4` oil, `N=8` biến, `M=9` đa thức bậc 2.
- Public key = 9 đa thức bậc 2 `p_k(x)`. Sinh `secret_signature` (8 giá trị ngẫu nhiên), `target = eval_public(polys, secret)`.
- `key = sha256(bytes(secret))`, mã hóa flag bằng AES-ECB → `encrypted_flag`.

Nhiệm vụ: từ `polys`, `target`, `encrypted_flag` khôi phục `secret_signature` → key → flag.

## 2. Kiến thức nền

**Oil-and-Vinegar (OV):** hệ chữ ký đa biến. Biến chia làm **vinegar** (x0..x3) và **oil** (x4..x7). Trong `make_poly`, số hạng bậc 2 CHỈ gồm:
- vinegar × vinegar (`i,j < V`)
- vinegar × oil (`i < V`, `j >= V`)

**KHÔNG có oil × oil.** Đây chính là "immiscible" — dầu và giấm không trộn với nhau. Hệ quả then chốt: **nếu cố định vinegar, mỗi đa thức trở thành TUYẾN TÍNH theo oil.**

## 3. Phân tích & lý do chọn kỹ thuật

Đặt vinegar `v=(x0..x3)` cố định. Phương trình `k`:
```
target_k = C_k(v) + Σ_o D_{k,o}(v) · x_o
```
với `C_k(v)` = phần hằng + tuyến tính + vinegar×vinegar (chỉ phụ thuộc v), `D_{k,o}(v) = linear_k[o] + Σ_{i<V} quad_k[i,o]·v_i`. Đây là hệ **tuyến tính 9×4** theo oil.

Vì có 9 phương trình > 8 ẩn ⇒ nghiệm **duy nhất**. Với vinegar ngẫu nhiên, hệ 9×4 theo oil thường **vô nghiệm**; chỉ đúng vinegar của secret mới **nhất quán**. Nên: **brute vinegar (79⁴), giải tuyến tính oil từ 4 phương trình đầu, kiểm tra 5 phương trình còn lại.** Điểm nhất quán duy nhất chính là secret.

79⁴ ≈ 39 triệu — quá chậm nếu vòng lặp Python thuần, nên **vectorize bằng numpy**: giải modular 4×4 theo lô (batched Gauss-Jordan trên F₇₉).

## 4. Các bước khai thác

1. Parse `polys` thành mảng hệ số (const, linear, vinegar×vinegar, vinegar×oil).
2. Với mỗi `v0`, sinh toàn bộ `(v1,v2,v3)` (79³) → mảng vinegar `(K,4)`.
3. Tính `C(v)` (K,9) và ma trận `D(v)` (K,9,4); `r = target − C`.
4. Batched solve `D[:, :4]·oil = r[:, :4]`; kiểm tra `D[:, 4:]·oil == r[:, 4:]`.
5. Điểm hợp lệ → signature; kiểm tra lại `eval_public(sig)==target`; `key=sha256`, giải AES → flag.

Solver: [solve/solve.py](../solve/solve.py) (thuần numpy, ~48s). Chạy:
```bash
python solve/solve.py
# signature [23,7,73,60,34,54,53,7]; eval==target True; flag L3AK{...}
```

## 5. Cách xác minh flag

- `eval_public(sig) == target` (thỏa **cả 9** đa thức công khai) → signature đúng, không phải nghiệm giả.
- AES key = sha256(signature) giải `encrypted_flag` unpad sạch, đúng `L3AK{...}`, nội dung có nghĩa ("Oil and vinegar without mixing spills everything").

## 6. Bài học & lỗi thường gặp

- **Nhận diện OV:** đa thức bậc 2 thiếu số hạng oil×oil ⇒ cố định vinegar là tuyến tính hóa. Đây là "cửa hậu" toán học của OV.
- **z3/Gröbner có thể quá chậm** với hệ bậc-2 modulo (ở đây cả hai đều timeout >2 phút). Dùng đúng cấu trúc + đại số tuyến tính vectorized nhanh hơn nhiều.
- **Overdetermined (M>N) ⇒ nghiệm duy nhất** ⇒ brute vinegar là bộ lọc nhất quán.
- **Đừng tin solver có sẵn:** bản z3 cũ trong repo timeout; đã thay bằng solver numpy tự chứng.

## 7. Đường đi nhanh lần sau

Đa thức bậc 2 nhiều biến, thiếu tích giữa một nhóm biến (oil) ⇒ OV ⇒ cố định nhóm còn lại (vinegar), giải tuyến tính. Có sage: `solve_mod`/Gröbner tức thì; không có: brute vinegar vectorized.
