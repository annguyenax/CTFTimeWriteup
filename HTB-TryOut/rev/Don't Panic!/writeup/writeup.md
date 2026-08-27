# Don't Panic!

**Challenge:** HTB TryOut 2026 — rev / easy — tác giả: makelaris
**File:** `files/rev_dontpanic.zip` → `rev_dontpanic/dontpanic` (ELF64 x86-64, ~3,8 MB, viết bằng Rust)

---

## 1. Tổng quan / Overview

Câu chuyện đưa người chơi vào vai một điệp viên cần vô hiệu hóa robot dò nhiệt
(heat-signature detection robot) để vào kho vũ khí. Chương trình là một ELF 64-bit
viết bằng Rust: nó hỏi "Have you got a message for me?" (bạn có nhắn gì không),
đọc một dòng từ stdin, kiểm tra chính xác chuỗi 31 ký tự, in **"All is well 😌"**
nếu đúng và **"You made me panic! 😱"** nếu sai.

**Flag:** `HTB{d0nt_p4n1c_c4tch_the_3rror}` (31 ký tự)

Độ khó *easy*: chỉ cần strings + đọc disassembly là ra — không có packing,
không có anti-debug, không mã hóa phức tạp. "Obfuscation" duy nhất là mỗi ký tự
của flag bị tách thành một closure nhỏ so sánh một byte, và thứ tự 31 closure đó
được ráp lại qua một mảng con trỏ hàm dựng ngầm trong prologue của `check_flag`.

## 2. Triage

- `file` (hexdump 16 byte đầu): `7F 45 4C 46 02 01 01 00` → ELF64 little-endian.
- `strings` thấy rất nhiều chuỗi của Rust stdlib (`/rustc/9b00956...`,
  `library/std/...`, `panic_unwind`...) → binary Rust, không stripped.
- Chuỗi đặc trưng của challenge: `" You made me panic! "` @ 0x47085 và
  prompt `"src.rs🤖💬 < Have you got a message for me? >"` @ 0x47000 →
  file nguồn tên `src.rs`, giao diện đọc stdin.
- `objdump -t` → binary **giữ nguyên symbol table**:
  - `_ZN3src10check_flag17h...E` @ 0x9060 (0x1c1 byte) — hàm kiểm tra
  - `_ZN3src4main17h...E` @ 0x9230 — main của Rust
  - `_ZN3src14remove_newline17h...E` @ 0x9030
- Tổng 16.887 chuỗi in được; không thấy `HTB{` thô → flag bị giấu qua logic.

## 3. Phân tích / Analysis

`main` (0x9230): in prompt → `stdin.read_line()` → `remove_newline` (bỏ `\n`) →
gọi `check_flag(buf, len)` → nếu qua hết, in "All is well".

`check_flag` (0x9060) — cấu trúc rất gọn:

```asm
check_flag(rdi = buf, rsi = len):
    ; prologue: dựng bảng 31 con trỏ hàm trên stack
    lea 0x8b80,%rax ; mov %rax,0x10(%rsp)   ; ...
    ... (31 lần lea + mov vào [rsp+0x10 .. rsp+0x100])
    cmp $0x1f,%rsi          ; len phải = 31
    jne assert_failed       ; nếu không -> panic
loop:
    movzbl (buf,rax),%edi   ; lấy ký tự thứ i
    call *0x10(%rsp,%rax,8) ; gọi closure thứ i với ký tự đó
    ... 31 lần, i = 0..30
    ret
```

Mỗi closure kiểm tra (tất cả cùng khuôn mẫu, ví dụ @0x8b80):

```asm
push %rax
cmp $0x48,%dil     ; ký tự phải bằng 0x48 = 'H'
jb  panic
jne panic
pop %rax
ret
```

→ Nghĩa là: **flag[i] = hằng số được so trong closure thứ i của bảng**.
Bảng 31 con trỏ hàm (đọc từ prologue) ứng với 19 closure khác nhau, ví dụ
`0x8b80→'H'`, `0x8d80→'T'`, `0x8d40→'B'`, `0x8e00→'{'`, `0x8e40→'d'`,
`0x8c00→'0'`, `0x8c80→'n'`, ... `0x8ec0→'}'`.

Ghép theo thứ tự bảng:
`H T B { d 0 n t _ p 4 n 1 c _ c 4 t c h _ t h e _ 3 r r o r }`

## 4. Exploit

Không cần chạy binary (đây là ELF Linux, máy Windows không có glibc để chạy).
`solve/solve.py` thực hiện trích xuất hoàn toàn từ bytes của file:

1. Đọc ELF, map VMA → file offset qua program headers.
2. **Giả lập prologue** của `check_flag` (giải mã `lea disp32(%rip)` + các
   `mov %rX,[rsp+slot]`, bám theo thanh ghi rax/rcx/rdx/rdi) → lấy đúng bảng
   31 con trỏ hàm đúng thứ tự.
3. Với mỗi địa chỉ trong bảng, đọc hằng số từ `cmp $imm,%dil`
   (byte pattern `50 40 80 FF NN`).
4. Ghép flag, kiểm tra định dạng `HTB{...}`, độ dài 31 và **replay toàn bộ
   31 phép so sánh** đúng như binary.

Chạy:

```
python solve/solve.py
```

Kết quả:

```
[+] recovered 31 function-pointer entries
[+] 19 distinct checker closures: 0x008a40 -> 'h' ... 0x008ec0 -> '}'
[+] raw bytes : b'HTB{d0nt_p4n1c_c4tch_the_3rror}'
[+] VERIFIED: all 31 bytes replay the binary check logic; format HTB{...} OK
[+] wrote final_flag.txt: HTB{d0nt_p4n1c_c4tch_the_3rror}
```

Xác minh độc lập: trace tay qua objdump và script tự phân tích ELF cho ra kết
quả trùng khớp từng byte. (Thử chạy runtime qua WSL docker-desktop không khả thi
— distro thiếu glibc loader — nhưng việc replay logic trong Python từ chính
các hằng số của file đã đủ xác minh.)

## 5. Flag

```
HTB{d0nt_p4n1c_c4tch_the_3rror}
```

## 6. Bài học / Lessons

- **Symbol table là mỏ vàng:** binary Rust "không stripped" giữ nguyên tên hàm
  (`src::check_flag`, `src::remove_newline`) — luôn chạy `objdump -t` trước khi
  đào sâu, chỉ cần disassemble đúng hàm.
- **Rust dựng closure `call_once` cho mỗi lần so sánh byte** — một cách "obfuscation"
  tự nhiên: flag nằm rải rác thành các hằng số `cmp $imm,%dil` trong hàng loạt
  hàm nhỏ, và thứ tự thật sự nằm trong mảng con trỏ hàm.
- **Prologue dựng mảng trên stack bằng `lea` + `mov`** rất dễ giả lập: chỉ cần
  bám 4 thanh ghi (rax/rcx/rdx/rdi) và ghi nhận các store là tái dựng được toàn
  bộ cấu trúc dữ liệu — không cần emulator đầy đủ.
- **Không bao giờ tin flag trước khi verify:** replay logic kiểm tra trong Python
  từ chính byte constants của file (hoặc 2 cách trích xuất độc lập khớp nhau)
  là tiêu chuẩn tối thiểu trước khi ghi `final_flag.txt`.
- Mẹo nhỏ: trên Windows, các chuỗi chứa dấu `'`/`!` làm hỏng `python -c` trong
  PowerShell — hãy viết script ra file thay vì inline.
