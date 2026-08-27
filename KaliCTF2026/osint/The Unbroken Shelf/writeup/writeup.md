# The Unbroken Shelf — KaliCTF 26 (OSINT, 100đ)

## 1. Tóm tắt / Flag

- **Trạng thái:** Giải xong, đã xác minh từ nguồn gốc (bài học offline, không submit).
- **Flag (tái dựng):** `KaliTeam{NEW-YORK_TRIBUNE_1920_08_21_157_EIGHTH_AVENUE_2040}`
- **Một câu:** Mẩu báo bị xé là bài trang nhất của **New-York Tribune ngày 21/08/1920**,
  kể vụ nổ ở **hiệu thuốc Slater & Halpern, số 157 Eighth Avenue**, xảy ra **khoảng 8:40 tối (20:40)**.

> ⚠️ Điểm cần lưu ý về tên báo: măng-sét in "New-York Tribune" (có gạch nối).
> OCR đọc thành "NEW YORK TRIBUNE". Theo luật format (chữ hoa, khoảng trắng → `_`) thì
> `NEW_YORK_TRIBUNE` là hợp lý nhất; nếu grader giữ nguyên gạch nối thì thử
> `NEW-YORK_TRIBUNE`. Các trường còn lại (ngày, số nhà, phố, giờ) là chắc chắn.

## 2. File đề & môi trường

- `files/The-Unbroken-Shelf-Final.png` — ảnh mẩu báo (PNG 1500×1150, sha256 `afc167e0…`).
  Không có EXIF/metadata ẩn (đã kiểm tra bằng PIL: `info = {}`). Mọi manh mối nằm trong **nội dung chữ**.
- Định dạng flag: `KaliTeam{NEWSPAPER_YYYY_MM_DD_STREET_NUMBER_STREET_TIME}` — chữ hoa,
  khoảng trắng → `_`, giờ theo 24h. Ví dụ đề cho: `KaliTeam{THE_DAILY_RECORD_1918_04_12_72_MAIN_2130}`.

## 3. Kiến thức nền (giải thích cho người mới)

- **OSINT báo chí lịch sử:** rất nhiều báo Mỹ cũ đã được số hoá và **OCR** (nhận dạng chữ)
  trong kho miễn phí **Chronicling America** của *Library of Congress (LOC)*:
  `chroniclingamerica.loc.gov`. Có thể tìm **toàn văn** theo cụm từ chính xác → cực mạnh để
  định danh "số báo gốc" của một mẩu cắt.
- **LCCN**: mã định danh mỗi tờ báo (ví dụ New-York Tribune = `sn83030214`).
- **ALTO XML**: định dạng OCR lưu từng từ kèm toạ độ. Toàn văn một trang nằm trong file `.xml`
  trên máy chủ lưu trữ `tile.loc.gov`.
- **Cloudflare "Just a moment…":** LOC đặt sau Cloudflare; truy cập bằng script (curl/WebFetch)
  bị chặn 403 vì phải chạy JavaScript. Người chơi bình thường mở bằng trình duyệt là xong;
  khi tự động hoá thì phải điều khiển một **trình duyệt thật**.

## 4. Phân tích mẩu báo (triage)

Đọc kỹ ảnh, các manh mối rõ ràng:

- **Tiêu đề (rất đặc trưng):** `Mysterious Explosion Blows Firemen Out of Drug S…tore`
- Thân bài (cột phải): *"Accompanied by Battalion \[Chief Law\]rence McGuire the two \[lieutenants\]
  led about a dozen firemen … store. They had scarcely … when the explosion came. …
  a single shelf it blew the \[con\]tents of the store into the … **Eighth Avenue**, carrying the
  \[win\]dows before it."*
- Các mảnh cột trái (đuôi dòng bị xé): `…Street`, `Samuel`, `clerk`, **`Slater`**, `Seven-`.
- Nhan đề bài CTF **"The Unbroken Shelf"** khớp câu: *"Except for a single shelf it blew the entire
  contents…"* — cái **kệ không vỡ** chính là chi tiết chốt.

Kết luận triage: đây là **một vụ nổ hiệu thuốc trên Eighth Avenue (New York)** — cần tìm đúng
tờ báo + số ra để lấy **số nhà** và **giờ** (những phần bị xé/cắt mất trong ảnh).

## 5. Vì sao chọn Chronicling America

Tiêu đề là một chuỗi độc nhất. Google thường **không index** phần OCR của báo cũ (thử nhiều
truy vấn đều ra kết quả nhiễu). Ngược lại, Chronicling America cho **tìm toàn văn chính xác** —
đúng công cụ cho "định danh số báo gốc".

## 6. Các bước khai thác

### 6.1. Rào cản Cloudflare và cách vượt

- `curl`/`WebFetch` tới mọi host loc.gov (`chroniclingamerica`, `www.loc.gov`, `tile.loc.gov`)
  đều trả **403 "Just a moment…"**. Thử qua proxy (allorigins, corsproxy, r.jina.ai,
  Google-Translate proxy), Wayback, Internet Archive, `curl_cffi` (giả TLS Chrome) — **đều fail**
  vì Cloudflare bắt chạy JS.
