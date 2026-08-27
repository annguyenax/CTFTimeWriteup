# Leaky — Writeup (Kali Team CTF 26 / Pwn)

## 1. Đề bài yêu cầu gì?

- Binary ELF64 + `libc.so.6` + loader + `flag.txt` mẫu.
- Prompt: *"Good Luck!"*
- Lấy shell / đọc flag `KaliTeam{...}` (package: `KaliTeam{fake_flag}`).

## 2. Kiến thức nền

| Khái niệm | Vai trò |
|---|---|
| Stack buffer overflow | Ghi đè saved RIP |
| Format string (`printf(user)`) | Leak địa chỉ libc |
| Full RELRO | Không ghi GOT |
| ret2libc (`system("/bin/sh")`) | Shell sau khi có base libc |
| Căn stack 16 byte | `movaps` trong libc; ret2func qua `ret` (không `call`) |

## 3. Phân tích

### Protections

```
Full RELRO | No canary | NX | No PIE
```

### Hàm `challenge` (rút gọn)

1. `read(0, buf, 0x60)` với `buf` tại **`[rbp-0x10]`** → overflow rõ (0x60 > 0x10).
2. `printf(buf)` → **format string** (tham số format = buffer user).
3. `leave; ret`.

Offset tới saved RIP: `0x10 + 8 = 0x18` (hoặc `0x10` pad + 8 byte RBP + chain).

### Format string

Trên x64, `printf(fmt)` chỉ có `fmt` trong `rdi`. Các `%N$` lấy từ stack:

- **`$6`** = 8 byte đầu buffer  
- **`$7`** = 8 byte tiếp  

Đặt `puts@GOT` ở qword 2, dùng **`%7$s`** để in địa chỉ `puts` trong libc.

## 4. Vì sao chọn leak + ret2libc?

| Hướng | Kết luận |
|---|---|
| Chỉ BOF ROP trong binary | Gần như không có `pop rdi` |
| Ghi GOT | Full RELRO chặn |
| **Fmt leak libc + ret2libc** | Phù hợp file libc kèm theo |
| ret2challenge (2 stage) | Cần vì leak và ROP không gói chung một payload |

## 5. Các bước khai thác

### Stage 1 — leak + quay lại `challenge`

```text
[ %7$s + pad 8 ][ puts@GOT ][ fake_RBP ][ ret ][ challenge ]
```

- `printf` in bytes của `puts` rồi marker `AAAA`.
- `leave; ret` nhảy tới `challenge` **sau một gadget `ret`** để RSP % 16 == 0  
  (vì vào bằng `ret` chứ không phải `call`).

**Bẫy quan trọng:** thiếu `ret` căn chỉnh → stage 2 luôn SIGSEGV (kể cả chỉ ret2challenge lần nữa).

### Stage 2 — `system("/bin/sh")`

```text
[ pad 0x10 ][ fake_RBP ][ ret ][ pop rdi; ret ][ &"/bin/sh" ][ system ]
```

Gadget `pop rdi; ret` trong libc đính kèm: offset **`0x2a3e5`**.

## 6. Solver

`solve/solve.py`

```bash
python3 solve/solve.py
python3 solve/solve.py remote HOST PORT
```

## 7. Xác minh (local)

```text
BBBBBBBBBBBBBBBB
SHELL_OK
KaliTeam{fake_flag}
```

## 8. Bài học / lỗi hay gặp

| Lỗi | Ghi chú |
|---|---|
| Quên căn `ret` khi ret2self | Stage 2 chết im |
| Dùng `ROP(libc)` khi `context` 32-bit | Lỗi pack address |
| Nhầm offset fmt (`$6`/`$7`) | Leak sai / crash `%s` |
| Coi `fake_flag` là flag thi | Chỉ file mẫu trong zip |
| Full RELRO vẫn cố GOT write | Không vào |

## 9. Một dòng

**`printf(buf)` leak `puts@GOT` → `ret`-align → `challenge` lần 2 → ret2libc `system("/bin/sh")`.**
