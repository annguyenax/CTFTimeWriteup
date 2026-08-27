# Character

**Phân loại:** misc | **Độ khó:** very easy | **Tác giả:** makelaris
**Môi trường:** TCP `nc 154.57.164.73 30760`

## 1. Tổng quan

Service cố tình làm cho việc đọc bí mật trở nên nhàm chán: mỗi lần kết nối (thực ra là mỗi lượt trong cùng session) chỉ trả **một ký tự** của flag theo chỉ số. Cần script hóa việc hỏi lần lượt mọi index.

## 2. Phân tích

Banner:

```
Which character (index) of the flag do you want? Enter an index:
```

Gửi `0` → `Character at Index 0: H` rồi hỏi lại. Gửi `1` → `T`. Không có file đính kèm; toàn bộ flag nằm trên server.

## 3. Ý tưởng khai thác

Giữ nguyên một TCP session, gửi `0`, `1`, `2`, … cho đến khi ghép được `HTB{...}`. Không cần brute hay RCE.

## 4. Thực thi

`python solve/solve.py 154.57.164.73 30760` đọc từng ký tự cho đến `}`.

Instance 2026-08-20:

`HTB{tH15_1s_4_r3aLly_l0nG_fL4g_i_h0p3_f0r_y0Ur_s4k3_tH4t_y0U_sCr1pTEd_tH1s_oR_els3_iT_t0oK_qU1t3_l0ng!!}`

## 5. Khắc phục

Đừng tiết lộ bí mật theo oracle từng byte. Nếu cần debug, giới hạn số lần hỏi và rate-limit.

## 6. Cờ

`HTB{tH15_1s_4_r3aLly_l0nG_fL4g_i_h0p3_f0r_y0Ur_s4k3_tH4t_y0U_sCr1pTEd_tH1s_oR_els3_iT_t0oK_qU1t3_l0ng!!}`
