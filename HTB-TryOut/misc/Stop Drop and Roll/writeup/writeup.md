# Stop Drop and Roll

**Phân loại:** misc | **Độ khó:** very easy | **Tác giả:** makelaris
**Môi trường:** TCP `nc 154.57.164.82 31142`

## 1. Tổng quan

Mini-game "The Fray": server lần lượt đưa một hoặc nhiều tình huống `GORGE` / `PHREAK` / `FIRE`. Người chơi phải trả đúng hành động, lặp nhiều vòng cho đến khi in flag.

## 2. Phân tích

Banner nêu mapping cố định:

| Tình huống | Trả lời |
|---|---|
| GORGE | STOP |
| PHREAK | DROP |
| FIRE | ROLL |

Nhiều tình huống trên một dòng, cách nhau bằng `", "`; câu trả lời nối bằng `-`. Ví dụ `GORGE, FIRE, PHREAK` → `STOP-ROLL-DROP`. Sau `Are you ready? (y/n)` gửi `y` là bắt đầu. Cần hàng trăm vòng đúng (thực tế ~500).

## 3. Ý tưởng khai thác

Script: đọc dòng tình huống, map từng token, gửi chuỗi hyphen, lặp đến khi thấy `HTB{`.

## 4. Thực thi

`python solve/solve.py 154.57.164.82 31142`

Instance 2026-08-20, dòng kết:

`Fantastic work! The flag is HTB{1_wiLl_sT0p_dR0p_4nD_r0Ll_mY_w4Y_oUt!}`

## 5. Khắc phục

Đây là challenge cố ý repetitive, không phải lỗ hổng sản phẩm. Nếu làm game thật: không nhúng flag sau N vòng đoán được bằng script.

## 6. Cờ

`HTB{1_wiLl_sT0p_dR0p_4nD_r0Ll_mY_w4Y_oUt!}`
