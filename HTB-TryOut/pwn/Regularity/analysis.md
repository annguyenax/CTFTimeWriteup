# Phân tích tĩnh — Regularity

## 1. Kiến trúc / stack

- ELF 64-bit x86-64 viết bằng assembly (`src/source.asm` còn trong symbol table), không có source rời trong archive.
- Chương trình không dùng libc/dynamic loader; nó gọi trực tiếp Linux syscalls `write`, `read`, `exit`.
- Luồng rất ngắn: `_start` in lời chào → gọi hàm `read` → in câu trả lời → nhảy tới `exit`.
- File phát hành kèm `flag.txt`, nhưng binary không có logic tự mở file; đây là dữ kiện đóng gói, không phải bằng chứng binary trực tiếp đọc secret.

### Protections (đọc tĩnh từ ELF)

| Cơ chế | Trạng thái | Căn cứ |
|---|---|---|
| PIE | Tắt | ELF loại `EXEC`, text cố định tại `0x401000` |
| NX | **Tắt** | `GNU_STACK` có cờ `rwx` |
| Stack canary | Tắt | Không có canary/import `__stack_chk_fail` |
| RELRO | Không áp dụng/thực tế không có | Không có `PT_DYNAMIC`, GOT hay relocation động |
| Symbols | Có | `_start`, `read`, `write`, `exit` và tên source có trong symbol table |

## 2. Lớp lỗ hổng nghi ngờ và lý do

### Stack buffer overflow do sai kích thước syscall

Nguồn: `files/pwn_regularity.zip` → binary `pwn_regularity/regularity`, disassembly hàm `read` tại `0x40104b`:

```asm
40104b: sub    rsp,0x100
401052: mov    eax,0x0
401057: mov    edi,0x0
40105c: lea    rsi,[rsp]
401060: mov    edx,0x110
401065: syscall
401067: add    rsp,0x100
40106e: ret
```

Hàm chỉ cấp 0x100 (256) byte trên stack nhưng yêu cầu `read(0, rsp, 0x110)` đọc tối đa 0x110 (272) byte. Phần vượt 16 byte có thể ghi qua vùng tạm và chạm dữ liệu stack kế tiếp, bao gồm địa chỉ trả về của lời gọi hàm. Không có kiểm tra giá trị trả về hoặc stack canary.

## 3. Vị trí lỗi và đường đi của input

- Entry point `_start` tại `0x401000` gọi wrapper `write`, rồi `call 0x40104b <read>`.
- Trong `read`, stdin (FD 0) được syscall đọc trực tiếp vào địa chỉ `rsp` sau khi chỉ trừ 0x100 byte.
- Khi syscall trả về, hàm cộng lại 0x100 rồi thực hiện `ret`; vì vậy dữ liệu vượt biên nằm đúng trên vùng stack mà `ret` sử dụng.
- Nếu luồng không bị thay đổi, `_start` in thông báo thứ hai và nhảy gián tiếp tới `exit` tại `0x40106f`.

## 4. Hướng tiếp cận khái niệm

- Dựng sơ đồ stack quanh thời điểm `call read`: vùng 0x100 byte, địa chỉ trả về, rồi phần còn lại của initial process stack.
- Xác định chính xác bao nhiêu byte đầu vào cần để chạm địa chỉ trả về bằng layout/disassembly hoặc một mẫu kiểm thử vô hại trong môi trường cục bộ; tài liệu này không cung cấp chuỗi/payload.
- Do text có địa chỉ cố định và stack executable, về mặt khái niệm có thể nghiên cứu chuyển hướng điều khiển tới mã sẵn có hoặc dữ liệu đã đọc. Việc chọn kỹ thuật cụ thể phải xét byte budget rất nhỏ sau vùng đệm và điều kiện thanh ghi; không cần tạo exploit để kết luận lỗi.
- Không suy diễn rằng `flag.txt` được mở tự động: binary chỉ có ba syscall nói trên. Bất kỳ hướng đọc file nào cũng cần được chứng minh từ primitive điều khiển luồng, không phải từ chuỗi trong binary.

## 5. Khắc phục

- Tham số thứ ba của syscall `read` không được vượt vùng đã cấp: dùng tối đa `0x100`, hoặc cấp đủ `0x110` và vẫn chừa/track độ dài nếu xử lý như chuỗi.
- Kiểm tra giá trị trả về âm, EOF và số byte thực đọc trước mọi xử lý tiếp theo.
- Đánh dấu stack không thực thi bằng section `.note.GNU-stack`; build PIE nếu môi trường hỗ trợ.
- Nếu chuyển sang toolchain C/linked binary, bật stack protector, full RELRO và các cảnh báo/hardening chuẩn.
- Tránh đặt buffer nhận dữ liệu không tin cậy sát dữ liệu điều khiển; tốt hơn là dùng vùng `.bss` có giới hạn rõ hoặc API wrapper thực thi kiểm tra kích thước.

## Kết luận

`Regularity` là một ELF assembly tối giản với lỗi sai lệch kích thước rõ ràng: cấp 256 byte nhưng đọc 272 byte. Kết hợp với no PIE, no canary và executable stack, đây là lớp stack buffer overflow có khả năng ảnh hưởng control flow; phân tích dừng ở mức khái niệm, không tạo exploit/payload.
