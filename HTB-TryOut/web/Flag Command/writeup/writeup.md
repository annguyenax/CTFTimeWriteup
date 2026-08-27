# Flag Command — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (very easy), không có file đính kèm.
Target: `http://154.57.164.82:32021`
Mục tiêu: lấy flag `HTB{...}` từ game terminal "Dimensional Escape Quest".

## 2. Kiến thức nền
- **Hidden/undocumented API**: frontend JS thường tải toàn bộ state (kể cả lệnh bí mật) từ JSON rồi chỉ ẩn trên UI.
- Client-side check không phải hàng rào bảo mật: nếu API chấp nhận lệnh `secret`, gọi trực tiếp bằng HTTP là đủ.
- Header `Server: Werkzeug/3.0.1 Python/3.11.8` → Flask.

## 3. Phân tích
- JS `main.js`: `fetch('/api/options')` gán `availableOptions = res.allPossibleCommands`.
- Lệnh được chấp nhận nếu thuộc `availableOptions[currentStep]` **hoặc** `availableOptions['secret']`.
- POST `/api/monitor` body `{"command": "..."}`; nếu `data.message` chứa `HTB{` thì coi như thắng.
- `commands.js` / help chỉ liệt kê `start/clear/audio/restart/info` — không nhắc secret.

## 4. Vì sao hướng này
- Không có source; recon rẻ nhất là đọc JS + gọi API đã lộ.
- H2 (chơi game tới thắng) tốn thời gian và không cần vì secret shortcut đã có.
- H3 (CMDi trên command) không có tín hiệu: command chỉ là token trong whitelist JSON.

## 5. Các bước
1. TRIAGE: GET `/` → 200, script `/static/terminal/js/{commands,main,game}.js`.
2. Đọc `main.js` → phát hiện `/api/options` và `/api/monitor`.
3. GET `/api/options` → `allPossibleCommands.secret` =
   `Blip-blop, in a pickle with a hiccup! Shmiggity-shmack`
4. POST `/api/monitor` `{"command":"<secret>"}` → JSON chứa flag.
5. Replay độc lập → cùng flag.

```text
python solve/solve.py --target http://154.57.164.82:32021
```

## 6. Flag
```
HTB{D3v3l0p3r_t00l5_4r3_b35t_wh4t_y0u_Th1nk??!_849b56a26793e9181ffd1cc6ebe163f3}
```
