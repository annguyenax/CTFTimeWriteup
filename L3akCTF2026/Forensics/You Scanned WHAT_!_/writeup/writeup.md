# You Scanned WHAT?!? — tái dựng ảnh từ các projection

## Tóm tắt

Archive không chứa ảnh y khoa hoàn chỉnh. Nó chứa một database SQLite với 180
phép chiếu của cùng một vật thể, mỗi phép chiếu ứng với một góc từ 0 đến 179 độ.
Sau khi biến các giá trị trung bình cột trở lại line integral và áp dụng filtered
backprojection (inverse Radon transform), ảnh hiện ra một nhân vật hình giọt/dâu
cầm cờ cùng chuỗi:

```text
L3AK{X-r4Y_C0mp13T3}
```

Trạng thái: **verified**. Solver được chạy độc lập hai lần từ archive gốc; hai PNG
đều có SHA-256
`aabee2bc31d0fca483346ed663ce37e9ecfd2d8b2fff8fc7cabd7bfd9cf2fdba`.

## Đề bài yêu cầu gì?

Đề cho một “scan” lấy từ bệnh viện và hỏi vật được scan là gì. Cách dùng từ này
gợi ý CT/X-ray, nhưng ta không nên giả định attachment là DICOM. Việc đầu tiên là
nhận diện container và dữ liệu thật bên trong.

File gốc:

- `files/scan.7z`, 190,594 byte;
- SHA-256: `e45a1da91290e654002c5c1ea49e5bf3caaad0e073dd76d848c2c2b6b955a92c`.

Môi trường đã xác minh: Python 3.13, NumPy 2.2.6, SciPy 1.15.2,
scikit-image 0.25.2 và Pillow 11.2.1. `tar.exe` của Windows được dùng để mở 7z.

## Kiến thức nền

### Projection và sinogram

Trong CT, một projection ghi tổng mức suy hao dọc theo nhiều tia song song ở một
góc nhất định. Xếp các vector projection của nhiều góc cạnh nhau tạo thành một
**sinogram**.

Phép biến đổi Radon đi từ ảnh sang các projection. **Inverse Radon transform** đi
chiều ngược lại. Một cách dựng phổ biến là filtered backprojection: lọc từng
projection bằng ramp filter rồi “trải ngược” nó qua mặt phẳng ảnh theo đúng góc.

### Vì sao phải nhân với chiều cao canvas?

Cột `light_values` không lưu tổng mà lưu trung bình cột trên ảnh đã xoay và mở
rộng canvas. Khi xoay ảnh chữ nhật, cả chiều rộng lẫn chiều cao canvas thay đổi.
Muốn có line integral dùng cho inverse Radon, ta khôi phục tổng:

```text
line_integral = column_mean × rotated_canvas_height
```

Với một hình chữ nhật, chiều cao ở góc `θ` chính là chiều rộng ở góc `θ + 90°`.
Database đã cho chiều rộng dưới tên `detector_count`, nên không cần đoán kích thước.

## Phân tích và lựa chọn kỹ thuật

Liệt kê archive trước, không chạy hay carve mù:

```powershell
tar -tf ".\Forensics\You Scanned WHAT_!_\files\scan.7z"
```

Kết quả chỉ có `scan.sqlite`, vì vậy giả thuyết DICOM bị loại. Database qua
`PRAGMA quick_check` trả về `ok`; schema có một bảng:

```text
projections(angle_degrees INTEGER PRIMARY KEY,
            detector_count INTEGER,
            light_values TEXT)
```

Có đúng 180 hàng cho các góc 0..179. `light_values` là JSON array và độ dài mỗi
mảng khớp `detector_count`. Chiều dài thay đổi từ 215 đến 543; đây là dấu hiệu
ảnh chữ nhật đã được rotate với canvas mở rộng, chứ không phải sinogram hình chữ
nhật đã pad sẵn.

Từ đó, đường giải ít giả định nhất là:

