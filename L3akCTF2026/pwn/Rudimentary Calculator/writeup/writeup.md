# Rudimentary Calculator — Writeup (L3akCTF 2026, pwn)

- **Flag:** `L3AK{s3Arch_f0r_Sm0otH}`
- **Trạng thái:** ✅ Verified (exploit chạy end-to-end trên instance chính thức)
- **Điểm/Solves:** 91 / 82 (dễ nhất nhóm pwn)
- **File:** `files/pwn_rudimentary-calculator.tar.gz` → `chall`, `chall.c`, `Dockerfile`
- **Bảo vệ:** PIE + Stack Canary + NX + Full RELRO (BIND_NOW)

---

## 1. Đề bài yêu cầu gì

Một "máy tính" chỉ hỗ trợ **nhân** các chữ số hex đơn (`d*d*...*d`). Kết quả lưu trong một **bignum** (mảng `uint32_t`) rồi in ra hệ thập phân. Có hàm `win()` đọc `flag.txt` nhưng không được gọi.

## 2. Kiến thức nền

- **Bignum tràn mảng:** `product_bignum[0x60]` (96 limb) nằm trên stack; `multiply_digit` ghi `product_bignum[len]` và tăng `len` khi có carry, **không giới hạn 0x60** → nhân đủ lớn thì tràn qua canary/return.
- **Stack canary:** giá trị bí mật ở `rbp-8`; nếu bị ghi đè sai → `__stack_chk_fail` → abort. Nằm **giữa** bignum và return → phải leak + giữ đúng.
- **`scanf("%s")` dừng ở WHITESPACE, không phải NULL:** cho phép nhúng byte `\x00` → parser dừng ở null nhưng scanf vẫn ghi tiếp → **ghi byte tùy ý** lên stack.

## 3. Phân tích — layout stack (từ disasm)

```
buf[0x1000]           @ rbp-0x1190   (offset 0)
int len               @ rbp-0x190    (buf offset 0x1000)
uint32_t bignum[0x60] @ rbp-0x18c    (buf offset 0x1004)   bignum[0]
canary                @ rbp-0x8      (buf 0x1188 = bignum limb 97,98)
saved rbp             @ rbp+0        (buf 0x1190 = limb 99,100)
return address        @ rbp+8        (buf 0x1198 = limb 101,102)
```
`win = 0x1289`, return-into-main = `0x1a9b` (sau `call run`).

## 4. Hai primitive & lý do chọn

**Primitive ghi tùy ý (scanf-null):** gửi `'1' + '\x00' + <đệm> + ...`. Parser thấy `'1'` (tính 1×…) rồi gặp `\x00` → dừng. Nhưng `scanf("%s")` đã ghi TOÀN BỘ token (kể cả sau null) lên stack, tràn `buf` → ghi đè `len`, bignum, canary, rbp, return bằng **byte chính xác** ta chọn (miễn không chứa whitespace).

**Primitive leak (len corruption):** ghi đè `len` (int tại `buf+0x1000`) thành 103. Khi đó `to_base_10` đọc 103 limb (vượt qua canary/return) và **in cả stack dưới dạng số thập phân khổng lồ**. Bóc các limb 97–102 ra được **canary** và **return address** → suy ra PIE base → `win`.

*Vì sao cần leak?* Canary nằm giữa bignum và return; muốn ghi return phải ghi đè canary → phải biết canary thật để ghi lại đúng. PIE ngẫu nhiên nên cần return-leak để tính `win`.

## 5. Các bước khai thác (trong MỘT kết nối)

1. **Leak:** gửi `'1'\x00` + đệm tới `buf+0x1000`, đặt `len=103`, KHÔNG chạm bignum[97..102] (để chúng còn là canary/return thật). `multiply_digit(1)` giữ nguyên (nhân 1). Đọc `Result: <N>` → limb97|limb98<<32 = canary; limb101|limb102<<32 = return → `pie = ret-0x1a9b`, `win = pie+0x1289`.
2. **Ghi:** gửi payload dài `0x11a0` byte: đặt `len=103`, `bignum[97,98]=canary` (đúng), `bignum[101,102]=win`. `multiply_digit(1)` giữ nguyên các byte này.
3. **quit:** vòng lặp reset `len=1, bignum[0]=1` (không chạm canary/return đã ghi) → `strcmp("quit")` → `run()` trả về → canary khớp → `ret` vào `win()` → in flag.

*Ràng buộc:* canary & win không được chứa byte whitespace (scanf sẽ cắt). Nếu có → reconnect (canary/PIE mới). Xác suất ~75%/kết nối; ở đây trúng ngay attempt 0.

Solver: [solve/exploit.py](../solve/exploit.py). Chạy: `python solve/exploit.py`.

## 6. Cách xác minh flag

Exploit chạy trên instance chính thức, `win()` đọc `flag.txt` in ra `L3AK{s3Arch_f0r_Sm0otH}`. Leak nhất quán (canary LSB=0x00, `ret&0xfff==0xa9b`, `pie&0xfff==0`).

## 7. Bài học & lỗi thường gặp

- **`scanf("%s")` KHÔNG dừng ở null** — nhúng `\x00` để "qua mặt" parser mà vẫn overflow bằng byte tùy ý. Đây là mấu chốt (khác với đọc dòng có kiểm tra độ dài).
- **Corrupt biến độ dài (`len`)** biến hàm in-số thành **oracle leak stack** — kỹ thuật tổng quát cho mọi "print bignum/array theo len".
- **Canary chặn overflow tuần tự** → phải leak + ghi lại đúng; nhớ canary LSB luôn 0x00.
- **Lỗi thường gặp:** tưởng phải điều khiển GIÁ TRỊ bignum để ghi return (bất khả thi vì bignum là tích các chữ số) — thực ra primitive ghi là **scanf**, còn bignum chỉ để leak.
- Bug nhỏ khi code: chờ prompt `> ` hai lần trong khi server đã in kèm `Result:` → treo recv; luôn recv_until `> ` để phân định mỗi vòng.

## 8. Đường đi nhanh lần sau

Bignum-print theo `len` + canary + `scanf("%s")` + `win()` ⇒ (1) corrupt `len` để leak canary/PIE, (2) scanf-null ghi canary+win, (3) quit. Reconnect nếu byte trúng whitespace.
