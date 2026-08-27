# Pablo Escobar

- **Event:** PTITCTF2026
- **Category / tags:** Reverse / hybrid (Go PE crypto + web gallery + OSINT)
- **Flag format:** `PTITCTF{...}`
- **Attachments / service:** `files/dist.zip` → `Tool.exe` + `config.enc`; remote `http://144.79.188.36:6500/`
- **Status:** partial — reverse + inbox recovered; flag **not verified**
- **Resume:** `notes/SESSION.md`

## Prompt (verbatim)

```text
Ông trùm buôn ma túy ở Bắc Ninh cung cấp cho đồng bọn một phần mềm. Trước mỗi cuộc giao dịch, ông chủ đều gửi ảnh thông qua cho đồng bọn. Đồng bọn nhận ảnh nơi giao ma túy, rồi cho flycam bay tới giao hàng. Công an PC04 đã tóm gọn một đối tượng thu được 1 ít thông tin tài khoản như sau:
TK: luongvd
MK: luongvd
Bên trong vẫn còn chứa ảnh địa điểm cuối cùng mà đối tượng nhận được.
```

## Recon

- `Tool.exe`: PE64 Go, `github.com/jchv/go-webview2` / configurable-webview. Loads decrypted URL in WebView2.
- `config.enc`: JSON envelope `pbkdf2-sha256` / 210000 / AES-256-GCM (salt + nonce + ciphertext, all b64).
- Password is not a string in `.rdata`. `configkey.Key` builds 44 bytes from two XOR tables + linear `73*i+0x5D`.

## Reverse (done, reproducible)

1. Locate `configkey.Key` @ `0x140103660`.
2. Tables: t1 `0x140297CC0`, t2 `0x140297C80`, loop `0x2C` bytes.
3. `out[i] = ((73*i + 0x5D) ^ (t1[i] ^ t2[i])) & 0xFF`
4. Password: `RqriV3LFYnQcOwZoTc5UQJLP59wyhg99VATMAqrIhlo=`
5. `pbkdf2_hmac(sha256, password, salt, 210000, dklen=32)` → AES-GCM open.

Decrypted config:

```json
{
  "url": "http://144.79.188.36:6500/",
  "title": "WebView Tool",
  "width": 1280,
  "height": 800,
  "debug": false
}
```

Solver: `solve/decrypt_config.py`.

## Web (done for user role)

```text
POST /api/session  {"username":"luongvd","password":"luongvd"}
→ {"user":{"username":"luongvd","role":"user"}}
Cookie: anhhop_session=<64 hex>
GET  /api/images
GET  /api/images/:id
POST /api/images   (admin only; 403 for user)
```

Frontend (`ImagePortal-*.js`): brand `Pablo_Escobar`; admin can **Gửi cho luongvd** or **Chỉ lưu vào kho**.

Inbox 2026-08-22 (see `notes/inbox/`):

| id | message | what |
|---|---|---|
| 1 | Chuẩn bị có đơn hàng lớn nha em, nghe nói công an | Pexels 38512126 aerial **Ikoyi, Lagos, Nigeria** (byte-identical to stock) |
| 2 | Ở xưởng có cái toilet hài vl | toilet-paper frog meme |
| 3 | (admin saved) | **403** `Không có quyền xem ảnh.` |
| 4 | Chạy đến đâu rồi em. | last `createdAt`; VN police inspecting a factory (pot, forklift, blue drum) |

## Flag gap

Prompt says the last received **location photo** is still inside. Chronologically that is **id 4**. Id 3 is the only object not visible to `luongvd`.

Candidate flags are **not** written here. Need either:

- pixel-matched news source for `notes/inbox/4.jpg`, or
- admin access to `/api/images/3`, then scoreboard accept.

## Dead ends

- Reverse-image id 4 (Yandex/Bing/Google + catbox URL): no exact match.
- Visual compare vs Mẫn Xá/Văn Môn inspection (Danviet 2024-11-08), Franking Việt Nam (Trung Đồng, Nếnh), Nha Trang ketamine raid, Hưng Yên fake cooking-oil case: **not the same frame**.
- Stego on inbox JPEGs: no trailing data, id4 has no EXIF, no `PTITCTF` in LSB/strings.
- Admin login guesses (anhhop, Pablo_Escobar, admin, recovered config key, … ~377 pairs): 401.
- Next middleware / `X-Original-URL` / role header / mass-assignment `role=admin` / NoSQL `$ne`: no id3.
- Image IDs: only 1–4 exist (0 and ≥5 → 404).

## Solver

```powershell
cd "D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Pablo Escobar\solve"
python decrypt_config.py --exe ..\..\..\..\ctf-scratch\ptitctf2026_pablo_escobar\Tool.exe --enc ..\..\..\..\ctf-scratch\ptitctf2026_pablo_escobar\config.enc
python fetch_inbox.py --out ..\notes\inbox_live
```

## Flag

```text
(not recovered — do not invent PTITCTF{...})
```

## What to reuse next time

- Go configurable-webview: encrypted JSON envelope next to the PE; recover obfuscated PBKDF2 password from `configkey.Key` XOR tables, then AES-GCM.
- Vinext/Next photo vault: user inbox vs admin “save-only” id; last `createdAt` + prompt “địa điểm cuối” = OSINT, not another crypto layer.
