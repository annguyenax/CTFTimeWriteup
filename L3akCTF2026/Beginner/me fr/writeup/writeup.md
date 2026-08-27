# me fr — Writeup (L3akCTF 2026, Beginner/misc)

- **Flag:** `L3AK{WHY_D0_1_dO_TH1S_s0_0f73N...}`
- **Trạng thái:** ✅ Verified (một phép thế giải nhất quán cả văn bản lẫn flag)
- **Điểm/Solves:** 59 / 315
- **File:** `files/me_fr.txt` (170 byte)

---

## 1. Đề bài yêu cầu gì

Prompt: *"monkey type has nothing on me fr no cap"*. "Monkeytype" là web luyện gõ phím. File `me_fr.txt` chứa một đoạn text méo mó:

```
Jo! Sp O was tjomlomg/// tu[omg os kist sp jard mpwadaus! :pplomg at upir jamds
wjo;e upi tu[e os omfiroatomg. Amuwaus. jeres tje f;ag" :3AL}WJU+D-+1+dP+TJ1S+s-+-f83M///|
```

Nhiệm vụ: giải mã để lấy flag.

## 2. Kiến thức nền

Đây là **keyboard shift cipher** (mật mã lệch phím): người gõ đặt tay sai vị trí nên mỗi phím bấm ra ký tự nằm cạnh phím định gõ. Rất phổ biến khi **tay phải bị lệch sang phải 1 phím** trên bàn phím QWERTY: mọi phím tay phải (y u i o p, h j k l, n m, và dấu câu bên phải) ra thành phím ngay **bên phải** nó; tay trái (q w e r t, a s d f g, z x c v b) và số 1–5 gõ đúng.

Muốn giải: với mỗi ký tự thuộc vùng tay phải, thay bằng phím **ngay bên trái** trên cùng hàng vật lý, giữ nguyên trạng thái Shift (chữ hoa/ký tự).

## 3. Phân tích & lý do chọn kỹ thuật

Nhìn từ đầu: `Jo!` → `Hi!` (j→h, o→i), `tjomlomg` → `thinking` (j→h, o→i, m→n, l→k, o→i, m→n; t và g là tay trái nên giữ nguyên). Quy luật "mỗi phím tay phải lệch sang phải 1 nấc" khớp hoàn hảo → đây chính là cipher cần giải. Gợi ý "monkey type / typing" trong đề xác nhận.

## 4. Các bước khai thác

1. Dựng 4 hàng phím QWERTY (bản thường và bản Shift), gồm cả `\|`.
2. Với mỗi ký tự tại chỉ số ≥ 6 trong hàng (vùng tay phải thực sự được gõ), map về ký tự chỉ số −1 (phím bên trái), giữ nguyên lớp Shift.
3. Áp lên toàn bộ file.

Solver: [solve/solve.py](../solve/solve.py). Chạy:

```bash
python solve/solve.py files/me_fr.txt
```

Kết quả decode:

```
Hi! So I was thinking... typing is just so hard nowadays! Looking at your hands
while you type is infuriating, Anyways, heres the flag: L3AK{WHY_D0_1_dO_TH1S_s0_0f73N...}
```

Chi tiết phần flag: `:`→`L`, `}`→`{`, `+`→`_` (đều là dấu bên phải lệch trái), `-`→`0`, `L`→`K`, `|`→`}`. Các số 1,3 và chữ tay trái giữ nguyên.

## 5. Cách xác minh flag

Cùng một bảng thế duy nhất giải ra **một câu tiếng Anh hoàn chỉnh, đúng ngữ pháp** *và* flag đúng khung `L3AK{}` với nội dung leetspeak có nghĩa ("WHY DO I DO THIS SO OFTEN..." = "0f73N" ≈ often). Xác suất trùng hợp gần như 0 → verified.

## 6. Bài học & lỗi thường gặp

- **Nhận diện:** text tiếng Anh "gần đúng" (nhiều từ chỉ sai 1–2 chữ, các chữ sai luôn là phím kề bên) ⇒ nghĩ ngay tới keyboard shift. Kiểm tra hướng lệch bằng 1–2 từ đoán được.
- **Lỗi #1 — chọn sai hướng:** lệch trái vs phải khác nhau. Ở đây tay phải lệch **phải**, nên decode bằng cách lùi **trái**.
- **Lỗi #2 — quên hàng số & dấu:** `+ - / | : }` đều lệch; phải đưa cả hàng số và các phím `[]\;'` vào bảng, kèm bản Shift, nếu không flag sẽ sót ký tự (ví dụ `|`→`}`).
- **Lỗi #3 — coi `...` là placeholder:** ba dấu `...` trong flag là **một phần thật** của flag (từ `///`), không phải chỗ bị che.

## 7. Đường đi nhanh lần sau

Text "sai chính tả theo phím kề" → dựng map QWERTY shift ±1, thử cả 2 hướng, chọn hướng ra tiếng Anh. Xong ~3 phút.
