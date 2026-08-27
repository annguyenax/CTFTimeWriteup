# any_secrets_could_instantly_be_imparted — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
Đề chỉ có một đoạn hội thoại và một chuỗi bí ẩn:

> Cody and Tiger have just had an argument...
> **Tiger: Et tu, Brute?**
> **Cody: `HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y`**
> Flag có dạng `LITCTF{...}`.

Nhiệm vụ: giải mã chuỗi của Cody ra flag.

## 2. Kiến thức nền

**Mã Caesar (Caesar cipher / shift cipher).** Mỗi ký tự được "dịch" đi một số vị trí cố định. Ví dụ dịch +3: `A→D`, `B→E`... Đây là mã cổ điển gắn với **Julius Caesar**.

**Câu "Et tu, Brute?"** là lời Caesar nói với Brutus (kẻ ám sát ông). Trong CTF, "Brute/Brutus" là gợi ý kép:
- Nhắc tới **Caesar** (mã Caesar),
- Nhắc tới **brute-force** (thử tất cả các phép dịch).

**Điểm mấu chốt:** ciphertext không chỉ chứa chữ cái mà còn có `?`, `=`, `)`, `-`, `_`, `/`, số... Vậy phép dịch **không** giới hạn trong bảng chữ A–Z, mà thực hiện trực tiếp trên **giá trị byte ASCII** của mỗi ký tự (rồi lấy mod 256).

## 3. Quá trình phân tích

Ta đã biết flag bắt đầu bằng `LITCTF{`. So từng cặp ký tự đầu ciphertext ↔ plaintext để tìm độ dịch:

| Cipher | ASCII | Plain | ASCII | Δ |
|--------|-------|-------|-------|---|
| `H` | 72 | `L` | 76 | +4 |
| `E` | 69 | `I` | 73 | +4 |
| `P` | 80 | `T` | 84 | +4 |
| `?` | 63 | `C` | 67 | +4 |
| `P` | 80 | `T` | 84 | +4 |
| `B` | 66 | `F` | 70 | +4 |
| `w` | 119 | `{` | 123 | +4 |

Độ dịch cố định **+4** khớp hoàn hảo → đúng là Caesar trên byte ASCII.

## 4. Lý do chọn kỹ thuật
Gợi ý "Et tu, Brute?" trỏ thẳng tới Caesar; bảng ký tự hỗn hợp cho biết dịch trên byte ASCII chứ không phải chỉ chữ cái. Vì không gian khóa chỉ có 256 khả năng, cách chắc chắn nhất là **brute-force toàn bộ shift** và giữ kết quả bắt đầu bằng `LITCTF{` và kết thúc bằng `}`.

## 5. Các bước khai thác / giải
1. Với mỗi shift `s` từ 0..255, tính `chr((ord(c)+s) % 256)` cho từng ký tự.
2. Giữ kết quả thỏa `startswith('LITCTF{')` và `endswith('}')`.
3. Chỉ có `s = 4` cho ra flag hợp lệ.

## 6. Solver tối thiểu
```python
ct = 'HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y'
for s in range(256):
    dec = ''.join(chr((ord(c)+s) % 256) for c in ct)
    if dec.startswith('LITCTF{') and dec.endswith('}'):
        print(s, dec)
```
Xem `../solve/solve.py`.

## 7. Cách xác minh flag
Xác minh mạnh bằng **giải mã rồi mã hoá lại**: dịch flag ngược -4 phải tái tạo **đúng từng byte** ciphertext gốc.
```
python solve.py
# shift = +4
# flag  = LITCTF{ASCII-jUl1us-c43s4r-gewowa}
# round-trip re-encryption OK
```

## 8. Flag
```
LITCTF{ASCII-jUl1us-c43s4r-gewowa}
```
Nội dung flag tự nó xác nhận chủ đề: **ASCII** + **Julius Caesar** (`jUl1us-c43s4r`).

## 9. Bài học & lỗi thường gặp
- **Đọc gợi ý văn học:** "Et tu, Brute?" = Caesar. Nhiều tên đề/độ khó ẩn manh mối kỹ thuật.
- **Đừng giả định Caesar chỉ trên A–Z.** Khi ciphertext có ký hiệu/số, hãy dịch trên **byte ASCII** (mod 256), nếu không sẽ giải sai hoặc "không ra gì".
- **Brute 256 khóa là miễn phí.** Không gian khóa Caesar rất nhỏ; luôn brute + lọc theo định dạng flag thay vì đoán bằng mắt.
- **Xác minh bằng round-trip** để chắc chắn, thay vì chỉ "trông giống flag".
