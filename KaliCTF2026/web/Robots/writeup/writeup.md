# Robots

## 1. Summary / Flag
- Status: `[x] solved`
- Flag: `KaliTeam{8db841c9-b44d-4e5c-ae71-4b7ba838822f}`

## 2. Challenge files / versions
- Files: (no attachments — prompt-only / live instance)
- Environment: Apache/2.4.25 (Debian) with PHP/7.0.33

## 3. Core concept
- Thay đổi User-Agent HTTP header để giả mạo bot của các công cụ tìm kiếm (ví dụ: Googlebot) nhằm lấy nội dung ẩn từ file obots.txt.

## 4. Triage
- Đề bài gợi ý về "robots" và "Silicon Intelligence". 
- Khi truy cập obots.txt bằng trình duyệt thông thường, trang web trả về nội dung chê bai "Human" và nhắc đến "GOOGLEBOTS".
- Phân tích HTTP response thấy obots.txt được xử lý bởi PHP (X-Powered-By: PHP/7.0.33), chứng tỏ nội dung của nó có thể thay đổi động dựa vào request.

## 5. Exploit/recovery
- Sử dụng curl gửi request đến /robots.txt với header User-Agent: Googlebot:
  `ash
  curl -s -A "Googlebot" http://f1a4.chall.kali-team.online:8001/robots.txt
  `
- Server nhận diện request đến từ Googlebot và trả về nội dung chứa flag.

## 6. Verification
- Chạy script solve.py hoặc dùng lệnh curl in ra đúng định dạng flag KaliTeam{...}.

## 7. Failed approaches
- Kiểm tra các file thông thường khác như /humans.txt hay /sitemap.xml đều trả về 404.

## 8. Alternative solve paths
- Dùng Burp Suite, Intercept request tới /robots.txt và sửa trường User-Agent thành Googlebot, sau đó Forward.

## 9. Faster route next time
- Khi thấy có thông báo nhắc tới một công cụ/bot cụ thể trong obots.txt, lập tức thử giả mạo User-Agent thành bot đó.

## 10. Sources
- Kiến thức cơ bản về HTTP headers và User-Agent spoofing.
