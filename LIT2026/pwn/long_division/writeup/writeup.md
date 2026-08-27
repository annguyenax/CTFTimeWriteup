# long_division - LIT CTF 2026 (Pwn)

## 1. Yêu cầu bài toán
Khai thác lỗ hổng trong tiện ích máy tính (calculator) tính phép chia hai số nguyên 32-bit có dấu.

## 2. Kiến thức nền tảng
- Integer Overflow: Phép chia số nguyên 32-bit có dấu (signed 32-bit integer) bị lỗi tràn bộ đệm số khi chia số âm nhỏ nhất (INT_MIN = -2147483648) cho -1, do kết quả dương 2147483648 vượt quá giới hạn biểu diễn của số nguyên 32-bit có dấu.

## 3. Quá trình phân tích & Giải
- Khi kết nối với 
c 136.115.87.65 31777, máy chủ yêu cầu nhập  và  để thực hiện phép tính  / b.
- Đã nhập  = -2147483648 và  = -1.
- Kết quả thu được: signed division overflow -> LITCTF{1nt_div1si0n_0v3rflow}.

## 4. Xác minh Flag
- Flag: LITCTF{1nt_div1si0n_0v3rflow}
