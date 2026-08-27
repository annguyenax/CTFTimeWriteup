# Phân tích tĩnh — TunnelMadness

## 1. Kiến trúc / stack

- ELF 64-bit x86-64, viết bằng C (`main.c` còn trong symbol table), liên kết động với glibc.
- Đây là chương trình terminal đơn tiến trình, không có server/network. Người chơi nhập một ký tự hướng trong `L/R/F/B/U/D`, hoặc `Q` để thoát.
- Trạng thái vị trí gồm ba số nguyên `(x, y, z)`, bắt đầu tại `(0,0,0)`. `get_cell()` ánh xạ vị trí vào mảng `maze` nhúng trong `.rodata`.
- Maze có kích thước 20 × 20 × 20. Symbol `maze` dài `0x1f400` byte = 8000 cell × 16 byte; trường tại offset `+0x0c` là loại cell. Loại 2 bị chặn, loại 3 là đích.
- Khi đến cell loại 3, `main()` gọi `get_flag()`, mở `/flag.txt`; nếu không có file thì in chuỗi flag giả nhúng trong binary.

### Protections

| Cơ chế | Trạng thái | Căn cứ |
|---|---|---|
| PIE | Bật | ELF loại `DYN`, `FLAGS_1: PIE` |
| NX | Bật | `GNU_STACK` là `RW` |
| Stack canary | Không thấy | Không import `__stack_chk_fail` |
| RELRO | Partial | Có `GNU_RELRO` nhưng không có `BIND_NOW` |
| Symbols | Không strip | Có `main`, `get_cell`, `prompt_and_update_pos`, `get_flag`, `maze` |

## 2. Lớp điểm yếu nghi ngờ và lý do

### Không thấy memory-corruption rõ ràng; lớp chính là embedded-data / client-side validation logic

Nguồn: `files/rev_tunnelmadness.zip` → `rev_tunnelmadness/tunnel`, disassembly `get_cell()` tại `0x11b5–0x11df`:

```asm
11b5: mov    eax,DWORD PTR [rdi]       ; x
11b7: lea    rax,[rax+rax*4]
11bb: lea    rax,[rax+rax*4]
11bf: shl    rax,0x4                   ; 400*x
11c3: mov    edx,DWORD PTR [rdi+0x4]   ; y
11c6: lea    rdx,[rdx+rdx*4]
11ca: lea    rax,[rax+rdx*4]           ; +20*y
11ce: mov    edx,DWORD PTR [rdi+0x8]   ; z
11d1: add    rax,rdx
11d4: shl    rax,0x4                   ; cell size 16
11d8: lea    rdx,[rip+...]             ; symbol maze
11df: add    rax,rdx
```

Công thức là `maze + 16 * (400*x + 20*y + z)`. Toàn bộ topology và marker đích nằm trong binary, còn vòng lặp chỉ kiểm tra trường loại cell ở offset `+0x0c`. Vì thế bài không đòi hỏi phá bộ nhớ; có thể trích cấu trúc dữ liệu và giải graph offline. Đây là điểm yếu thiết kế nếu maze được coi là bí mật, nhưng là cơ chế có chủ ý của bài reverse engineering.

Kiểm tra biên trong sáu nhánh di chuyển chặn tọa độ ngoài `0..19` trước khi gọi `get_cell()`. `get_flag()` cấp 128 byte và gọi `fgets(..., 128, ...)`, nên cũng không thấy overflow trực tiếp. Không nên gán nhãn integer overflow/UAF khi disassembly hiện tại không hỗ trợ kết luận đó.

## 3. Vị trí logic và đường đi của input

- `main()` (`0x1538`) giữ ba tọa độ trên stack, gọi `get_cell()`, và lặp tới khi `[cell+0x0c] == 3`.
- `prompt_and_update_pos()` (`0x11e3`) dùng `scanf(" %c", ...)`, đổi sang chữ hoa rồi dispatch qua jump table.
- Mapping tĩnh: `L/R` giảm/tăng `x`, `B/F` giảm/tăng `y`, `D/U` giảm/tăng `z`; `Q` gọi `exit`.
- Mỗi nhánh kiểm tra biên, tạo vị trí ứng viên, gọi `get_cell()`, từ chối nếu loại cell là 2, nếu không thì commit vị trí mới.
- Khi cell hiện tại có loại 3, `main()` gọi `get_flag()` → `fopen("/flag.txt", "r")` → `fgets` → `puts`.

## 4. Hướng tiếp cận khái niệm

- Dùng symbol/section table để lấy đúng blob `maze` từ `.rodata`: địa chỉ symbol `0x20e0`, kích thước `0x1f400`.
- Parse mỗi record 16 byte theo thứ tự `(x,y,z)` của công thức trên; dùng số nguyên ở offset 12 làm loại cell.
- Xây graph 3D: node là cell trong biên, bỏ cell loại 2, cạnh nối sáu hàng xóm trực giao. Tìm cell loại 3 rồi dùng BFS từ `(0,0,0)` để lấy đường đi ngắn.
- Chuyển các delta tọa độ sang `L/R/B/F/D/U` theo jump table. Nên tự kiểm tra lại đường bằng mô phỏng offline cùng quy tắc, không cần chạy binary và không cần brute-force tương tác.
- Không nhầm chuỗi `HTB{fake_flag_for_testing}` trong `.rodata` với secret thật; nó chỉ là fallback khi `/flag.txt` không mở được.

## 5. Khắc phục / secure design

- Nếu topology hoặc đích phải bí mật, không nhúng toàn bộ dữ liệu và logic xác minh vào client; xác minh tiến trình ở phía tin cậy bằng trạng thái/session có integrity protection.
- Không coi obfuscation hay strip symbol là ranh giới bảo mật. Strip symbol chỉ làm reverse engineering chậm hơn, không bảo vệ dữ liệu `.rodata`.
- Nếu tiếp tục dùng mảng phẳng, đóng gói phép tính index với kiểm tra biên tập trung và dùng kiểu không dấu/kích thước đủ lớn; kiểm tra overflow trước phép nhân.
- Giữ `fgets` theo đúng kích thước buffer, kiểm tra giá trị trả về trước `puts`, và chạy với quyền chỉ đủ đọc đúng file cần thiết.
- Có thể bật stack protector và Full RELRO để tăng hardening chung, dù chúng không giải quyết việc topology được nhúng phía client.

## Kết luận

`TunnelMadness` là bài reverse/graph extraction hơn là bài khai thác memory corruption. Điểm cốt lõi là mảng maze 20³ cell được nhúng nguyên trong `.rodata` và hàm index hóa rất rõ; hướng học thuật phù hợp là parse cấu trúc rồi BFS offline. Không có exploit hay chuỗi lời giải hoàn chỉnh trong ghi chú này.
