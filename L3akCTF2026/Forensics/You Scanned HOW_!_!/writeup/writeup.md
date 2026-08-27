# You Scanned HOW?!?! — dựng radiograph dọc từ 617 CT slice

## Tóm tắt

Phần revenge mở rộng ý tưởng của `You Scanned WHAT?!?` từ một ảnh 2D thành một
volume. SQLite chứa 617 bảng slice ở các cao độ 0, 3, 6, ..., 1848 cm; mỗi bảng
có 180 projection của mặt cắt 800×400.

Không cần chạy inverse Radon 617 lần. Lấy projection góc 0 của mọi slice, biến
column mean thành line integral, rồi xếp chúng theo cao độ sẽ tạo một longitudinal
radiograph. Sau khi khôi phục voxel spacing z=3 và deskew bằng PCA, tấm chữ 3D
hiện ra:

```text
L3AK{CT_Sc4Ns_R_JU57_L0tz_0F_Xr4y5!!!}
```

Trạng thái: **verified**. Hai replay từ archive gốc tạo PNG byte-identical với
SHA-256 `354c5578d38b5efd4e32094a5c3d15875a1be445ca9c77b24cee87dfd4b76004`.

## Đề bài yêu cầu gì?

Đề nói agent mang về một “scan” lớn hơn rất nhiều và gọi đây là revenge của phần
trước. Ta cần nhận diện representation, dựng nội dung và trả lời “nó là gì”. Gợi ý
phần trước cho biết nên kiểm tra projection/Radon trước DICOM hay định dạng ảnh
thông thường.

Artefact:

- `files/scan2.7z`, 43,776,137 byte;
- SHA-256: `7f1ee82b27d7d7a5886703e26082fde58705f4272b38c09ad0943d5f3e1e598c`;
- chứa `scan2.sqlite`, 1,168,048,128 byte;
- SQLite SHA-256:
  `626ea7fd01761cc448abb95823d4e3f91f6e1fcaad792db4a98362bba448c3c8`.

Môi trường đã xác minh: Python 3.13, NumPy 2.2.6 và Pillow 11.2.1.

## Kiến thức nền

### Từ CT slice đến volume

Mỗi CT slice là một mặt cắt 2D. Nếu có nhiều slice ở các vị trí z liên tiếp, xếp
chúng theo z sẽ tạo volume 3D. Ở đây mỗi slice chưa phải ảnh hoàn chỉnh mà vẫn là
180 projection góc.

Cách “đầy đủ” là inverse Radon từng slice rồi ghép 617 ảnh. Nhưng nếu mục tiêu là
xem vật thể từ một hướng, ta có thể chọn cùng một projection angle ở mọi slice và
xếp các vector đó lại. Kết quả là một **longitudinal radiograph**: ảnh X-ray nhìn
xuyên cả volume theo hướng đã chọn.

### Column mean và line integral

Giống phần trước, `light_values` lưu trung bình cột của canvas xoay. Projection CT
cần tổng dọc tia:

```text
line_integral(angle) = stored_mean(angle) × canvas_height(angle)
```

Với góc 0, chiều cao canvas lấy từ detector count ở góc 90.

### Voxel spacing

Một pixel theo x không nhất thiết bằng một slice theo z. Tên bảng cho biết z tăng
3 cm mỗi slice. Nếu hiển thị 617 slice thành 617 hàng mà không nhân 3, trục z bị
nén ba lần: chữ cao trở nên hẹp và khó đọc.

Sau khi scale z×3, tấm chữ vẫn xoay trong mặt phẳng. PCA trên foreground pixels
cho principal axis `79.126338°`; rotate theo góc này và chọn orientation đối diện
180° đưa chuỗi về chiều đọc đúng.

## Triage và phân loại

Archive listing chỉ có `scan2.sqlite`. `PRAGMA quick_check` trả về `ok`. Database
có 617 bảng khớp pattern:

```text
slice_0cm, slice_3cm, ..., slice_1848cm
```

Mỗi bảng có schema:

```text
angle_degrees INTEGER PRIMARY KEY
detector_count INTEGER
light_values TEXT
```

Tất cả bảng có 180 hàng. Detector profile của một slice:

```text
angle 0°   -> width 800, orthogonal height 400
angle 45°  -> width 850
angle 90°  -> width 400
maximum    -> 896 (padded detector axis)
```

Profile này khớp một ảnh 800×400 được rotate với expanded canvas; đường chéo xấp
xỉ `sqrt(800² + 400²) ≈ 894.4`.

## Vì sao không inverse Radon toàn bộ?

Mục tiêu cần tìm là nội dung của vật thể 3D. Dựng 617 mặt cắt 896×896 sẽ tốn nhiều
CPU và gần 2 GB nếu giữ float32 volume. Một longitudinal radiograph chỉ cần:

