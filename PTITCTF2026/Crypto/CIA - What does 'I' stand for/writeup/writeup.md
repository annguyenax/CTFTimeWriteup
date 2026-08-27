# PTITCTF 2026 — CIA - What does 'I' stand for?

- **Category:** Cryptography
- **Points:** 101 pts
- **Files provided:** `chall.py`, `chall.zip`
- **Decoy Flag:** `PTITCTF{y0Ur_3ff0r7_15_h16hlY_4ppr3c1473D}` *(Fake / Honeypot)*
- **Authentic Flag:** `PTITCTF{1_574nd5_f0r_1n736r17y_4nd_7c3199444034_h45h1n6_h31p_3n5ur3_7h15_pr0p3rtY}`

---

## 1. Phân tích Cốt truyện & Ý nghĩa Ý niệm "Integrity" ('I')

Tên thử thách đặt ra câu hỏi: **"CIA - What does 'I' stand for?"** (Trong mô hình CIA Triad: Confidentiality, **Integrity**, Availability).

Mô tả thử thách:
> *"In an old intelligence archive, every message was accepted only after its source could be proven. Some agents trusted the seal, some trusted the courier, but the careful ones walked the route from the last mark back to the first before trusting the identity behind the message."*

### Cái bẫy "Decoy Flag" (Fake Flag)
Nếu người chơi giải bài theo hướng bẻ khóa mù quáng các tầng zip lồng nhau (`chall.zip` $\to$ `secret.zip` $\to$ `flag.zip`), kết quả trong `flag.txt` nhận được là:
```
PTITCTF{y0Ur_3ff0r7_15_h16hlY_4ppr3c1473D}  ("Your effort is highly appreciated")
```
Khi nộp flag này lên hệ thống sẽ **bị từ chối (Wrong Flag)**, bởi vì đây là cờ giả được cài vào để thử thách xem người chơi có hiểu chữ **"I" (Integrity - Tính toàn vẹn)** hay không.

### Nguyên lý Xác thực Tính toàn vẹn (Integrity Verification)
Trong `chall.py`:
```python
def password_material() -> bytes:
    if PASSWORD_MODE == "sha256_digest":
        flag = os.environ.get("GZCTF_FLAG") or os.environ.get("FLAG") or "PTITCTF{local_test_flag}"
        return hashlib.sha256(flag.encode("utf-8")).hexdigest().encode("ascii")
```
Mật khẩu mở khóa `chall.zip` chính là giá trị băm **SHA256 của chuỗi Flag thật**:
$$\text{Target Hash} = \text{SHA256}(\text{FLAG}) = \texttt{1fcbf4aa0eb78c74f822684fa93cda458e431365e96b2c04abe5cdd56fca9733}$$

Bên trong `chall.zip`, Flag thật được xé nhỏ thành các mảnh ghép và mã hóa ngược (từ ký tự cuối về đầu - *"walked the route from the last mark back to the first"*):
- `chall3.py` (modulus 0): `n475_1{FTCTITP` $\xrightarrow{\text{reverse}}$ `PTITCTF{1_574n`
- `chall3.py` (modulus 3): `1r637n1_r0f_5d` $\xrightarrow{\text{reverse}}$ `d5_f0r_1n736r1`
- `chall6.py`: `6n1h54h_4304449913c7_dn4_y7` $\xrightarrow{\text{reverse}}$ `7y_4nd_7c3199444034_h45h1n6`
- `chall7.py`: `}Ytr3p0rp_51h7_3ru5n3_p13h_` $\xrightarrow{\text{reverse}}$ `_h31p_3n5ur3_7h15_pr0p3rtY}`

Ghép nối 4 mảnh lại:
$$\text{Flag} = \texttt{PTITCTF\{1\_574nd5\_f0r\_1n736r17y\_4nd\_7c3199444034\_h45h1n6\_h31p\_3n5ur3\_7h15\_pr0p3rtY\}}$$
Kiểm tra tính toàn vẹn:
$$\text{SHA256}(\text{Flag}) = \texttt{1fcbf4aa0eb78c74f822684fa93cda458e431365e96b2c04abe5cdd56fca9733} \quad \color{green}\checkmark$$

---

## 2. Phân tích Học thuật các Lỗ hổng Mật mã

### Lỗ hổng 1: RSA Modulus Ngắn ($N \approx 280$ bits)
- **Tham số:** $p, q$ có độ dài 140 bit ($N \approx 280$ bit $\approx 84$ chữ số thập phân).
- **Kỹ thuật:** Sử dụng Self-Initializing Quadratic Sieve (SIQS) qua YAFU trên máy tính thông thường (8 luồng AVX2) bẻ khóa mỗi modulus trong ~30-40 giây.

### Lỗ hổng 2: RSA Batch GCD (`chall3.py`)
- Các module $N_i$ trong danh sách dùng chung thừa số nguyên tố $p$.
- Tính $\gcd(N_i, N_j) > 1$ tìm ra thừa số ngay lập tức trong $\mathcal{O}(\log N)$.

