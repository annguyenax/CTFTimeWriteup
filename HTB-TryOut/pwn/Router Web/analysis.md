# Phân tích tĩnh — Router Web

## 1. Kiến trúc / stack

- Firmware ARM 32-bit little-endian cho máy QEMU `versatilepb`; `run.sh` boot `zImage` với `rootfs.ext2` và forward các cổng 1337, 1338, 31337.
- Rootfs Buildroot/BusyBox có hai dịch vụ: `router-management` chạy dưới UID `rm`, và `router-web-panel` chạy dưới UID `rweb`. Web panel làm việc trong `/opt/router-web-panel`.
- `router-web-panel` là C++ dùng Crow/Asio, Mustache và JSON. `main()` tạo `Crow<BasicAuthMiddleware>`, khởi tạo cấu hình, đăng ký route rồi chạy HTTP trên cổng 31337.
- Các route đáng chú ý: `/configs/*`, `/devices/*`, `/admin`, và POST `/admin/ping`. Template `admin.mustache` đưa trường form `ip` tới `/admin/ping`.
- Binary chứa symbol C++ đầy đủ nên có thể nhận diện `main`, `install_routes`, `ping_handler`, `execCommand`, `Config::FromJson` và middleware xác thực.

### Protections của `router-web-panel`

| Cơ chế | Trạng thái | Căn cứ |
|---|---|---|
| PIE | Tắt | ELF ARM loại `EXEC` |
| NX | Bật | `GNU_STACK` là `RW`, không executable |
| Stack canary | Bật | Import và sử dụng `__stack_chk_fail` |
| RELRO | Full | Có `GNU_RELRO`, `BIND_NOW` và `FLAGS_1: NOW` |
| Symbols | Không strip | Symbol table chứa tên hàm ứng dụng |

## 2. Lớp lỗ hổng nghi ngờ và lý do

### Chính: OS command injection qua chức năng ping

Nguồn: `files/router_web.zip` → `rootfs.ext2` → `/usr/bin/router-web-panel`, disassembly `ping_handler()` tại `0x66dc8–0x66e04`:

```asm
66dc8: ldr  r1, [pc, #1320]    ; địa chỉ chuỗi "ping -c 1 "
66dcc: mov  r2, #10
66dd0: add  r0, sp, #56
66dd4: bl   basic_string::_M_append
66dec: mov  r2, r4             ; độ dài giá trị form
66df0: mov  r1, r5             ; con trỏ giá trị form "ip"
66df4: add  r0, sp, #56
66df8: bl   basic_string::_M_append
66dfc: add  r1, sp, #56
66e00: add  r0, sp, #80
66e04: bl   execCommand(...)
```

`ping_handler()` lấy body parameters, tìm trường `ip`, nối nguyên giá trị vào tiền tố lệnh rồi chuyển chuỗi kết quả cho `execCommand()`. Hàm sau gọi `popen(command.c_str(), ...)` tại `0x20144–0x20152`, tức là đi qua shell. Không thấy allowlist/canonical parse giữa bước nối chuỗi và sink. Đây là mẫu command injection điển hình; kiểm tra định dạng IP dùng ở lớp `Device` không xuất hiện trên đường đi này.

### Phụ: xác thực bằng bí mật hard-code và cổng quản trị nguy hiểm

Trong `.rodata` có cặp chuỗi liền nhau `admin` và `router123`, được `BasicAuthMiddleware::before_handle()` dùng cùng header `Authorization`/scheme `Basic`. Firmware vì thế dùng credential tĩnh, có thể trích trực tiếp từ image và giống nhau trên mọi bản sao. Basic Auth cũng không cung cấp bí mật truyền tải nếu thiếu TLS.

Route ping còn kiểm tra biến toàn cục `dev_mode_enabled`; nếu tắt, nó trả `Dev Mode Not Enabled`. Đây là điều kiện trước của sink, không phải biện pháp làm sạch input. Các hàm `enable_dev_mode()`/`disable_dev_mode()` và cơ chế cấu hình cho thấy trạng thái này có thể thay đổi trong tiến trình, nên cần lập bản đồ state transition khi phân tích tiếp.

## 3. Vị trí lỗi và đường đi của input

- `rootfs.ext2:/opt/router-web-panel/templates/admin.mustache` tạo POST form với trường `ip` tới `/admin/ping`.
- `install_routes()` đăng ký `/admin/ping` với `ping_handler(crow::request const&)`.
- `BasicAuthMiddleware::before_handle()` kiểm tra header Basic Auth; `ping_handler()` sau đó kiểm tra `dev_mode_enabled`.
- `ping_handler()` gọi `request.get_body_params()`, lấy giá trị `ip`, nối vào chuỗi `"ping -c 1 "`, rồi gọi `execCommand()`.
- `execCommand()` đưa chuỗi vào `popen()` và thu stdout bằng `fgets`; kết quả được render vào `admin.mustache` qua trường `output`.
- Dịch vụ chạy dưới user `rweb`, không phải root. Điều này giảm quyền tiến trình nhưng không loại bỏ command injection; phạm vi tác động là mọi tài nguyên UID `rweb` truy cập được, gồm working directory của web panel.

## 4. Hướng tiếp cận khái niệm

- Trước hết lập sơ đồ điều kiện: Basic Auth → trạng thái dev mode → POST parameter `ip` → shell sink. Xác nhận từng cạnh bằng symbol/disassembly và template, không cần gửi request tới server.
- Đối với command injection, chỉ cần chứng minh input không được parse thành địa chỉ IP và được nối trực tiếp trước `popen`; không cần xây payload. Có thể đối chiếu tập ký tự shell có ý nghĩa với việc không có validation trên đường đi.
- Phân tích riêng state machine của cấu hình để hiểu khi nào `dev_mode_enabled` được bật; không nhầm nút HTML `disabled` với kiểm soát phía server.
- Đánh giá tác động theo UID `rweb`, cwd `/opt/router-web-panel`, quyền file và seccomp (nếu thực sự được áp dụng). Không giả định tự động có đặc quyền root.

## 5. Khắc phục

- Không dùng `popen()`/shell. Gọi chương trình ping bằng `fork` + `execve`/`posix_spawn` với argv cố định, ví dụ executable cố định và địa chỉ là một phần tử argv riêng.
- Parse input bằng thư viện chuẩn (`inet_pton` cho IPv4/IPv6), sau đó serialize lại dạng chuẩn; áp giới hạn chiều dài và timeout/rate limit.
- Tách chức năng chẩn đoán khỏi web process, dùng helper quyền tối thiểu với giao thức dữ liệu chặt chẽ và seccomp/namespace thực sự.
- Loại bỏ credential hard-code; cấp secret riêng mỗi thiết bị, lưu dạng hash/secret store, hỗ trợ rotation và chỉ truyền qua TLS. Phân quyền riêng route quản trị thay vì một middleware chung đơn giản.
- Giữ các hardening hiện có (NX, canary, Full RELRO) và bật PIE. Hardening bộ nhớ không sửa được command injection.
- Bảo vệ dev-mode ở backend bằng authorization rõ ràng, thời hạn ngắn và audit log; không dựa vào trạng thái UI.

## Kết luận

Lỗi nổi bật là command injection trong `ping_handler()`: dữ liệu form được nối vào câu lệnh và chuyển tới `popen()`. Khai thác thực tế còn phụ thuộc Basic Auth và `dev_mode_enabled`, nhưng cả hai chỉ là gate; credential tĩnh trích được từ firmware và dev mode là trạng thái thay đổi được. Phân tích này chỉ mô tả primitive và điều kiện, không cung cấp request hay payload chạy được.
