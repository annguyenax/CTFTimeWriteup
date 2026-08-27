# Blessed

**Phân loại:** crypto | **Độ khó:** hard | **Tác giả:** makelaris
**Môi trường:** TCP `nc 154.57.164.65 31465` (BLS12-381 + P-256 EC-LCG)

## 1. Tổng quan

`unveil_secrets` trả flag nếu `FastAggregateVerify` đúng trên **mọi** robot đã `verified`. Server tạo sẵn 4 robot với `sk` giấu → phải triệt tiêu chúng bằng rogue-key, rồi giả chữ ký tổng. `join` không yêu cầu proof-of-possession; `verify` là Σ-protocol 64 vòng có thể gian nếu đoán trước coin.

## 2. Phân tích

**BUG 1 — Σ-protocol.** Prover gửi `C` trước, server tung `coin = next(rng) & 1`:
- `coin=1`: kiểm `C = x·G1` (bản live; một số bản dùng `x·pk`)
- `coin=0`: kiểm `C = (sk+x)·G1 − pk`

Mỗi nhánh không cần `sk` nếu biết coin trước khi commit.

**BUG 2 — rogue-key.** `pk' = t·G1 − Σ pk_verified`. Sau khi verify `pk'`, tổng agg_pk = `t·G1` → ký `unveil_secrets` bằng `t`.

**Enabler — EC-LCG.** `Wn += G` trên P-256, yield `Wn.x>>32`, `Wn.y>>32`. `robot_id` chính là các output. 4 robot khởi tạo + `create` + `join` = 6 output = 3 điểm liên tiếp cách `+G`. Lập 7 đa thức (3 phương trình đường cong + công thức cộng điểm), đưa hệ số vào lattice, LLL khôi phục 32 bit thấp.

## 3. Ý tưởng khai thác

1. `create` → `list` (ký `b'list'`) → 5 pk.
2. `pk' = 1337·G1 − Σpk`; `join(pk')` → đủ 6 id.
3. LLL khôi phục điểm thứ 3 → đi tiếp `+G` để biết từng coin.
4. `verify` 64 vòng, commit `C` đúng nhánh.
5. `unveil_secrets(Sign(1337, b'unveil_secrets'))`.

## 4. Thực thi

`python solve/solve.py 154.57.164.65 31465` (cần `py-ecc`, `pycryptodome`, `sympy`, `python-flint`).

Instance 2026-08-20:

`HTB{uNv31leD_5eCre7s_0f_BLS_r0gu3_k3y_4t7aCk_w1th_cu5t0m_zkp_4nd_ec-lcg!!_62773e24b8287635ec3fe1c4a83efe2b}`

## 5. Khắc phục

Challenge Σ-protocol phải Fiat–Shamir hoặc RNG thật, không chung PRNG với id. Bắt PoP khi `join`. Đừng lộ toạ độ EC-LCG đã cắt bit.

## 6. Cờ

`HTB{uNv31leD_5eCre7s_0f_BLS_r0gu3_k3y_4t7aCk_w1th_cu5t0m_zkp_4nd_ec-lcg!!_62773e24b8287635ec3fe1c4a83efe2b}`
