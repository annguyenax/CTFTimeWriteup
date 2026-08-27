# Blessed — Analysis (HTB Try Out / Crypto, hard) — BLS12-381

Target: nc 154.57.164.66:31963 | Mục tiêu: cmd `unveil_secrets` trả FLAG.

## Điều kiện thắng
`unveil_secrets(agg_sig)` gọi `bls.FastAggregateVerify(agg_pk, b'unveil_secrets', agg_sig)`,
với `agg_pk = [r.pk for r in robots if r.verified]`. Cần agg_sig = (Σ sk_i)·H(msg) — tức biết
DLOG của tổng public key của MỌI robot đã verified.

Server khởi tạo **4 robot verified** (crew 5 − {Hackers} = 4) với sk NGẪU NHIÊN, không lộ.
→ Không thể tính Σsk vì 4 con này. Phải triệt tiêu chúng.

## Chuỗi tấn công (2 lỗ hổng ghép)

### BUG 1 — Σ-protocol `verify` KHÔNG an toàn (challenge đoán trước được)
Mỗi vòng: prover gửi C trước, rồi server tung "coin" = `next(self.rand) & 1`:
- coin=1: lộ x, kiểm `x·Pk == C`  → prover chỉ cần chọn x, đặt C=x·Pk (KHÔNG cần sk).
- coin=0: lộ s (=sk+x), kiểm `s·G1 − Pk == C` → prover chọn s bất kỳ, đặt C=s·G1 − Pk (KHÔNG cần sk).
Mỗi nhánh riêng lẻ KHÔNG cần sk. Chỉ cần **biết coin trước khi commit C** là pass 64/64 vòng cho
BẤT KỲ pk nào (kể cả pk ta không biết sk). → verify được 1 **rogue key**.

### BUG 2 — BLS rogue-key attack (thiếu proof-of-possession thực sự khi `join`)
Dùng `create` (trả sk) + `list` (ký bằng robot của ta) để đọc pk của cả 4 robot gốc.
`join` một rogue pk = **t·G1 − Σ(pk các robot verified khác)** (t ta chọn, biết).
Sau khi verify rogue (nhờ BUG 1), tổng agg_pk = t·G1 → DLOG = t đã biết →
forge `agg_sig = t · H('unveil_secrets')` (bls.Sign với sk=t). unveil_secrets PASS → FLAG.

### ENABLER — dự đoán EC-PRNG để biết coin
`rng`: W0 = seed·G + B (P256), Wn = W0 + n·G, yield `Wn.x>>32` rồi `Wn.y>>32` (2 output/điểm).
- robot_id trả về CHÍNH LÀ các output x>>32 / y>>32 → ta quan sát được luồng (top 224 bit toạ độ
  các điểm LIÊN TIẾP cách nhau đúng +G).
- coin = (giá trị next & 1) = **bit thứ 32 của toạ độ** điểm tương ứng.
- Khôi phục 1 ĐIỂM đầy đủ từ top-224-bit của x,y (32 bit thấp ẩn) bằng phương trình đường cong +
  quan hệ điểm liên tiếp (lattice/Coppersmith, hoặc kết hợp nhiều điểm). Có 1 điểm đầy đủ →
  suy ra MỌI điểm kế (bước +G cố định) → biết trước toàn bộ coin của 64 vòng verify.

## Trình tự khai thác
1. `create` vài robot → có sk + chữ ký hợp lệ; `list` → đọc pk 4 robot gốc + của ta.
2. Thu robot_id (các output PRNG) → khôi phục 1 điểm đầy đủ → đồng bộ trạng thái PRNG,
   dự đoán coin cho các `next()` sắp tới (nhớ mỗi create/join tiêu 1 output, mỗi vòng verify tiêu 1).
3. Tính rogue pk = t·G1 − Σ(pk mọi robot sẽ verified) ; `join(rogue_pk)`.
4. `verify(rogue_id)`: 64 vòng, mỗi vòng dùng coin đã dự đoán → commit C đúng dạng (BUG 1) → pass.
5. `unveil_secrets(agg_sig=t·H('unveil_secrets'))` → FLAG.

## Khắc phục (defensive)
- Challenge của Σ-protocol phải từ hash cam kết (Fiat–Shamir) hoặc randomness thật, KHÔNG từ PRNG
  nội bộ đoán được. Đừng dùng chung 1 PRNG cho id lẫn challenge.
- BLS: bắt buộc **proof-of-possession** đúng chuẩn khi join (ciphersuite là ProofOfPossession nhưng
  join lại bỏ qua) để chặn rogue-key.
- Không truncate rồi lộ output PRNG dựa trên EC point (EC-LCG truncated là dự đoán được).
