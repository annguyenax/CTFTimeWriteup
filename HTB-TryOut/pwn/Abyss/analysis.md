# Phân tích tĩnh — Abyss

## 1. Kiến trúc / stack

- ELF 64-bit x86-64, C, liên kết động với glibc; symbol chưa bị strip.
- Docker Ubuntu 20.04 chạy `socat`, mỗi kết nối được chuyển vào một tiến trình `/app/abyss`. Không có HTTP.
- `main()` đọc `.creds` theo định dạng `username:password` vào hai biến toàn cục, rồi nhận một số nguyên 4 byte để chọn `LOGIN`, `READ` hoặc `EXIT`.
- `cmd_login()` nhận hai bản tin thô có tiền tố `USER ` và `PASS `; `cmd_read()` mở đường dẫn do người dùng cung cấp nhưng chỉ sau khi `logged_in` được đặt.

### Protections (đọc tĩnh từ ELF)

| Cơ chế | Trạng thái | Căn cứ |
|---|---|---|
| PIE | Tắt | ELF loại `EXEC`, địa chỉ text cố định quanh `0x401000` |
| NX | Bật | `GNU_STACK` có cờ `rw-`, không có quyền thực thi |
| Stack canary | Tắt | Không có import/symbol `__stack_chk_fail` |
| RELRO | Partial | Có `GNU_RELRO` nhưng dynamic section không có `BIND_NOW` |
| Symbols | Có | `cmd_login`, `cmd_read`, `main` xuất hiện trong symbol table |

## 2. Lớp lỗ hổng nghi ngờ và lý do

### Chính: stack buffer overflow do thiếu kết thúc NUL

Nguồn: `files/pwn_abyss.zip` → `pwn_abyss/challenge/source.c`, hàm `cmd_login()` (khoảng dòng 25–38):

```c
memset(buf, '\0', sizeof(buf));
if (read(0, buf, sizeof(buf)) < 0)
    return;

if (strncmp(buf, "USER ", 5))
    return;

i = 5;
while (buf[i] != '\0')
{
    user[i - 5] = buf[i];
    i++;
}
user[i - 5] = '\0';
```

`read()` được phép ghi đủ 512 byte, làm mất toàn bộ các byte NUL được tạo bởi `memset`. Vòng lặp sau đó không bị chặn bởi kích thước `buf` hoặc `user`: nó đọc quá cuối `buf` và tiếp tục ghi quá cuối `user` cho tới khi tình cờ gặp byte 0. Nhánh xử lý `PASS` lặp lại cùng mẫu lỗi. Đây là out-of-bounds read kết hợp stack buffer overflow, có khả năng làm hỏng dữ liệu điều khiển trên stack.

### Phụ: arbitrary file read / path traversal sau xác thực

Nguồn: cùng file, `cmd_read()` (khoảng dòng 72–84):

```c
if (read(0, buf, sizeof(buf)) <= 0)
    return;

fd = open(buf, O_RDONLY);
if (fd < 0)
{
    perror("open");
    return;
}

ret = read(fd, buf, sizeof(buf));
```

Không có allowlist, thư mục gốc cố định, canonicalization hoặc kiểm tra loại file. Vì vậy người dùng đã đăng nhập có thể yêu cầu một đường dẫn tùy ý mà UID `ctf` đọc được. Nếu đầu vào dài đúng 512 byte thì đường dẫn cũng có thể thiếu NUL, tạo thêm một lỗi đọc quá biên khi `open()` xử lý chuỗi.

## 3. Vị trí lỗi và đường đi của input

- `main()` đọc 4 byte từ stdin vào `cmd`; giá trị `LOGIN` gọi `cmd_login()`.
- `cmd_login()` → lần `read()` thứ nhất → kiểm tra tiền tố `USER ` → vòng sao chép không giới hạn vào `user[512]`; lần `read()` thứ hai tạo cùng đường đi vào `pass[512]`.
- Nếu so sánh credential thành công, biến toàn cục `logged_in` được đặt thành 1.
- Lệnh `READ` trong `main()` gọi `cmd_read()` → dữ liệu stdin đi thẳng vào `open()` → nội dung file được trả ra stdout.
- Việc `socat` fork theo kết nối giới hạn trạng thái vào từng tiến trình con nhưng không loại bỏ lỗi bộ nhớ.

## 4. Hướng tiếp cận khái niệm

- Xác nhận giao thức nhị phân trước: selector là một số nguyên 4 byte, sau đó mới đến hai bản tin đăng nhập.
- Với nhánh đăng nhập, nghiên cứu trường hợp một lần đọc lấp kín buffer mà không có NUL; dùng phân tích layout stack/disassembly để xác định vùng nào có thể bị ghi đè và protections nào chi phối khả năng kiểm soát luồng. Không cần giả định đây chỉ là bypass chuỗi vì lỗi có thể vượt ra ngoài cả hai mảng cục bộ.
- Một hướng khác ở mức logic là đánh giá liệu trạng thái `logged_in` có nằm trong vùng có thể bị ảnh hưởng hay không; phải chứng minh từ layout thực tế, không suy ra chỉ từ thứ tự khai báo C.
- Sau khi có quyền hợp lệ, đánh giá phạm vi đọc file dựa trên UID, working directory và quyền filesystem. Không cần dùng đường dẫn/payload cụ thể để chứng minh thiếu ràng buộc.

## 5. Khắc phục

- Luôn chừa một byte và dùng số byte thực đọc được: `n = read(fd, buf, sizeof(buf) - 1); buf[n] = '\0';`.
- Không tự viết vòng sao chép chuỗi không giới hạn; kiểm tra chiều dài phần sau tiền tố trước khi dùng `memcpy`, đồng thời loại bỏ ký tự xuống dòng theo độ dài đã biết.
- Bật hardening khi biên dịch/liên kết: stack protector mạnh, PIE, full RELRO, `_FORTIFY_SOURCE`, và giữ NX.
- Với đọc file, giới hạn vào một thư mục được phép bằng directory FD + `openat`/`openat2`, từ chối absolute path, symlink và thành phần thoát thư mục; kiểm tra loại file sau khi mở.
- Tách quyền: tiến trình phục vụ không nên có quyền đọc secret không cần thiết; không dùng một biến toàn cục đơn giản làm toàn bộ ranh giới ủy quyền.

## Kết luận

Dấu hiệu mạnh nhất là lỗi quản lý độ dài/NUL trong `cmd_login()`, nghiêm trọng hơn chức năng đọc file có chủ ý sau xác thực. Binary được phát hành không PIE, không canary và chỉ Partial RELRO, nên lỗi stack cần được ưu tiên khi phân tích sâu hơn; tài liệu này không xây dựng exploit hay payload.
