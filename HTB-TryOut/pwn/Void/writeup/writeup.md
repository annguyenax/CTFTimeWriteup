# Void

## 1. Tổng quan

- **Loại:** pwn (binary exploitation)
- **Độ khó:** medium
- **Tác giả:** makelaris
- **Mô tả:** Căn phòng tối đen, chỉ còn một chiếc terminal hỏng — hack vào để khôi phục nguồn điện và tìm đường ra.
- **Mục tiêu:** Khai thác buffer overflow trên binary chỉ import mỗi `read`, không leak, NX bật → dùng **ret2dlresolve** để gọi `system("cat flag*")`.

## 2. Thông tin instance

- **Target:** `154.57.164.83:30313` (TCP)
- File: `files/pwn_void.zip` (binary `void` không PIE, NX bật, không canary, kèm glibc 2.31 + ld).

## 3. Phân tích binary

```c
void vuln() {
    char buf[64];                  // rbp-0x40
    read(0, buf, 0xc8);            // <-- đọc 200 byte vào buffer 64 byte
}
int main() { vuln(); }
```

Đặc điểm khó:
- Chỉ import `read` — không có `puts`/`printf`/`system` → không leak được địa chỉ libc.
- Không có gadget `syscall` trong binary → không SROP.
- NX bật → không chạy shellcode trên stack.
- Có `__libc_csu_init` (ret2csu) và gadget `pop rdi; ret` (0x4011bb, misaligned từ `pop r15`).
- Đủ dữ kiện để **ret2dlresolve**: nhờ lazy binding, ta tạo giả cấu trúc `Elf64_Rela`/`Elf64_Sym`/strtab trong `.bss` để resolver tự tìm `system` trong libc mà không cần biết địa chỉ libc.

Offset đến saved RIP = `0x40 + 8 = 72`.

## 4. Khai thác

Hai giai đoạn (chuỗi ROP một giai đoạn dài hơn giới hạn đọc 200 byte):

**Giai đoạn 1** (đúng 200 byte — đệm để `read` tiêu thụ trọn):
- ret2csu: `read(0, 0x404e00, 50)` — ghi payload ret2dlresolve (fake strtab `"system"`, fake Rela, fake Sym, chuỗi `"cat flag*"`) vào `.bss`.
- `ret` về `main` (0x401143) để chạy lại `vuln()`.

**Giai đoạn 2** (overflow thứ hai):
- `pop rdi; ret` → `0x404e28` (con trỏ `"cat flag*"`)
- `ret` → `PLT0` (0x401020) → `reloc_index` (0x49f0) trên stack.

Cơ chế: khi ret vào PLT0, stack có `[link_map][reloc_index]`; `_dl_runtime_resolve` trong glibc 2.31 lưu/khôi phục thanh ghi — rdi được khôi phục về giá trị lúc vào resolver (chính là `0x404e28` do `pop rdi` đặt) → sau khi resolve xong `system`, nhảy vào `system(0x404e28)` = `system("cat flag*")` → in flag.

Lưu ý: không dùng `rop.ret2dlresolve()` tự động của pwntools vì nó không tìm thấy pop-rdi trong gadget DB của nó và đặt arg0 trên stack (không hoạt động trên x86-64).

## 5. Kết quả

```
HTB{pwnt00l5_h0mep4g3_15_u54ful}
```

## 6. Bài học

- **ret2dlresolve:** khi binary chỉ có `read`, không leak, có thể giả mạo bảng relocation để resolver tự nạp `system` từ libc — không cần biết địa chỉ libc (có glibc kèm theo thì càng chắc chắn).
- **ret2csu** để gọi hàm với 3 tham số khi thiếu gadget `pop rdi/rsi/rdx`.
- Giới hạn độ dài `read` → phải chia exploit nhiều giai đoạn và đệm payload cho khớp số byte đọc; `read` trên socket trả về ngay khi có dữ liệu.
- Hiểu cơ chế `_dl_runtime_resolve`: thanh ghi được lưu/khôi phục nên phải đặt `rdi` (tham số của hàm resolve) TRƯỚC khi vào PLT0.
