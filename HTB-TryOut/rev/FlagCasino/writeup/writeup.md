# FlagCasino

## 1. Tổng quan / Overview

- **Challenge:** FlagCasino (HackTheBox TryOut, rev, rất dễ)
- **File:** `files/rev_flagcasino.zip` → `casino` (ELF x86-64, 17.064 bytes, dynamic link, **không stripped** — còn đủ symbol `main`, `check`, `banner`)
- **Ý tưởng:** Một "sòng bạc robot" yêu cầu bạn đặt cược từng ký tự (bet) cho 29 vòng. Mỗi vòng chương trình gọi `srand(bet); rand()` rồi so sánh với một mảng hằng số `check[]`; sai một ký tự là `exit(-2)`. Đúng cả 29 vòng sẽ in "HOUSE BALANCE $0" (tức là đã phá sản nhà cái → thành công).
- **Kết quả:** Flag = `HTB{r4nd_1s_v3ry_pr3d1ct4bl3}` (29 ký tự).

## 2. Triage

- Giải nén zip bằng `Expand-Archive` → một file `casino` duy nhất.
- `strings`: thấy banner casino, các chuỗi `[ * CORRECT *]`, `[ * INCORRECT * ]`, `[ *** ACTIVATING SECURITY SYSTEM - PLEASE VACATE *** ]`, `[ ** HOUSE BALANCE $0 ... ** ]`, và import `srand`, `__isoc99_scanf`, `printf`, `rand` → chương trình đọc input, gieo seed rồi so sánh.
- Symbol table còn nguyên (`main`, `check`, `banner`, `main.c`, GCC 10.2.1) → không bị strip, chỉ cần `objdump` là đủ, không cần Ghidra/IDA.
- Các chuỗi "rác" không in được trong `.rodata` chỉ là phần nhị phân lệnh/điều khiển — không phải flag mã hoá.

## 3. Phân tích / Analysis

Disassembly `main` (x86-64):

```
for (i = 0; i <= 0x1c; i++) {            ; 29 vòng → flag 29 ký tự
    printf("> ");
    if (scanf("%c", &bet) != 1) exit(-1);
    srand(bet);                          ; seed = giá trị ký tự bet
    if (rand() != check[i]) {            ; check[] tại VA 0x4080 (.data)
        puts("[ * INCORRECT * ]");
        puts("[ *** ACTIVATING SECURITY SYSTEM - PLEASE VACATE *** ]");
        exit(-2);
    }
    puts("[ * CORRECT *]");
}
puts("[ ** HOUSE BALANCE $0 - PLEASE COME BACK LATER ** ]");
```

- Mảng `check` là 29 DWORD little-endian tại VA `0x4080` (lấy bằng pyelftools từ section `.data`, lưu ở `solve/evidence/check_array.txt`).
- Bản chất: với mỗi vị trí, cần tìm ký tự `c` sao cho `glibc srand(c); rand() == check[i]`. Vì `srand` chỉ nhận 1 byte, toàn bộ không gian seed chỉ có 256 giá trị → dễ vét cạn.

## 4. Exploit

1. **Trích mảng `check[]`:** pyelftools đọc `.data` tại VA 0x4080 → 29 DWORD.
2. **Lấy ground-truth của glibc `rand()`:** viết chương trình C nhỏ `srand(s); printf(rand())` với `s = 0..255`, biên dịch chạy trên glibc thật (Kali local) → bảng `seed → rand()` (lưu `solve/evidence/rand_table.txt`).
   - *Ghi chú:* lần đầu tôi tự viết lại thuật toán additive-feedback của glibc trong Python nhưng cho kết quả lệch; dùng bảng đo từ glibc thật là chuẩn và nhanh hơn.
3. **Tra ngược:** với mỗi `check[i]`, tìm seed printable (0x20–0x7E) có `rand()` khớp → ghép thành flag.
4. **Replay độc lập:** viết lại đúng vòng lặp của binary bằng C trên glibc thật, nhét đúng 29 DWORD từ file → `VERIFY PASS`.

Solver: `solve/solve.py` (đọc 2 file evidence, tra ngược bảng, tự xác minh replay).

## 5. Flag

```
HTB{r4nd_1s_v3ry_pr3d1ct4bl3}
```

- Ký tự tại các vị trí 8/11/16 (`_`), 13/19/27 (`3`), 7/20 (`d`), 9/21 (`1`) lặp lại → giá trị `check[]` lặp lại, khớp hoàn toàn với flag thật.
- Xác minh kép: (a) replay trong Python bằng bảng glibc thật — PASS; (b) replay native C trên glibc thật với đúng 29 DWORD lấy từ file — PASS.

## 6. Bài học / Lessons

- **Đừng tin vào việc tự viết lại thư viện:** thuật toán `rand()` của glibc rất dễ chép sai một chi tiết (pointer wrap, discard 309 giá trị khi gieo seed). Cách chắc chắn nhất là *đo* từ chính libc thật bằng một chương trình C nhỏ, hoặc chạy thẳng binary.
- **Sinh số ngẫu nhiên "bảo mật" phải dùng CSPRNG:** `srand(1 byte)` chỉ có 256 seed — vét cạn trong tích tắc. Đây chính là thông điệp của challenge: `r4nd` (rand) rất dễ **predictable**.
- **Khai thác tĩnh là đủ cho bài easy:** binary không stripped + logic đơn giản → `strings` + `objdump` + vài dòng Python là xong, không cần công cụ nặng.
- **Dấu hiệu nhận biết flag qua dữ liệu:** mảng hằng 29 DWORD với giá trị lặp lại là dấu vết rõ ràng của flag mã hoá theo từng ký tự.
