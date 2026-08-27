# Pablo Escobar — SESSION (đọc file này khi làm tiếp)

- **Status:** PAUSED — reverse + login xong, **chưa có flag đã verify**. Không có `final_flag.txt`.
- **Flag format:** `PTITCTF{...}`
- **Ngày pause:** 2026-08-22
- **Scratch:** `D:\download\ctf-scratch\ptitctf2026_pablo_escobar\`
- **Bắt đầu lại:** đọc file này → mở `notes\evidence\` và `notes\inbox\` → chạy solver trong `solve\README.md`.

## Mục tiêu đề bài (verbatim)

Ông trùm buôn ma túy ở Bắc Ninh cung cấp cho đồng bọn một phần mềm. Trước mỗi cuộc giao dịch, ông chủ đều gửi ảnh thông qua cho đồng bọn. Đồng bọn nhận ảnh nơi giao ma túy, rồi cho flycam bay tới giao hàng. Công an PC04 đã tóm gọn một đối tượng thu được 1 ít thông tin tài khoản như sau:
TK: luongvd
MK: luongvd
Bên trong vẫn còn chứa ảnh địa điểm cuối cùng mà đối tượng nhận được.

## Đã xong (đừng làm lại)

1. `dist.zip` → `Tool.exe` (PE64 Go WebView2) + `config.enc`.
2. Khôi phục password `configkey.Key` từ binary, PBKDF2-SHA256 210000 + AES-256-GCM → URL portal.
3. Login `luongvd`/`luongvd`, dump hộp thư.

### Artifact hashes (SHA256)

```
66adf83ef86d8e76605063c7d01dc61fdd87cac446f34696a305b3a394c6aae7  Tool.exe  3023360
7b546c39e853fe2907c07d54ede5d5c08f183e9360953079ad6ff51f0f1bfb54  config.enc  470
257fec34a3b0ad32bc18a700fa898e379003bc739da884694eb781a0ca3daf54  dist.zip  1262685
ea2d63e77f755d5302539b9cd03273e9bea95d1b8646adb3aa14da94a03ea66a  img_1  1768998
b6479820f75efedaeac4fdf69467197d199e982a295a2fef624f31469a4956bc  img_2  119827
3c06e7c5b970f2246bf78f01875f0d4fa5eccdad455ad97b08860f913556ac97  img_4  35998
```

### Config decrypt

- Password (44 bytes): `RqriV3LFYnQcOwZoTc5UQJLP59wyhg99VATMAqrIhlo=`
- KDF: pbkdf2-sha256, iterations 210000, salt `91fS3SAVqIPnMb8UEB0GWA`, nonce `5Oql/E6+RenWpfIQ`
- Plaintext: `url = http://144.79.188.36:6500/` title `WebView Tool` 1280x800 debug false
- Solver: `solve\decrypt_config.py`

Key recovery (đừng đoán offset lại):

- `configkey.Key` @ VA `0x140103660`
- t1 @ `0x140297CC0`, t2 @ `0x140297C80`, length `0x2C`
- `out[i] = ((73*i + 0x5D) ^ (t1[i] ^ t2[i])) & 0xFF`

### Portal

- Cookie: `anhhop_session` (64 hex, server-side).
- Login POST `/api/session` JSON `{username,password}`.
- Gallery GET `/api/images`. Image GET `/api/images/:id`. Upload POST `/api/images` **admin only**.
- UI brand: `Pablo_Escobar`. Role `user` vs `admin`.
- Stack: Vinext/Next-like (`vinext.navigationRuntime`).

### Inbox (login 2026-08-22)

| id | name | size | createdAt UTC | message | file |
|---|---|---|---|---|---|
| 1 | pexels-taiwo-samson-1239982962-38512126.jpg | 1768998 | 01:52:39 | Chuẩn bị có đơn hàng lớn nha em, nghe nói công an | `notes/inbox/1.jpg` |
| 2 | 3.jpg | 119827 | 01:53:08 | Ở xưởng có cái toilet hài vl | `notes/inbox/2.jpg` |
| **3** | ? | ? | giữa 1 và 4 | admin “Chỉ lưu vào kho” — **403** `Không có quyền xem ảnh.` | chưa có |
| **4** | images.jpg | 35998 | **01:56:31 last** | Chạy đến đâu rồi em. | `notes/inbox/4.jpg` |

JSON gốc: `notes/evidence/inbox.json`.

## Flag đang kẹt ở đâu