### Lỗ hổng 3: RSA Håstad's Broadcast Attack (`chall6.py`)
- Số mũ mã hóa $e = 3$ gửi đến 3 module $N_1, N_2, N_3$.
- Áp dụng Định lý số dư Trung Hoa (CRT) tìm $C \equiv m^3 \pmod{N_1 N_2 N_3}$. Vì $m^3 < N_1 N_2 N_3$, khai căn bậc 3 nguyên thu được $m$.

### Lỗ hổng 4: Rabin Cryptosystem Decryption (`chall7.py`)
- Cho biết $p, q \equiv 3 \pmod 4$ và $c \equiv m^2 \pmod N$.
- Tính $m_p \equiv c^{(p+1)/4} \pmod p$, $m_q \equiv c^{(q+1)/4} \pmod q$, dùng CRT tìm 4 nghiệm và chọn nghiệm văn bản ASCII hợp lệ.

---

## 3. Cấu trúc 3 tầng Zip lồng nhau (đã xác minh)

Toàn bộ chuỗi giải mã được xác minh bằng việc mở khoá thành công từng tầng (mật khẩu chỉ đúng nếu là bản giải mã RSA chính xác):

| Tầng | Zip | Mật khẩu (hex) | Nguồn RSA | Ghi chú |
|------|-----|----------------|-----------|---------|
| 0 | `chall.zip` | `1fcbf4aa0eb78c74f822684fa93cda458e431365e96b2c04abe5cdd56fca9733` | 4 × modulus 280-bit | = `sha256(FLAG)` |
| 1 | `secret.zip` | `f10fda62a88f71de05fc1250e5d8c8f2` | 1 × modulus 280-bit (`secret.py`) | `random_password` |
| 2 | `flag.zip` | `f4c77352bcf15110fc88035149f7859e` | 1 × modulus 280-bit (`flag.py`) | `random_password` |

- `flag.zip/flag.txt` chứa **flag giả** `PTITCTF{y0Ur_3ff0r7_15_h16hlY_4ppr3c1473D}` — bị hệ thống từ chối vì vi phạm tính toàn vẹn.
- Các thừa số tầng 1/2 (đã kiểm chứng `p*q == n` và bản rõ khớp): `secret.py` → `p=735432302834815394130966759183454512666931`, `q=1174974587228525212165789660572485929948699`; `flag.py` → `p=747771481777026344042866914653467085484091`, `q=877953031758785223550630135889920837486321`.
- **Lưu ý:** bản `PUBLIC_SEGMENTS` trong `chall.py` kèm theo là bản cũ/không khớp với `chall.zip` này; mật khẩu được xác minh trực tiếp bằng cách giải mã thành công chuỗi zip lồng nhau.

## 4. Cách tái lập (Reproduction)

Solver quyết định, tự kiểm tra toàn vẹn: `solve/solve.py`

```bash
python "solve/solve.py"
# [+] Layer-0 password (sha256 of FLAG): 1fcbf4aa0eb78c74f822684fa93cda458e431365e96b2c04abe5cdd56fca9733
#     chall3[0]: PTITCTF{1_574n
#     chall3[3]: d5_f0r_1n736r1
#     chall6   : 7y_4nd_7c3199444034_h45h1n6
#     chall7   : _h31p_3n5ur3_7h15_pr0p3rtY}
# [+] Flag: PTITCTF{1_574nd5_f0r_1n736r17y_4nd_7c3199444034_h45h1n6_h31p_3n5ur3_7h15_pr0p3rtY}
# [*] sha256(flag) = 1fcbf4aa0eb78c74f822684fa93cda458e431365e96b2c04abe5cdd56fca9733
# [+] INTEGRITY VERIFIED
```

Các thừa số tầng 0 (kiểm chứng `p*q==n` và `m^e ≡ c (mod n)`):
- `n=8885236454624829145...` → `(816038443286324146051749864697465935484847, 1088825719881833826874734770997970677090071)`
- `n=1366132309756057281...` → `(1096134935962049816277643537216664923557871, 1246317642961573541737717408379320425028777)`
- `n=7495614225910237681...` → `(790643357812107280431894889727685284754859, 948039865490343569959398817969461165882673)`
- `n=1189948736727152080...` → `(991405450807867692135161548464024686216719, 1200264468747369902613990913429268593482847)`

## 5. Flag Cuối cùng

```
PTITCTF{1_574nd5_f0r_1n736r17y_4nd_7c3199444034_h45h1n6_h31p_3n5ur3_7h15_pr0p3rtY}
```
*(Ý nghĩa: "PTITCTF{I_stands_for_integrity_and_..._hashing_help_ensure_this_property}")*

> **Xác minh:** `sha256(flag)` khớp 100% với mật khẩu tầng 0 (preimage của SHA-256 không thể giả mạo), và flag được tái lập độc lập từ việc giải 3 sub-challenge `chall3`, `chall6`, `chall7` bên trong `chall.zip`.
