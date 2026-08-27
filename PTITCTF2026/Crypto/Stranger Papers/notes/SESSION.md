# Stranger Papers — SESSION (đã giải xong)

- **Status:** SOLVED — có flag.
- **Flag:** `PTITCTF{21.0286_105.8356}`
- **Điểm:** 500
- **Ngày:** 2026-08-22 (giải lại)

## Prompt (verbatim)

```
Stranger Papers — 500 pts
[PHÒNG THÍ NGHIỆM HAWKINS - TỐI MẬT] — 6/11/1983, dự án "Stranger Papers".
Tín hiệu Phân khu 4 mất liên lạc; các nhà nghiên cứu để lại tập tài liệu mã hóa.
Những trang giấy nắm giữ tọa độ duy nhất nối liền thế giới của chúng ta và The Upside Down.
Một thứ gì đó rò rỉ từ hư không và làm biến dạng dữ liệu.
```

## Mô hình (đã xác nhận)

1. Zip 502 ảnh (455 jpg + 47 HEIC), **chỉ 22 hash unique** → chuỗi 502 ký hiệu trên bảng 22 chữ.
2. Mỗi unique = 1 chữ viết to trên giấy rồi **gấp (blintz)** → chỉ thấy nét ở 4 góc.
3. Chuỗi 502 = **substitution đơn bảng** (IC ≈ 0.078).

## Bước ngoặt: plaintext là TIẾNG VIỆT, không phải tiếng Anh

- IC 0.078 quá cao cho English (0.066); 22 ký hiệu đúng bằng **bảng chữ cái tiếng Việt không dấu**
  (`a b c d e g h i k l m n o p q r s t u v x y` — không có f/j/w/z).
- Mọi solver English (quadgram / dictionary / quipqiup) đều kẹt ở local optimum "AND…AND…AND".
- Chạy **quadgram tiếng Việt** (corpus từ vi.wikipedia, bỏ dấu) + simulated annealing → ra đoạn văn
  tiếng Việt liền mạch.

## Lời giải

Chạy `solve/solve.py` (hoặc `D:\download\ctf-scratch\ptitctf2026_stranger_papers\_solve_vi3.py`).

Plaintext (bỏ dấu, xem `solve/plaintext.txt`):

```
giua long ha noi on ao mot khoang san gach co van lang le duoi nhung tan cay xanh mat
ngoi reu phong cong tam quan gieng nuoc vuon va khue van cac thanh nha khien nguoi ta
nhu buoc vao mien ky uc xa xua nhung tam bia tren lung rua da ghi ten cac bac hien tai
nhac rang tri thuc la nen mong cua quoc gia ...
```

Khôi phục dấu: *"Giữa lòng Hà Nội ồn ào, một khoảng sân gạch cổ vẫn lặng lẽ … **Khuê Văn Các**
… những tấm **bia trên lưng rùa** … truyền thống **hiếu học** của dân tộc …"*

→ Địa điểm: **Văn Miếu – Quốc Tử Giám** (Hà Nội).

"Tọa độ" đề bài hỏi = tọa độ Văn Miếu: **21.0286° N, 105.8356° E**.

## Flag

```
PTITCTF{21.0286_105.8356}
```

## Việc đã bỏ qua / dead ends

- EXIF GPS (21.2792,105.7208 và 21.00845,105.81793) là nơi chụp ảnh → red herring.
- Không cần đọc ảnh gấp; substitution bị phá bằng thống kê (quadgram tiếng Việt).
- Solver scratch: `D:\download\ctf-scratch\ptitctf2026_stranger_papers\_solve_vi3.py` (key đầy đủ).
