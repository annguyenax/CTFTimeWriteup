# Getting Started

## 1. Tổng quan

- **Loại:** pwn (binary exploitation)
- **Độ khó:** very easy
- **Tác giả:** makelaris
- **Mô tả:** Bài hướng dẫn cuối cùng trước exploit thật sự — "đã đến lúc thể hiện kỹ năng hack".
- **Mục tiêu:** Ghi đè giá trị `0xdeadbeef` trên stack để chương trình gọi hàm `win()` in flag.

## 2. Thông tin instance

- **Target:** `154.57.164.71:31025` (TCP)
- File đính kèm: `files/pwn_getting_started.zip` (binary `gs`, glibc, `wrapper.py` hướng dẫn gửi payload).

## 3. Phân tích binary

`main` (PIE, không canary):

```c
char buf[32];                 // rbp-0x30
long long alignment = 0x6969696969696969;  // rbp-0x10
long long target = 0xdeadbeef;             // rbp-0x8
...
scanf("%s", buf);             // <-- không giới hạn độ dài
show_stack(buf);
if (target != 0xdeadbeef)     // rbp-0x8 bị ghi đè
    win();                    // mở ./flag.txt, in từng ký tự
```

Layout stack: `[buffer 32B][alignment 8B][target 0xdeadbeef 8B][saved rbp][ret]`.
Để ghi đè `target`, cần `32 + 8 = 40` byte, cộng thêm 8 byte bất kỳ khác `0xdeadbeef` → tổng 48 byte.

## 4. Khai thác

Payload: `b"A" * 48` — 48 ký tự `A` ghi đè buffer (32), alignment (8) và target (8) → `target` không còn là `0xdeadbeef` → nhảy vào `win()` → in `flag.txt`.

## 5. Kết quả

```
HTB{b0f_tut0r14l5_4r3_g00d}
```

## 6. Bài học

- `scanf("%s")` / `gets` không giới hạn độ dài → buffer overflow kinh điển.
- Kỹ thuật "ret2win": khi có sẵn hàm in flag, chỉ cần ghi đè biến canh/giá trị kiểm tra hoặc return address để nhảy vào hàm đó.
- Luôn tính offset chính xác từ buffer đến vị trí cần ghi đè (ở đây 40 byte đến `target`).
