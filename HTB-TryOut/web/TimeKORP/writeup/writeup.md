# TimeKORP — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (very easy), có source `web_timecorp.zip`.
Target: `http://154.57.164.82:30695`
Mục tiêu: đọc file `/flag` trên server, flag dạng `HTB{...}`.
Ứng dụng PHP hiển thị giờ/ngày qua tham số `?format=`.

## 2. Kiến thức nền
- **OS command injection**: khi input người dùng được nối vào chuỗi lệnh rồi chạy bằng `exec()` / `system()` mà không sanitize, kẻ tấn công thoát khỏi quoting và chèn lệnh mới (`'; cmd #`).
- PHP `exec($cmd)` chỉ trả về **dòng cuối** của stdout/stderr. File `/flag` không có newline nên cần payload để flag là (một phần của) dòng cuối.
- Lệnh gốc: `date '+FORMAT' 2>&1` — `FORMAT` nằm giữa hai dấu nháy đơn.

## 3. Phân tích
- `TimeController`: `$format = $_GET['format']` (mặc định `%H:%M:%S`), không filter.
- `TimeModel`: `"date '+" . $format . "' 2>&1"` rồi `exec()`.
- `Dockerfile` copy flag vào `/flag` (không nằm trong webroot `/www`).
- View in `$time` thẳng vào `<h1>It's <?= $time ?>.</h1>`.
- Handbook (`03_web_application_analysis.md`): `exec()` chạy shell, không trả raw stream — phù hợp đọc `/flag` qua CMDi.

## 4. Vì sao hướng này
- Input duy nhất là `format` và nó đi thẳng vào `exec` → command injection là vector rẻ nhất.
- Flag path đã biết từ Dockerfile → không cần RCE phức tạp hay brute-force.
- H2 (LFI/router) bị loại vì chỉ có route `GET /`. H3 (đọc `/flag` qua HTTP) bị loại vì file ngoài webroot.

## 5. Các bước
1. TRIAGE: GET `/` → 200, H1 `It's 13:26:10.` — service sống, output `date` phản hồi.
2. Payload thoát quote: `format=' ; cat /flag ; '`
   → `date '+' ; cat /flag ; '' 2>&1`
3. Response H1 chứa `HTB{...}` (kèm `sh: 1: : Permission denied` vì lệnh rỗng sau `;` và `/flag` không newline).
4. Verify độc lập: `format=' ; cat /flag #` (comment phần quote thừa) → cùng flag.

```text
python solve/solve.py --target http://154.57.164.82:30695
```

## 6. Flag
```
HTB{t1m3_f0r_th3_ult1m4t3_pwn4g3_489135c96ccbd58dbb8f42b8806e5911}
```
