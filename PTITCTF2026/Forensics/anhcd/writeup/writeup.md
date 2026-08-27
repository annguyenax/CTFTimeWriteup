# anhcd — Forensics (PTITCTF2026)

## Trạng thái

**needs_verification** — chưa có flag được xác minh. Hai chuỗi flag-shaped đều được
nhúng có chủ ý, nhưng khả năng đọc lại một chuỗi không chứng minh scoreboard chấp nhận nó.

1. PNG RGB-LSB, có độ dài 32-bit big-endian bằng 52:
   PTITCTF{hihihi_th15_15_your_riel_fl4g_...._i_guess?}
2. Phổ log-magnitude FFT 2D:
   PTITCTF{FFT_15_fun_bu7_700_3a5y_i_gu355}

Chuỗi đầu tự nhận là trò đánh lạc hướng. Chuỗi FFT đọc được rõ và tái lập được,
nhưng nội dung “FFT is fun but too easy, I guess” có thể tiếp tục là decoy. Không
có phản hồi scoreboard nên hồ sơ này không gọi chuỗi FFT là flag thật.

## Tệp và tính toàn vẹn

- Forensics - anhcd.7z: 87,716 byte; chỉ chứa hai ảnh, không mã hóa.
- anhcd.png: 200x200 RGB; SHA-256
  044bf345ef2a70772244f0cb3bed3931fba662cd7f6c6414e12c96e7f98e50f5.
- anhcd_better.jpg: 200x200 JFIF; SHA-256
  9832b7b2d5a14050d3baa5d58fbb797ad03c0ad9fd79ca07bc6a4678bf2857af.
- PNG chỉ có IHDR/IDAT/IEND; JPEG kết thúc đúng tại EOI. Không có EXIF,
  ancillary chunk hoặc dữ liệu nối đuôi.

## Hai đường giải tái lập được

Chạy từ thư mục solve:

    python solve.py

Solver đọc 32 bit đầu của RGB-LSB làm độ dài, rồi lấy đúng 52 byte payload. Nó
đồng thời tạo fft_flag.png bằng FFT 2D, log-magnitude và high-pass. Tính đối xứng
liên hợp của FFT ảnh thực làm chữ xuất hiện thành hai bản quay 180 độ; cả hai bản
cho cùng chuỗi.

## Ma trận kỹ thuật đã kiểm tra

- Container/metadata: 7z listing, PNG chunks, JPEG markers, EXIF, trailing data,
  strings và binwalk — không có object thứ ba.
- Pixel stego: zsteg toàn bộ bit-plane; RGB/BGR; đảo thứ tự; hàng/cột/đường
  chéo/chu vi; XOR, hiệu tuyệt đối và hiệu modulo giữa hai ảnh; lấy mẫu đều
  bước 2–32 — chỉ tìm lại LSB decoy.
- Miền biến đổi: FFT theo grayscale/từng kênh/ảnh hiệu; phase, real, imaginary,
  magnitude; DCT, DST, cepstrum, autocorrelation, Radon, Haar/db4 DWT và
  Walsh–Hadamard — chỉ FFT magnitude của PNG chứa chữ đã biết.
- JPEG stego: steghide với từ khóa và RockYou, vét toàn bộ 2^32 seed bằng
  stegseek, OutGuess, jsteg/stegdetect và F5 extractor. Không có payload hoàn
  chỉnh. Báo F5 của stegdetect là false positive vì JPEG sạch tái nén cũng cho
  cùng tín hiệu.
- OSINT/provenance: tìm challenge, chuỗi đặc trưng và hồ sơ công khai anhcd05;
  không thấy flag hoặc writeup công khai khớp artifact.

## Kết luận học thuật

Các kiểm tra âm không thể chứng minh tuyệt đối rằng không tồn tại một thuật toán
stego tùy biến có khóa. Chúng chỉ loại các họ kỹ thuật có tín hiệu quan sát được.
Với artifact hiện tại, mô hình đơn giản nhất là hai lớp chủ ý: LSB decoy và FFT
candidate; chưa có bằng chứng thực nghiệm cho lớp thứ ba. Bước có giá trị thông
tin cao nhất là nộp **đúng chuỗi không có dấu gạch chéo trước dấu gạch dưới** và
lưu phản hồi scoreboard. Nếu bị từ chối, cần thêm hint hoặc nguồn xác nhận từ tác
giả thay vì brute-force tiếp không có mô hình.