Đề bài: *ảnh địa điểm cuối cùng mà đối tượng nhận được*.

**H1 (mạnh):** ảnh **id 4** là địa điểm — OSINT/reverse-image ra địa chỉ/tên xưởng → `PTITCTF{...}`.
**H2:** ảnh **id 3** (admin-only) mới là map/GPS/flag.
**H3 (yếu hơn):** ảnh 1 là đích flycam (Ikoyi, Lagos). Không phải ảnh cuối theo `createdAt`.

## Ảnh 4 — mô tả để reverse-image

JPEG JFIF, **không EXIF**, 547×365, 36 KB (thumbnail tin tức).

Cảnh: nhà xưởng tôn, đoàn công an + dân sự đeo khẩu trang KF94/N95 (khoảng 2020–2022). Nồi inox lớn bẩn trên xe đẩy, xe nâng phía sau, thùng phuy nhựa xanh nắp đỏ, tầng lửng 4 bồn inox + ống. Sĩ quan giữa không đeo khẩu trang, nhìn camera.

Public copy đã upload (có thể hết hạn): `https://files.catbox.moe/jy72x2.jpg`

Yandex/Bing/Google: **không có bản gốc**. OCR Yandex không đọc được chữ trên ảnh.

## Đã loại (đừng pixel-match lại trừ khi có ảnh mới)

| Ứng viên | Kết luận |
|---|---|
| CCN Mẫn Xá / Văn Môn / Yên Phong (Danviet 2024-11-08, Đại tá Phạm Văn Lương) | 2 ảnh báo **không khớp** (`danviet_manxa_2.jpg`, `danviet_manxa_4.jpg` trong scratch) |
| Franking Việt Nam, Trung Đồng, phường Nếnh (toilet/inox giả SUS 304) | `kho.jpg` + `cq.jpg` **không khớp**. Image 2 (meme toilet) chỉ là flavor, không phải bằng chứng pixel |
| Xưởng ketamin Nha Trang / C04 (Tuổi Trẻ 2025-03) | cảnh tương tự, **không cùng shot** |
| Dầu thực vật giả Hưng Yên / Nhật Minh Food (2025-06) | không khớp |
| Mỡ bẩn Hòa Long 2016 | quá sớm so với khẩu trang COVID |
| Stego LSB/EXIF/binwalk/trailing EOI trên 1/2/4 | không có `PTITCTF` |
| Login admin bounded (~377 cặp, gồm anhhop, Pablo_Escobar, key config) | toàn 401 |
| IDOR/header spoof/middleware Next/mass-assignment/NoSQL `$ne` | id 3 vẫn 403; username object/array → 500 rỗng, không leak |

## Việc tiếp theo (thứ tự)

1. Reverse-image **ảnh 4** bằng Google Lens / Yandex (upload file, không chỉ URL) + soi Facebook Công an Bắc Ninh / baobacninh / cand 2020–2022: nồi + xe nâng + thùng phuy xanh.
2. Nếu khớp pixel một bài báo → lấy **địa chỉ/tên cơ sở** làm candidate flag, verify trên scoreboard rồi mới ghi `final_flag.txt`.
3. Song song: tìm admin (không brute rộng). Gợi ý còn lại: username ẩn, password không phải common; cookie `anhhop_session` có thể là tên author chứ không phải user.
4. Ảnh 3: chỉ retry khi có primitive mới (leak tên file, session admin, bug mới). ID 0 và ≥5 = 404; chỉ tồn tại 1–4.
5. Ảnh 1 đã định vị: Pexels 38512126, tags **Ikoyi / Lagos Island / Nigeria**. Chỉ dùng nếu scoreboard/hint nói flycam chứ không phải “ảnh cuối”.

## Không làm

- Bịa `PTITCTF{...}` từ địa danh đoán (Mẫn Xá, Ikoyi, Trung Đồng, …).
- Brute login rộng / scan cổng ngoài scope.
- Ghi `final_flag.txt` trước khi verify.

## File liên quan

| Path | Nội dung |
|---|---|
| `writeup/writeup.md` | writeup đầy đủ, gồm dead ends |
| `solve/decrypt_config.py` | recover key + AES-GCM |
| `solve/fetch_inbox.py` | login + dump inbox |
| `notes/inbox/` | 3 JPEG user đã tải |
| `notes/evidence/` | hashes, config plaintext, inbox JSON |
| `D:\download\ctf-scratch\ptitctf2026_pablo_escobar\` | Tool.exe, JS, crop, ảnh báo so sánh |
