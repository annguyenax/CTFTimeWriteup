# space radiation - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Đề bài cho biết có một bức điện từ không gian bị bức xạ (radiation) làm sai lệch dữ liệu. Chuỗi dữ liệu gồm các block 16-bit (4 ký tự hex): 84ea cc57 4906.... Cần phục hồi thông điệp ban đầu.

## 2. Kiến thức nền tảng
- **Hamming Code**: Một mã sửa lỗi (Error-Correcting Code) phổ biến.
- Dấu hiệu: Bức xạ (radiation) ám chỉ lỗi lật bit (bit-flip). Block 16-bit gợi ý đến mã **Extended Hamming(16, 11)**, trong đó 11 bit là dữ liệu, 4 bit parity và 1 bit parity tổng.

## 3. Quá trình phân tích & Giải
- Đổi các khối hex thành chuỗi nhị phân 16-bit.
- Khi đếm số bit 1 trong mỗi khối 16-bit, tất cả đều là số lẻ (lệch so với Even Parity chuẩn). Điều này chứng minh mỗi khối đã bị lật đúng 1 bit do bức xạ.
- Cấu trúc Hamming(15, 11) quy định các bit ở vị trí lũy thừa của 2 (1, 2, 4, 8) là parity bit. Tính toán *syndrome* từ các bit nhận được sẽ cho ra vị trí chính xác của bit bị lật.
- Viết script Python để tính syndrome, lật lại bit lỗi, và trích xuất 11 bit dữ liệu từ mỗi khối.
- Ghép toàn bộ các bit dữ liệu thu được và giải mã ASCII, ta lấy được Flag nguyên vẹn.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- Lưu solve.py thực hiện toàn bộ quá trình parse hex, correct bit flip và xuất ASCII.

## 5. Xác minh Flag
- Flag: LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}

## 6. Bài học rút ra
Khi gặp dữ liệu bị sai lệch bit có quy luật block cố định, Hamming Code là thuật toán hàng đầu nên nghĩ tới. Khả năng tự sửa lỗi (Forward Error Correction) của nó rất mạnh và phổ biến trong truyền thông vệ tinh.
