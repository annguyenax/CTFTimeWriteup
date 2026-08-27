# Lock Out

## 1. Summary / Flag
- Status: `[x] solved`
- Flag: `KaliTeam{e10f1a45-2433-48a6-84e4-713c35474b9a}`
- Flag: `KaliTeam{138ef4d5-49a4-41ed-a6d0-5c38f1dc4f7d}`

## 2. Challenge files / versions
- Files: (no attachments — prompt-only / live instance)
- Environment: Apache/2.4.38 (Debian) with PHP/7.2.34

## 3. Core concept
- **Challenge Name:** Lock Out
- **Category:** Web
- **Points:** 100
- **Solves:** 34
- **Instance:** http://0602.chall.kali-team.online:8001/

## Solution

The web application contains two main pages: `login.php` and `admin.php`. When navigating to the root, we are presented with a login page.

Looking at the `/admin.php` page via a standard browser redirects us back to `login.php` since we are not authenticated. However, when intercepting the HTTP request using `curl`, we observe that the server returns a `302 Found` redirect but still includes the full HTML content of the admin page in the response body. This is a classic "Execution After Redirect" (EAR) vulnerability.

In the leaked admin page HTML, there is a hint:
```html
<!-- <a href="?PrintFlag=Execute: Get_Flag.sh">Click here</a> to get the flag! -->
```

By crafting a request directly to `admin.php?PrintFlag=Execute:+Get_Flag.sh` and ignoring the redirect, the server executes the command and returns the flag within the response body.

## Flag
`KaliTeam{138ef4d5-49a4-41ed-a6d0-5c38f1dc4f7d}`dmin.php?PrintFlag=Execute:+Get_Flag.sh"
  `
- Kết quả nhận được mã HTML chứa thẻ flag.

## 6. Verification
- Chạy script solve.py để tự động gửi request  llow_redirects=False và trích xuất KaliTeam{...}.

## 7. Failed approaches
- Thử các loại SQL Injection cơ bản (ví dụ ' OR 1=1--) ở form đăng nhập nhưng không thành công do bản chất lỗ hổng không nằm ở câu truy vấn CSDL.

## 8. Alternative solve paths
- Sử dụng Burp Suite để truy cập dmin.php, chặn (Intercept) phản hồi từ server, xoá dòng Location: login.php và đổi HTTP/1.1 302 Found thành HTTP/1.1 200 OK để xem trực tiếp trang trên trình duyệt, sau đó ấn nút Get Flag.

## 9. Faster route next time
- Khi thấy có form/trang nào yêu cầu đăng nhập, luôn luôn xem xét trực tiếp source HTML của request bị block/redirect bằng các công cụ không tự động chuyển hướng như curl hoặc Burp Suite.

## 10. Sources
- [CWE-698: Execution After Redirect (EAR)](https://cwe.mitre.org/data/definitions/698.html)
