# Phreaky

## 1. Tổng quan

**Phreaky** là challenge forensics (HackTheBox, mức độ medium) đi kèm một file `phreaky.pcap` (7.2 MB). Câu chuyện: có một "con chuột chũi" (mole) trong tổ chức Phreaks đang gửi các **khóa** (keys) cho phe Talents qua email, và nhiệm vụ của chúng ta là theo dõi đường truyền mạng để lần ra bí mật bị phản bội. Đây là dạng bài kinh điển: **phân tích PCAP + trích xuất email SMTP + phá mã ZIP có mật khẩu + ráp file PDF**, cờ nằm trong tài liệu được gửi ra ngoài.

## 2. Triage

- `forensics_phreaky.zip` (683 B) chứa 1 entry `phreaky.pcap` nhưng **bị mã hóa bằng mật khẩu**; `Expand-Archive` thất bại, `python zipfile` báo "encrypted, password required". Thử dò mật khẩu thông dụng → trúng ngay `hackthebox`.
- Chạy `strings` trên pcap: thấy chuỗi SMTP rất rõ ràng —
  `MAIL FROM:<caleb@thephreaks.com>`, `RCPT TO:<resources@thetalents.com>`, Subject "Secure File Transfer", body chứa `Attached is a part of the file. Password: S3W8yzixNoL8`, kèm attachment `application/zip`. → **giả thuyết chính**: nhiều email, mỗi email gửi 1 mật khẩu + 1 phần ZIP bị khóa; cần gom đủ các phần rồi ráp lại.

## 3. Phân tích

- Viết bộ parser PCAP thuần Python (không cần scapy/tshark): đọc header pcap, tách từng packet Ethernet/IPv4/TCP, ghép lại luồng TCP theo cặp (src,dst,port).
- Tìm thấy 64 kết nối TCP, trong đó các kết nối tới **cổng 25 (SMTP)**; trích phần `DATA` giữa `DATA\r\n` và `\r\n.\r\n` → thu được **15 email**.
- Mỗi email (lưu thành `email_NN.eml`) có:
  - body text/plain: `Attached is a part of the file. Password: <mật khẩu 12 ký tự>`
  - 1 attachment `application/zip` (base64 trong MIME) → lưu thành `part_NN.zip`.
- Mỗi `part_NN.zip` chứa đúng 1 file tên `phreaks_plan.pdf.partN` (221 B, phần cuối 208 B). Giải nén từng cái bằng đúng mật khẩu trong email tương ứng (email N ↔ part N ↔ mật khẩu N).
- Nối tuần tự `part1..part15` → `reassembled.bin` (3302 B) có magic `%PDF-1.3` và kết thúc bằng `%%EOF` → **file PDF hợp lệ** tên `phreaks_plan.pdf` ("Operation Spotlight: The Phreaks' Grand Scheme Against The Talents").

## 4. Exploit

Các bước khai thác (tự động hóa trong `solve/solve.py`):

1. Giải nén `forensics_phreaky.zip` bằng mật khẩu `hackthebox`.
2. Parse PCAP → tái tạo luồng TCP cổng 25 → cắt 15 email raw.
3. `email.message_from_bytes` để lấy mật khẩu (regex `Password:\s*(\S+)`) và giải mã base64 attachment ZIP.
4. `zipfile.ZipFile.read(name, pwd=...)` để lấy từng `phreaks_plan.pdf.partN`.
5. Nối `part1..part15` theo thứ tự → PDF.
6. Tìm các `stream` thật trong PDF (lưu ý tránh nhầm `endstream` vì chứa chuỗi "stream"), giải nén FlateDecode bằng `zlib` → nội dung trang 2 có dòng:

```
Key for secure communication: HTB{Th3Phr3aksReadyT0Att4ck}.
```

## 5. Flag

```
HTB{Th3Phr3aksReadyT0Att4ck}
```

**Xác minh độc lập:** cờ xuất hiện đúng 1 lần trong nội dung stream trang 2 của PDF; quy trình trích xuất chạy lại được từ đầu (pcap → 15 email → 15 zip → 15 part → PDF hợp lệ `%PDF-1.3...%%EOF` → giải nén stream), đúng định dạng `HTB{...}`.

## 6. Bài học

- **PCAP không cần tool nặng**: chỉ cần hiểu cấu trúc Ethernet/IP/TCP là viết được parser; `strings` là test phân biệt rẻ nhất để định hướng (thấy SMTP/MIME ngay).
- **Mật khẩu ZIP của challenge** thường nằm ở mô tả hoặc là mật khẩu chung dễ đoán (`hackthebox`) — thử bộ từ thông dụng trước khi đưa vào bẻ khóa.
- **Kỹ thuật exfil theo kiểu "chia nhỏ + mã hóa"**: kẻ tấn công gửi nhiều phần file qua nhiều email, mỗi phần một mật khẩu riêng — dấu vết nằm chính trong email (mật khẩu đi kèm attachment!).
- Khi giải nén stream PDF, cẩn thận chuỗi `endstream` cũng chứa literal `stream` — phải kiểm tra byte phía trước để tránh bắt nhầm offset.
- Dữ liệu "sạch" cần được bảo quản dạng nhị phân nguyên vẹn (email → zip → part → PDF) trước khi chuyển đổi, để đảm bảo tái lập được kết quả.
