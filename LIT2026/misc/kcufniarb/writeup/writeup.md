# kcufniarb - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Đề bài cho một chuỗi các ký tự giống ngôn ngữ Brainfuck nhưng không thể chạy được trực tiếp:
----------]<-----<-----------<--------<------->>>>+[<<<++++,+++,-----------,<+++,>,<---,>>-------------,+++++++,+++++++++++,++++++++++,-----,-----,+++++,+++++,-------------------,---,++++++,----------,<-----------,>>,-,-,<+++++++,++++++++,-------------,<--,---,-----------,>>,<<++++++,>>+,<------,

## 2. Kiến thức nền tảng
- Ngôn ngữ esolang **Brainfuck** (chỉ dùng các ký tự + - < > [ ] . ,).
- Tư duy dịch ngược (Reverse thinking): Tên bài kcufniarb chính là chữ rainfuck viết ngược.

## 3. Quá trình phân tích & Giải
- Phân tích đoạn code, ta nhận thấy dấu đóng ngoặc ] xuất hiện trước dấu mở ngoặc [, và thay vì dùng . (output) nó lại dùng , (input).
- Rõ ràng toàn bộ lệnh Brainfuck đã bị đảo ngược 100% (cả thứ tự chuỗi và bản thân các toán tử).
- Ta viết script hoán đổi lại: + thành -, < thành >, , thành ., [ thành ], và ngược lại.
- Kết quả nhận được là một đoạn Brainfuck hợp lệ: ++++++++++[>+++++...
- Chạy đoạn Brainfuck chuẩn này qua một trình thông dịch (interpreter) đơn giản tự viết bằng Python, ta nhận được flag.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- Lưu solve.py thực hiện convert và chạy code Brainfuck.
  `ash
  python solve.py
  `

## 5. Xác minh Flag
- Flag: LITCTF{ti_did_ruoy_234rjwado4i3}

## 6. Bài học rút ra
Khi gặp dữ liệu vô lý ở một định dạng quen thuộc (như Brainfuck bị ngược bracket), việc chú ý đến tên bài (kcufniarb) là chìa khóa để nhận ra thuật toán "đảo ngược toàn bộ các lệnh".