1. đọc các hàng theo thứ tự góc;
2. parse JSON array;
3. nhân mỗi vector với chiều cao canvas suy ra ở góc lệch 90°;
4. căn giữa tất cả vector trong detector axis dài 543;
5. gọi inverse Radon với ramp filter;
6. lật dọc vì trục ảnh và trục Radon dùng chiều dương ngược nhau;
7. kéo tương phản theo percentile để lưu PNG dễ đọc.

## Cách giải tối thiểu

Từ thư mục gốc của event:

```powershell
python ".\Forensics\You Scanned WHAT_!_\solve\solve.py" `
  ".\Forensics\You Scanned WHAT_!_\files\scan.7z" `
  ".\Forensics\You Scanned WHAT_!_\solve\evidence\reconstruction.png"
```

Solver tự giải nén vào temporary directory, mở SQLite read-only, dựng ảnh và tự
xóa bản SQLite tạm. Ảnh kết quả là
[`solve/evidence/reconstruction.png`](../solve/evidence/reconstruction.png).

Trong ảnh, chuỗi nằm phía trên nhân vật. Ký tự giữa `C` và `m` là số `0`; đoạn
`13T3` là leetspeak cho `leTe`. Hai dấu `!!` được vẽ sau dấu `}` nên không thuộc
flag.

## Xác minh flag

Xác minh không dựa trên hình đoán một lần:

1. replay solver từ `scan.7z` vào một file tạm khác;
2. hash cả ảnh evidence và ảnh replay;
3. hai file cùng SHA-256
   `aabee2bc31d0fca483346ed663ce37e9ecfd2d8b2fff8fc7cabd7bfd9cf2fdba`;
4. đọc lại chuỗi đầy đủ từ ảnh đã chuẩn hóa orientation và kiểm tra dấu `}`.

Không submit lên scoreboard theo phạm vi hoạt động offline của bài học.

## Nhánh không dùng và lỗi thường gặp

- **Mở như DICOM:** tên đề là gợi ý chủ đề, không phải định dạng. Archive listing
  cho bằng chứng trực tiếp rằng payload là SQLite.
- **Ghép các JSON array như ảnh thường:** độ dài detector thay đổi theo góc nên sẽ
  tạo ma trận răng cưa, không phải ảnh không gian.
- **Pad nhưng dùng nguyên giá trị trung bình:** hình có thể lờ mờ hoặc méo cường
  độ vì projection đúng phải là tổng dọc tia.
- **Đọc flag trước khi sửa orientation:** rất dễ nhầm chữ phản chiếu, `0/O` hoặc
  đưa hai dấu chấm than ngoài ngoặc vào flag.
- **Dùng `circle=True`:** dữ liệu bắt nguồn từ ảnh chữ nhật/canvas mở rộng; giả định
  mọi pixel ngoài đường tròn bằng 0 không phù hợp bằng `circle=False`.

## Bài học và đường nhanh cho lần sau

Khi gặp dữ liệu CT/projection tự chế:

1. kiểm tra container, schema, số góc và độ dài detector;
2. xác định giá trị là tổng hay trung bình;
3. chuẩn hóa projection về cùng detector axis bằng centered padding;
4. thử filtered backprojection trước các kỹ thuật tối ưu phức tạp;
5. sửa orientation và xác minh từng ký tự trên output tái lập.

HexStrike không được dùng: mọi artefact đều cục bộ, SQLite và scikit-image đã đủ,
nên chuyển file sang Kali không đem lại lợi ích.

## Nguồn tham khảo

- [scikit-image: Radon transform](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html) — giải thích projection/sinogram và filtered backprojection.
- [scikit-image API: `iradon`](https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.iradon) — tham số `theta`, filter, interpolation và `circle` dùng trong solver.
- [SQLite URI filenames](https://www.sqlite.org/uri.html) — cơ chế `mode=ro` để mở database ở chế độ chỉ đọc.
