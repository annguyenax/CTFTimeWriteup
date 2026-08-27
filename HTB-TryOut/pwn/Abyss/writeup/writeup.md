# Abyss — HTB TryOut (pwn, easy)

## Tóm tắt
Service (ELF64 non-PIE, NX) đọc `.creds` (ngẫu nhiên 15:15 mỗi lần deploy) làm
user/pass hợp lệ rồi lặp theo lệnh 4-byte: `0=LOGIN`, `1=READ`, `2=EXIT`.
`cmd_read` là primitive **đọc file tùy ý** nhưng bị chặn bởi biến toàn cục
`logged_in`. Vì creds ngẫu nhiên, phải **bypass login** để dùng `cmd_read`.

## Lỗ hổng
`cmd_login` copy USER/PASS từ `buf` sang `user`/`pass` bằng vòng lặp
`i=5; while(buf[i]) dst[i-5]=buf[i]; i++` **không kiểm biên và không NUL-terminate**
(`read` không thêm `\0`). Khung stack được canh sao cho một lần `read(512)` tuyến
tính KHÔNG chạm tới return address. Điểm mấu chốt: **biến đếm `i` nằm trên stack
(`rbp-0x4`) ngay trong đường ghi**. Bằng cách dựng input USER để vòng copy ghi đè
chính `i`, ta làm `i` "nhảy qua" saved RBP và đưa các lần ghi kế tiếp rơi đúng vào
saved return address của `cmd_login` mà không phá RBP.

Ta ghi đè các byte thấp của return address thành `0x4014eb` — đây là
`test eax,eax ; jne 0x401500` **bên trong `cmd_read`**, tức ngay sau khi bỏ qua
`mov eax,[logged_in]` (0x4014e5). `eax` khác 0 nên `jne` được lấy → **bỏ qua kiểm
tra `logged_in`** và `cmd_read` tiến thẳng tới `read()→open()→write()` với tên file
do ta cấp. Gửi `flag.txt` → nhận flag.

## Payload (kiểm chứng bằng mô phỏng vòng copy — RET → 0x4014eb)
```
cmd  = p32(0)                                       # vào LOGIN
USER = b"USER " + b"a"*17 + b"\x1c" + b"k"*11 + b"\xeb\x14\x40"
PASS = b"PASS " + b"b"*507
file = b"flag.txt"                                  # (hoặc ".creds")
```
`python solve/solve.py HOST PORT` (raw socket, không cần pwntools) gửi 4 message trên và đọc flag.

Instance 154.57.164.82:32138 (2026-08-20):
`HTB{sH0u1D_h4v3-NU11-t3rmIn4tEd_buf!_46c5f0ca8383b8de8432e99c738629e5}`

## Khắc phục
Giới hạn copy theo kích thước đích, NUL-terminate; không để biến đếm nằm trong
vùng ghi. Không tách kiểm tra `logged_in` khỏi hành động (state machine chắc chắn),
bật canary/PIE, dùng `strlcpy`/`snprintf`.
