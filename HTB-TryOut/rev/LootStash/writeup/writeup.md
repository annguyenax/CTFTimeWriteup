# LootStash

**Category:** rev — **Difficulty:** very easy — **Author:** makelaris — **Event:** HackTheBox CTF Try Out

## 1. Tổng quan / Overview

Challenge cung cấp một file ELF 64-bit `stash` (30.704 bytes). Flavor text gợi ý
một "kho chiến lợi phẩm" khổng lồ (loot stash) gồm nhiều item, và ta cần lọc ra
đúng thứ mình cần — tức là flag bị giấu giữa một loạt chuỗi tên item. Đây là một
bài rev rất dễ: flag nằm nguyên văn (plaintext) trong `.rodata` của binary, chỉ
cần quét `strings` là thấy.

**Flag:** `HTB{n33dl3_1n_a_l00t_stack}`

## 2. Triage

- `chalenge.md`: rev, difficulty **very easy**, author makelaris.
- Giải nén `files/rev_lootstash.zip` → `rev_lootstash/stash`.
- Magic bytes `7F 45 4C 46 02 01 01 00` → ELF 64-bit, little-endian, không packed.
- `strings` quét nhanh: xuất hiện ngay `HTB{n33dl3_1n_a_l00t_stack}` cùng hàng
  loạt tên item ngẫu nhiên kiểu `"Mirage, Bead of Secrets"`, `"Lightbane, Crusader
  of Trembling Hands"` — đúng chủ đề "loot stack".

## 3. Phân tích / Analysis

- Định vị chuỗi flag bằng tìm kiếm byte thô: offset **15440 (0x3C50)** trong
  section `.rodata` (vaddr 0x3000, size 0x20CB) — xác nhận bằng parse ELF section
  header. Đây là kết quả trùng khớp độc lập thứ hai với `strings`.
- Disassembly `.text` (0x20C0, chỉ 0x1C6 byte) bằng Capstone cho thấy `main`
  in banner `"Diving into the stash - let's see what we can find."`, đọc input,
  tính một index (phép nhân/`mul` với hằng số, kiểu `rand() % N`) rồi in ra một
  item từ bảng con trỏ. Toàn bộ tên item — trong đó có flag — là các chuỗi
  plaintext nằm cạnh nhau trong `.rodata`; chương trình không mã hóa gì cả.
- Không có XOR, không có encode, không có anti-RE. Ý tưởng bài chỉ là "cây kim
  trong đống rơm" (needle in a loot stack): flag là 1 trong ~170 chuỗi item.

## 4. Exploit

Không cần khai thác — chỉ cần trích xuất tĩnh:

```python
import re
data = open("stash", "rb").read()
flags = re.findall(rb"HTB\{[^}]+\}", data)   # -> [b'HTB{n33dl3_1n_a_l00t_stack}']
print(flags[0].decode())
```

Hoặc đơn giản: `strings stash | grep HTB`. Solver đầy đủ tại `solve/solve.py`
(thực hiện quét chuỗi + verify byte thô tại offset + xác nhận section `.rodata`).

## 5. Flag

```
HTB{n33dl3_1n_a_l00t_stack}
```

## 6. Bài học / Lessons

- Với rev easy, luôn bắt đầu bằng `strings`/`file`/scan header trước khi nghĩ tới
  decompiler — rất nhiều challenge để flag plaintext trong `.rodata`.
- "Độ khó" đôi khi nằm ở việc lọc nhiễu (nhiều chuỗi tên item) chứ không phải ở
  độ phức tạp thuật toán; grep theo pattern `HTB{...}` là đủ.
- Kỷ luật xác minh: một candidate chỉ được coi là flag khi khớp định dạng
  `HTB{...}` **và** được tái hiện độc lập từ chính bytes của file (ở đây: hai
  phép trích xuất khác nhau — regex strings và tìm kiếm byte thô tại offset —
  cho cùng một kết quả).
