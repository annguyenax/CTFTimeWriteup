# one does not simply hide a flag - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Đề bài cho một file ảnh tên mordor_challenge.png. Nhiệm vụ là tìm cờ ẩn trong đó, sử dụng các kỹ thuật giấu tin (Steganography).

## 2. Kiến thức nền tảng
- **Phân tích Meta Data**: Dùng exiftool để đọc thông tin meta.
- **Phân tích cấu trúc PNG**: Tìm dữ liệu đính kèm sau thẻ IEND (phần rác đính kèm sau khi ảnh kết thúc).
- **Steganography LSB**: Phân tích bit ít quan trọng nhất (Least Significant Bit) trên các kênh màu.
- **Mã hóa Vigenère**: Giải mã chuỗi dựa trên một từ khóa (key).

## 3. Quá trình phân tích & Giải
- Sử dụng exiftool mordor_challenge.png để lấy thông tin meta, ta phát hiện:
  - Một câu đố: "This thing all things devours... -- Bilbo". Đáp án là **time**.
  - Một cảnh báo: [minor] Trailer data after PNG IEND chunk.
- Bóc tách phần dữ liệu sau IEND, phát hiện đó là một file ZIP bị mã hóa.
- Giải nén ZIP bằng mật khẩu là đáp án câu đố (	ime), thu được file shire.png.
- Phân tích LSB của file shire.png (sử dụng bit 0 làm 1, bit 1 làm 0 và đọc theo thứ tự hàng) ta thu được một thông điệp ẩn thứ hai:
  - Riddle 2: "Voiceless it cries, wingless flutters, toothless bites, mouthless mutters. -- Gollum". Đáp án là **wind**.
  - Cipher: CIPHER: HQGFPN{elzlyho_eedlxrg_ev_cltmyv_wvq_yazfh}
- Dùng mã hóa Vigenère với khóa là chữ WIND để giải mã CIPHER, ta thu được Flag hoàn chỉnh.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- Lưu solve.py tổng hợp các bước tự động.

## 5. Xác minh Flag
- Flag: LITCTF{riddles_wrapped_in_pixels_and_verse}

## 6. Bài học rút ra
Việc kết hợp nhiều lớp giấu tin (metadata, file zip appending, steganography LSB nghịch đảo và mã hóa cổ điển) làm tăng độ khó của bài. Không nên dừng lại khi chỉ tìm thấy một manh mối nhỏ.
