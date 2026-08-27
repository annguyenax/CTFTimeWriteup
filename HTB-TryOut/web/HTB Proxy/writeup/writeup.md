# HTB Proxy — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (medium), source `web_htb_proxy.zip`.
Target: `http://154.57.164.77:32208`
Mục tiêu: đọc `/flag<10 hex>.txt` (entrypoint đổi tên flag).
Custom HTTP proxy (Go :1337) + backend Node `ip-wrapper` (:5000).

## 2. Kiến thức nền
- **SSRF qua Host**: proxy `Dial("tcp", Host)` sau khi blacklist chuỗi `localhost/127./10./172./192.` trên **hostname**, không phải IP đã resolve.
- **HTTP parser confusion**: `strings.Split(req, "\r\n\r\n")` rồi chỉ validate `bodySplit[1]` với `Content-Length`. Phần `bodySplit[2+]` vẫn nằm trong `requestBytes` gửi backend.
- **Command injection**: `ip-wrapper` 1.1.1 `exec(\`ip address flush dev ${interface}\`)`. Không space → `${IFS}`; `;` nằm request 2 nên WAF body request 1 không thấy.
- Flag randomize: `mv /flag.txt /flag$(hex).txt` → glob `/flag*`.

## 3. Phân tích
- `/server-status` leak IP pod `10.244.40.122` (chứa `10.` → IP trần bị chặn).
- URL chứa `flushinterface` (case-insensitive) bị chặn; percent-encode Express **không** decode (`Cannot POST /flush%49nterface`).
- Backend `POST /flushInterface` + `POST /getAddresses`. `validateInput` cấm space.
- Buffer đọc client chỉ 1024 byte.

## 4. Vì sao hướng này
- H1 SSRF IP trần `10.244.40.122:5000` → kill (blacklist `10.`).
- H2 encode path `/flush%49nterface` → Express 404, kill.
- H3 domain `10-244-40-122.sslip.io` (không chứa `10.`) + smuggle request 2 `/flushInterface` → đúng cả Dial và parser.

## 5. Các bước
1. GET `/server-status` → IP `10.244.40.122`.
2. Host `10-244-40-122.sslip.io:5000` → Express 401 `/getAddresses` (SSRF OK).
3. Pipeline (body1 `{}` CL=2; sau `\r\n\r\n` là POST `/flushInterface`):
   ```
   {"interface":";cp${IFS}/flag*${IFS}/app/proxy/includes/index.html"}
   ```
4. GET `/` → nội dung flag (index.html bị ghi đè).
5. Replay GET `/` độc lập → cùng flag.

```text
python solve/solve.py --target http://154.57.164.77:32208
```

## 6. Flag
```
HTB{r3inv3nting_th3_wh331_c4n_cr34t3_h34dach35_edcec11fd46a9fe5e9820f74ebb11c6a}
```