- 617 JSON arrays ở góc 0;
- 617 detector counts ở góc 90;
- khoảng 0.55 triệu sample thay vì toàn bộ 111,060 projection rows.

Thử 12 view cách nhau 15° cho thấy góc 0 giữ toàn bộ hình dạng tấm chữ, còn các
góc gần 90° nhìn tấm chữ gần edge-on và chỉ thấy các nét ngang. Vì vậy góc 0 là
view có information gain cao nhất.

## Thuật toán giải

1. Sắp xếp các bảng theo số trong `slice_<z>cm`.
2. Xác minh z spacing đồng nhất và bằng 3.
3. Với mỗi bảng, đọc projection 0° và detector count 90°.
4. Tính `line_integral = light_values × orthogonal_count`.
5. Center-pad vector 800 vào detector axis 896.
6. Stack 617 vector theo z và lật trục ảnh.
7. Contrast-normalize theo percentile 1 và 99.7.
8. Scale chiều cao ×3 để khôi phục physical spacing.
9. Lấy principal component của foreground pixels, rotate theo góc PCA.
10. Rotate 180° để chọn chiều đọc đúng.

## Lệnh tái tạo tối thiểu

Từ thư mục gốc event:

```powershell
python ".\Forensics\You Scanned HOW_!_!\solve\solve.py" `
  ".\Forensics\You Scanned HOW_!_!\files\scan2.7z" `
  ".\Forensics\You Scanned HOW_!_!\solve\evidence\calibrated_radiograph.png"
```

Solver giải nén SQLite vào subdirectory tạm dưới
`D:\download\ctf-scratch\l3akctf_you_scanned_how`, đọc database ở chế độ
read-only và tự xóa bản tạm khi kết thúc.

Ảnh kết quả:
[`solve/evidence/calibrated_radiograph.png`](../solve/evidence/calibrated_radiograph.png).

## Xác minh flag

Ảnh calibrated đọc được toàn bộ chuỗi trong braces. Leetspeak cũng tạo thành câu
nhất quán “CT scans are just lots of X-rays”, giúp phân biệt các ký tự dễ nhầm:

- `Sc4Ns`, chữ `N` hoa;
- `R` là một ký tự đại diện “are”;
- `JU57`, cả `JU` viết hoa;
- `L0tz`, gồm số 0 và chữ z thường;
- `0F`, số 0 rồi F hoa;
- `Xr4y5`, X hoa, r thường;
- ba dấu `!!!` nằm bên trong `}`.

Hai lần chạy độc lập từ archive gốc đều báo:

```text
slices: 617; z spacing: 3; PCA angle: 79.126338
sha256: 354c5578d38b5efd4e32094a5c3d15875a1be445ca9c77b24cee87dfd4b76004
```

Không submit lên scoreboard theo phạm vi học tập offline.

## Nhánh thử nghiệm và lỗi thường gặp

- **In toàn bộ schema:** 617 bảng tạo output rất lớn mà không thêm thông tin. Chỉ
  cần table count/range/spacing và schema một bảng mẫu.
- **Inverse Radon mọi slice ngay:** đúng về lý thuyết nhưng quá tốn so với một
  projection dọc đúng góc.
- **Xếp projection nhưng bỏ spacing:** tạo ra chữ bị nén 3× và dễ đọc sai.
- **Đoán góc deskew bằng mắt:** PCA cho góc tái lập và tránh tuning thủ công.
- **Dùng góc gần 90°:** tấm chữ bị nhìn edge-on, thông tin ký tự chồng lên nhau.
- **Đọc trước khi sửa orientation:** principal axis không có hướng; phải kiểm tra
  hai orientation cách nhau 180°.

## Bài học và đường nhanh

Khi gặp multi-slice tomography:

1. kiểm kê số slice, angle count, detector profile và physical spacing;
2. hỏi có thật sự cần reconstruct toàn volume không;
3. thử stack cùng projection angle để tạo orthographic radiograph;
4. chọn góc có silhouette giàu thông tin nhất;
5. hiệu chỉnh spacing trước rotate/deskew;
6. xác minh bằng deterministic archive-to-image replay.

HexStrike không được dùng: database cục bộ, SQLite và phép toán mảng nhỏ đã đủ;
chuyển file 1.168 GB sang Kali sẽ làm chậm workflow.

## Nguồn tham khảo

- [scikit-image: Radon transform](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html) — quan hệ giữa ảnh, projection và sinogram.
- [scikit-image API: `radon`/`iradon`](https://scikit-image.org/docs/stable/api/skimage.transform.html) — quy ước góc và detector của Radon transform.
- [NumPy `linalg.eigh`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html) — eigenvector dùng để lấy principal axis cho deskew.
