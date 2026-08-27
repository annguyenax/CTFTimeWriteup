# read the rules - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Cho một file GIF (grid.gif) là mô phỏng của một cellular automaton 2D và một file danh sách hoán vị permutation.txt. Tìm thông điệp bí mật được ẩn giấu trong luật của CA này.

## 2. Kiến thức nền tảng
- Cellular Automaton: Với Moore neighborhood 8 ô (không tính bản thân), mỗi ô ở trạng thái t sẽ quyết định trạng thái ở t+1. Có 256 trạng thái hàng xóm, tương ứng với luật 256 bit.
- Image Processing: Cần phân tích kích thước của mỗi 'cell' trên grid ảnh GIF (ở đây là 6x6 pixel).

## 3. Quá trình phân tích & Giải
- Phân tích grid.gif để trích xuất mảng lưới ở từng frame. Kích thước thật của mỗi cell là 6x6 pixel, vì thế grid thực tế là 64x64 cell.
- Tính toán luật chuyển đổi: Duyệt qua các cell giữa frame 0 và 1, xây dựng lại bảng quy tắc 256 bits.
- Do không rõ quy ước thứ tự duyệt 8 ô hàng xóm (neighbor order), ta tiến hành vét cạn toàn bộ 8! = 40320 thứ tự.
- Với mỗi thứ tự, tính toán bảng quy tắc 256 bits. Sau đó áp dụng hoán vị từ permutation.txt vào 256 bits này để xáo trộn lại.
- Nếu chuỗi 256 bit sau hoán vị tạo thành các ký tự ASCII hợp lệ, ta sẽ thu được Flag.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- solve.py: Script tự động làm mọi việc từ đọc GIF, trích xuất luật, brute-force hoán vị neighbor và giải mã Flag.

## 5. Xác minh Flag
- Flag: LITCTF{th3_fl4g_1s_in_th3_ru1e5}

## 6. Bài học rút ra
Khi không chắc chắn về các hằng số quy ước (như thứ tự duyệt bit của neighborhood), brute-force không gian nhỏ (8!) là phương pháp hiệu quả nhất.
