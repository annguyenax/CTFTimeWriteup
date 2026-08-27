# pw.zip - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Đề bài cung cấp một file zip bị khóa bằng mật khẩu (pw.zip). Mô tả gợi ý rằng mật khẩu nằm trong top 100 mật khẩu phổ biến nhất năm 2025. Mục tiêu là bẻ khóa file zip để đọc nội dung file cờ bên trong.

## 2. Kiến thức nền tảng
- **Password Cracking**: Kỹ thuật brute-force (thử sai) mật khẩu của các file nén bằng từ điển (wordlist).
- **Công cụ**: Các công cụ phổ biến như crackzip, zip2john (chuyển định dạng zip sang hash) và john (John the Ripper) dùng để thử hàng loạt mật khẩu.

## 3. Quá trình phân tích & Giải
- Sử dụng zip2john để trích xuất mã băm (hash) từ file zip: zip2john pw.zip > pw.hash
- Sử dụng công cụ john kết hợp từ điển ockyou.txt để crack mã băm: john --wordlist=/usr/share/wordlists/rockyou.txt pw.hash
- Rất nhanh chóng, john tìm ra mật khẩu là: 1234qwer.
- Giải nén file pw.zip với mật khẩu trên, thu được file lag.txt chứa cờ.

## 4. Bằng chứng (Evidence) & Lệnh tái lập
- Tool: HexStrike API (zip2john + john)
- Lệnh tối thiểu:
  `ash
  zip2john pw.zip > pw.hash
  john --wordlist=/usr/share/wordlists/rockyou.txt pw.hash
  7z x -p1234qwer pw.zip
  `

## 5. Xác minh Flag
- Flag: LITCTF{password_123456_103flkj3}

## 6. Bài học rút ra
- Không nên dùng các mật khẩu phổ biến hoặc dễ đoán. Ngay cả việc biến tấu một chút (như 1234qwer) vẫn nằm trong từ điển và bị bẻ khóa chỉ trong vài mili-giây.
