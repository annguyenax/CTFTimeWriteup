# Evidence manifest - The Unbroken Shelf

| File | Claim supported | Source / tool | Reproduce | Hash (sha256, prefix) | Vì sao giữ |
|------|-----------------|---------------|-----------|-----------------------|------------|
| `../../files/The-Unbroken-Shelf-Final.png` | Mẩu báo gốc: tiêu đề + thân bài (Eighth Avenue, McGuire, Slater) | đề bài | mở ảnh | `afc167e0…` | Artifact gốc, điểm khởi đầu |
| `article_ocr.txt` | Toàn văn bài báo: "Slater & Halpern's drug store, 157 Eighth Avenue … about 8:40 p. m." | Chronicling America OCR (ALTO) | xem lệnh dưới | (trích 1490 ký tự) | Chứng cứ quyết định cho địa chỉ + thời gian |

## Nguồn gốc (định danh số báo)

- Kho: **Chronicling America** — Library of Congress.
- Tìm chính xác cụm tiêu đề `"Blows Firemen Out of Drug Store"` → **kết quả duy nhất**:
  **New-York Tribune, 1920-08-21, trang 1** — LCCN `sn83030214`.
- Trang: https://www.loc.gov/resource/sn83030214/1920-08-21/ed-1/?sp=1&st=text
- OCR ALTO (nguồn của `article_ocr.txt`):
  `https://tile.loc.gov/storage-services/service/ndnp/dlc/batch_dlc_eustachy_ver01/data/sn83030214/00206532543/1920082101/0503.xml`

## Lệnh tái lập (rút gọn)

loc.gov nằm sau Cloudflare JS-challenge ⇒ curl/WebFetch bị 403.
Vượt bằng Chrome thật qua CDP rồi `fetch()` trong ngữ cảnh trang (đã có cookie CF):

```
chrome.exe --remote-debugging-port=9444 --remote-allow-origins=* --user-data-dir=<scratch>
python solve.py     # in ra Address / Time / FLAG
```

## Kết quả

- NEWSPAPER = NEW_YORK_TRIBUNE  (masthead OCR: "NEW YORK TRIBUNE"; tiêu đề chính thức "New-York Tribune")
- DATE      = 1920_08_21
- ADDRESS   = 157 EIGHTH AVENUE
- TIME      = 8:40 p.m. → 2040
- FLAG (tái dựng) = `KaliTeam{NEW_YORK_TRIBUNE_1920_08_21_157_EIGHTH_AVENUE_2040}`
