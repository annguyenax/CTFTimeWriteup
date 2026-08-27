# Router Web — HTB TryOut (pwn/firmware, medium)

## Tóm tắt
Firmware ARM32 Buildroot chạy QEMU `versatilepb`. Dịch vụ mới `router-web-panel`
(C++/Crow, non-strip, non-PIE, NX, Full RELRO, có canary) nghe cổng **31337** dưới
user `rweb`, cwd `/opt/router-web-panel` (flag tại `./flag.txt`). Lỗi chính là
**OS command injection** ở chức năng ping.

## Chuỗi khai thác
1. **Basic Auth**: `BasicAuthMiddleware::before_handle()` so với cặp hard-code
   `admin:router123` nhúng trong `.rodata`.
2. **Bật dev mode**: `ping_handler` (0x66c68) kiểm tra global `dev_mode_enabled`
   (0x85654); nếu 0 trả `Dev Mode Not Enabled`. Panel có `enable_dev_mode` (0x1f958)
   /`disable_dev_mode` điều khiển qua hệ thống config (`/configs/save`,
   `/configs/use/<name>`, `/configs/update`, `/configs/current`).
3. **Command injection**: `ping_handler` lấy tham số POST `ip`, nối chuỗi
   `"ping -c 1 " + ip` rồi đưa cho `execCommand` (0x1ffec) → `popen(cmd,"r")`
   (chạy qua `/bin/sh -c`). Không có validate IP/allow-list giữa form và `popen`.
   POST `/admin/ping` với `ip = "127.0.0.1; cat flag.txt"` → flag hiện trong
   `{{output}}` của `admin.mustache`.

Route liệt kê từ `install_routes`: `/admin`, `POST /admin/ping`, `/configs/list`,
`/configs/save`, `/configs/current`, `/configs/update`, `/configs/use/<name>`,
`/configs/delete/<name>`, `/devices`, `/devices/add`, `/devices/update`,
`/static/<path>`.

## Chạy
`python "solve/solve.py" HOST 31337` (cần `requests`): auth, cố bật dev mode qua
config, rồi thử các payload injection và trích `HTB{...}` từ output.

## Trạng thái trên instance 154.57.164.82:32578 (2026-08-20)

- Basic Auth `admin:router123` đúng (firmware `.rodata`).
- `GET /admin` và `POST /admin/ping` trả `401 Dev Mode Not Enabled`.
- `enable_dev_mode` (0x1f958) **không có BL/literal xref** trong ELF; không
  được `install_routes` gắn vào URL. `/configs/update` (JSON),
  `GET /configs/save?name=alnum`, `GET /configs/use/<name>` (307 → `/configs/list`)
  chỉ đổi `current_config`, không set `dev_mode_enabled` (0x85654).
- Device update dùng `__dynamic_cast` sang `Desktop` trước khi ghi `location`.
- Service cũ `router-management` (TCP 1337, `SetParameterValue`) **không** được
  publish trên spawn (1337/1338/31337 timeout).

Chưa bật được dev mode → chưa chạy được sink `popen("ping -c 1 "+ip)`. Không bịa
flag. Bundle local chỉ có `HTB{FakeFlagForTesting}`.

## Khắc phục
Không dùng `popen`/shell; gọi `execve`/`posix_spawn` với argv cố định. Validate IP
bằng `inet_pton` rồi tái tuần tự hoá. Bỏ credential hard-code, cấp secret mỗi thiết
bị + TLS. Bảo vệ dev-mode và route admin ở backend (authorization thực), audit log.
