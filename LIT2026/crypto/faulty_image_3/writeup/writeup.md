# faulty_image_3 — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
> A hacker sent us another suspicious image. We don't know what to do with it.
> Maybe you do? **It's pretty colorful though...**

File: `corrupt3.png` (500×200), viền cam, chữ đỏ ở giữa. Gợi ý chính thức:
*"What does it being colorful remind you of? Do you see a part of the border that
is a different color than the rest?"* → dữ liệu nằm ở **màu của border**.

## 2. Cạm bẫy: flag hiển thị là DECOY
Ảnh render ra chữ đỏ `LITCTF{1mAg3_F1ag_1o3fjs!}`. **Đây là flag giả** — nộp sẽ sai.
Bài học: trong series này (bài 2, 4 cũng vậy), thứ nhìn thấy thường là mồi nhử.

## 3. Kiến thức nền
- **Kênh màu RGB.** Mỗi pixel có 3 byte R,G,B (0–255). Một byte có thể trùng khoảng
  ASCII in được (32–126), nên **có thể giấu văn bản trong một kênh màu**.
- **Ẩn dữ liệu bằng màu:** đặt các pixel "khác màu" xen kẽ, với **kênh R = ký tự flag**
  còn G,B để ngẫu nhiên → mắt thường chỉ thấy vài chấm "colorful", không đọc ra chữ.

## 4. Quá trình phân tích
1. Render ảnh → thấy chữ đỏ (decoy) + viền cam.
2. Theo gợi ý, soi **border**: màu chủ đạo là cam `(255,157,0)`.
3. Tìm pixel **khác màu** trên border:
   - Hàng trên cùng (y=0) có **30 pixel** xanh-tím, **cách đều 7px** (x=7,14,…,210).
   - Một khối nhỏ `(255,177,20)` ở viền dưới (mồi/đánh lạc hướng).
4. Đọc màu 30 mark đó. **Kênh R**: `76,73,84,67,84,70,123,…` = `L,I,T,C,T,F,{,…`
   → chính là flag! (Kênh G,B chỉ là nhiễu để pixel trông có màu.)

## 5. Lý do chọn kỹ thuật
Gợi ý "colorful" + "border khác màu" trỏ thẳng vào các pixel màu lạ trên viền.
Khi thử đọc từng kênh của chúng, **kênh R ra ASCII sạch bắt đầu `LITCTF{`** → xác nhận
đúng hướng ngay lập tức.

## 6. Solver tối thiểu
```python
import numpy as np; from PIL import Image
a=np.array(Image.open('corrupt3.png').convert('RGB'))
marks=[tuple(int(v) for v in a[0,x]) for x in range(a.shape[1]) if tuple(int(v) for v in a[0,x])!=(255,157,0)]
print(bytes(m[0] for m in marks).decode())   # kênh R
```
→ `LITCTF{p1x3l_p3rf3ct_98xzfq9!}`. Xem `../solve/solve.py`.

## 7. Cách xác minh
- 30 mark → 30 ký tự, kênh R ra chuỗi **in được**, đúng định dạng `LITCTF{…}`, kết thúc `}`.
- Chủ đề nội dung "p1x3l_p3rf3ct" (pixel perfect) khớp bản chất bài (giấu trong pixel màu).
- Solver tất định, chạy lại luôn cho cùng kết quả.

## 8. Flag
```
LITCTF{p1x3l_p3rf3ct_98xzfq9!}
```
(Flag giả cần tránh: `LITCTF{1mAg3_F1ag_1o3fjs!}`.)

## 9. Bài học & lỗi thường gặp
- **Đừng tin flag nhìn thấy** trong các bài "faulty image" — thường là decoy.
- **Giấu tin trong một kênh màu**: khi thấy pixel "màu lạ", hãy tách R/G/B và đọc từng kênh
  như byte/ASCII, đừng chỉ nhìn màu tổng hợp.
- Bám **gợi ý**: "colorful" + "border khác màu" = dữ liệu ở màu của viền.
- Chú ý **khoảng cách đều** (7px) — dấu hiệu của dữ liệu được đặt có chủ đích, không phải nhiễu.