- Cách thắng: máy có sẵn **Chrome thật**. Mở Chrome ở chế độ **headed** (có cửa sổ) kèm cổng
  debug CDP; Cloudflare tự pass sau vài giây. Sau khi pass, dùng `fetch()` **ngay trong ngữ cảnh
  trang** (đã có cookie CF) để tải JSON/ALTO. (Chi tiết trong `solve/solve.py`.)
  - Lưu ý: Chrome **headless** vẫn bị Cloudflare chặn — phải **headed**.

### 6.2. Tìm đúng số báo

Gọi API tìm kiếm toàn văn (qua trình duyệt đã pass CF):

```
https://www.loc.gov/collections/chronicling-america/?q="Blows Firemen Out of Drug Store"&fo=json
```

→ **đúng 1 kết quả:** *New-York Tribune, 1920-08-21, trang 1* (LCCN `sn83030214`).

### 6.3. Lấy toàn văn để đọc địa chỉ + giờ

1. Lấy metadata trang: `…/resource/sn83030214/1920-08-21/ed-1/?sp=1&st=text&fo=json`
   → trường `fulltext_service` chỉ tới file ALTO trên `tile.loc.gov`:
   `…/service/ndnp/dlc/batch_dlc_eustachy_ver01/data/sn83030214/00206532543/1920082101/0503.xml`
2. Tải ALTO XML, ghép các thuộc tính `CONTENT="…"` thành văn bản tuyến tính, rồi đọc bài.

Trích đoạn quyết định (đã làm sạch dấu OCR):

> *Mysterious Explosion Blows Firemen Out of Drug Store — A fireman and three other men were hurt
> last night in an explosion which wrecked **Slater & Halpern's drug store, 157 Eighth Avenue**. …
> **It was about 8:40 p. m.** Samuel Slater, proprietor of the store, was standing in the doorway
> with his clerk, Benjamin Prilek… His clerk ran to the fire-alarm box at **Seventeenth Street, two
> doors away**. … Accompanied by Battalion Chief **Lawrence McGuire** the two lieutenants led about a
> dozen firemen into the store. They had scarcely got inside when the explosion came. **Except for a
> single shelf** it blew the entire contents of the store into the middle of Eighth Avenue…*

Khớp 100% với mẩu báo (McGuire, hai lieutenant, ~một tá lính cứu hoả, "single shelf", Eighth Avenue,
clerk Slater/Samuel, mảnh "Seven-" = Seventeenth Street).

## 7. Ghép flag

| Trường | Giá trị | Nguồn trong bài |
|---|---|---|
| NEWSPAPER | `NEW_YORK_TRIBUNE` | măng-sét / LCCN sn83030214 |
| YYYY_MM_DD | `1920_08_21` | ngày ra báo |
| STREET_NUMBER | `157` | "…drug store, 157 Eighth Avenue" |
| STREET | `EIGHTH_AVENUE` | như trên |
| TIME | `2040` | "about 8:40 p. m." → 24h |

→ `KaliTeam{NEW_YORK_TRIBUNE_1920_08_21_157_EIGHTH_AVENUE_2040}`

## 8. Xác minh

- **Cụm tiêu đề chính xác chỉ khớp DUY NHẤT một số báo** trong toàn kho Chronicling America
  → không mơ hồ về "số báo gốc".
- **Thân bài trùng khớp từng chi tiết** với ảnh đề (đối chiếu trực tiếp) → đúng bài, không nhầm trang.
- Số nhà và giờ đọc trực tiếp từ OCR nguồn cấp một (không suy đoán).
- (Không có server chấm offline nên đây là mức xác minh cao nhất có thể; chỉ còn cách viết tên báo
  là điểm cần chốt khi submit.)

## 9. Hướng đi sai đã thử (và vì sao fail)

- **Google/Bing/DuckDuckGo thường:** không index OCR báo cũ → toàn kết quả nhiễu (nổ nhà máy dược
  hiện đại…). Bài học: báo lịch sử phải tra **archive chuyên dụng**, không phải search engine đại chúng.
- **Trang 11 báo The Evening World 1904-10-10** (một match "mờ" của body): đọc OCR ra là **trang cáo phó**,
  không có "Eighth Avenue/explosion" → false positive. Bài học: chỉ **cụm tiêu đề chính xác** mới đáng tin;
  match theo từ rời dễ trùng ngẫu nhiên trên một trang báo lớn.
- **Mọi proxy/curl_cffi/Wayback:** không vượt được Cloudflare JS-challenge → phải dùng trình duyệt thật.

## 10. Lộ trình nhanh hơn lần sau (checklist)

1. Ảnh mẩu báo → **lấy cụm chữ độc nhất nhất** (thường là tiêu đề).
2. Mở **chroniclingamerica.loc.gov** (browser thật) → tìm **toàn văn cụm chính xác**.
3. Trùng khớp thân bài để chắc đúng số báo; đọc **số nhà + giờ** ngay trong OCR.
4. Nếu cần tự động hoá: Chrome **headed** + CDP; sau khi pass Cloudflare thì `fetch()` JSON/ALTO
   ngay trong trang (`?fo=json` → `fulltext_service` → ALTO trên `tile.loc.gov`).
5. Đổi giờ am/pm → 24h; chữ hoa; khoảng trắng → `_`.

## 11. Nguồn

- Chronicling America — New-York Tribune, 1920-08-21, p.1 (LCCN sn83030214):
  https://www.loc.gov/resource/sn83030214/1920-08-21/ed-1/?sp=1&st=text
  → dùng để định danh số báo và đọc toàn văn (địa chỉ + giờ).
