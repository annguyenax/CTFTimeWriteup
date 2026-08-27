# Satellite Hijack — Writeup (HTB Try Out · Reversing)

## 1. Đề bài yêu cầu gì
Một bảng điều khiển liên lạc với vệ tinh thời tiền-chiến bị kẻ thù "sửa" để chặn
các **control code** cần thiết khi truyền lệnh lên vệ tinh. Nhiệm vụ là khôi phục
lại các control code đó — tức tìm flag dạng `HTB{...}`.
Có 2 file ELF: `satellite` (chương trình chính) và `library.so` (thư viện chứa logic).

## 2. Kiến thức nền
- **ELF PIE x86-64**: file `.so` có thể tải nhiều lần, địa chỉ nội bộ tương đối.
- **memfrob(3)**: hàm GNU đảo byte bằng `XOR 42` — dấu hiệu của mã bị "giấu".
- **Kỹ thuật self-modifying / runtime unpack**: `mmap` một vùng RWX, `memcpy` mã,
  rồi `memfrob` (XOR 42) để khôi phục mã thật tại runtime.
- **`getenv`** làm cổng (gate): chỉ giải mã khi biến môi trường được đặt.

## 3. Phân tích (protections + hàm chính)
- **satellite (main @ 0x1185)**: in banner, gọi `send_satellite_message(0, ...)` một lần,
  rồi lặp: đọc dòng nhập → in lại → gọi `send_satellite_message(0, input)`.
- **`send_satellite_message` (0x25d0) — hàm export đã bị "tampered"**:
  dựng chuỗi tên biến môi trường bằng cách giảm 1 từng byte của 3 hằng số
  (`TB`UQSPE…` → `SAT_PRODENVIRONMENT`), rồi:
  `if (getenv("SAT_PRODENVIRONMENT")) unpack();`
  → Đây chính là "vết sửa" mà đề nhắc: logic control-code gốc bị thay bằng stub chỉ giải mã.
- **Unpacker 0x23e3**: `getauxval(AT_PHDR)` → `mmap` RWX → `memcpy` vùng
  `.text [0x11a9,0x21a9)` → `memfrob` (XOR 42). Vậy mã thật bị mã hoá trong file.
- **Giải mã offline**: vì địa chỉ `.text` == offset file nên
  `dec[i] = file[0x11a9+i] ^ 42` → được `library_dec.so`.

## 4. Vì sao chọn hướng này
Thấy import `memfrob` ngay từ TRIAGE ⇒ nghi ngờ runtime decrypt ⇒ bỏ qua việc chạy
động (chạy vô ích nếu chưa đặt env), thay vào đó **XOR 42 ngay trong file** rồi
disassemble vùng giải mã. Cách này tái lập đúng, không cần Kali và cho ra thuật toán
check ngay lập tức.

## 5. Các bước khai thác
1. Đọc disassembly: `satellite` chỉ gọi `send_satellite_message`; toàn bộ logic nằm ở `library.so`.
2. Nhận ra stub `send_satellite_message` = cổng `getenv(SAT_PRODENVIRONMENT)` → `unpack()`.
3. Giải mã vùng `[0x11a9,0x21a9)` bằng XOR 42 (splice lại vào bản patched).
4. Trong mã giải mã tìm thấy routine **0x11a9** scan `"HTB{"`, gọi checker **0x1235**.
5. Checker dựng key 28 byte từ 4 hằng số `movabs`:
   ```
   imms = 0x37593076307b356c, 0x3a7c3e753f665666, 0x784c7c214f3a7c3e, 0x663b2c6a246f21
   key  = "l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f"
   ```
   và yêu cầu với `i = 0..27`: `input[i] XOR key[i] == i`.
6. Suy ra 28 byte trong (sau `HTB{`): `inner[i] = key[i] ^ i` =
   `"l4y3r5_0n_l4y3r5_0n_l4y3r5!}"`.
7. Ghép lại: `HTB{` + inner.

## 6. Flag
```
HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}
```
(Hiểu là "layers on layers on layers!" — bài chơi trên nhiều lớp obfuscation:
stub → getenv gate → memfrob/runtime unpack → key-overlap trên stack.)

### Verify
- `solve/solve.py` đọc thẳng binary, giải mã vùng, trích 4 hằng số, dựng key đúng
  layout ghi-chồng của stack, tính `inner`, và **tái mô phỏng checker** (assert
  `key[i]^inner[i]==i` với i=0..27) — PASS.
- Đối chiếu thủ công các hằng số `movabs` + vòng `xor; cmp rax,rdx` với `objdump`
  — khớp chính xác. (2 cách độc lập đạt ngưỡng VERIFY của ctf-ai-system.)
