# Transcendent Renovation — Writeup (L3akCTF 2026, Beginner/forensics) — ⏳ 6/7

- **Trạng thái:** 6/7 câu đúng trên service; Q7 ("original name") chưa lấy được → flag chưa có (không bịa)
- **Điểm/Solves:** 108 / 59
- **File:** `files/TranscendentRenovation.zip` (pw `dead7852`) → `Administrator_JumpLists.zip` → AutomaticDestinations/ + CustomDestinations/
- **Service:** `ncat --ssl transcendent-renovation.instances.ctf.l3ak.team 1337` — "Ghost Hunt Terminal", hỏi 7 câu, đúng hết mới lộ flag.

---

## 1. Đề bài yêu cầu gì

Một folder lạ `NoNeedToWonder` xuất hiện. Dùng **Windows Jump Lists** để trả lời 7 câu về nguồn gốc của nó; trả lời đủ trên service SSL để nhận flag.

## 2. Kiến thức nền

- **Jump Lists:** Windows lưu MRU cho mỗi app ở `%AppData%\Microsoft\Windows\Recent\AutomaticDestinations\<AppID>.automaticDestinations-ms`. File này là **OLE Compound File** (còn gọi CDF V2 / CFBF).
- Bên trong: stream `DestList` (danh sách MRU + timestamp + hostname + droid) và các stream đánh số hex, mỗi stream là một **LNK (shell link)**.
- **DistributedLinkTracking (Droid):** mỗi LNK có `TrackerDataBlock` chứa `MachineID` (hostname) và các GUID `DroidVolumeId/DroidFileId` (ObjectID NTFS — **bền vững qua rename**).
- **\\tsclient\<share>:** ổ đĩa được **redirect qua RDP** từ máy client.

## 3. Phân tích & cách lấy từng đáp án

`f01b4d95cf55d32a` là AppID của **Windows Explorer** (taskbar). `grep` thấy `NoNeedToWonder` chỉ trong file này. Parse bằng `olefile`:

1. **Q1 – file format:** `file *.automaticDestinations-ms` → *"Composite Document File V2"* ⇒ **`OLE CF`** (server nhận `OLE CF`, không nhận `CDF V2`).
2. **Q2 – file:** `f01b4d95cf55d32a.automaticDestinations-ms`.
3. **Q4 – stream:** parse `DestList`; entry có path `...\Desktop\NoNeedToWonder` trỏ tới **stream 0x46 = `46`**.
4. **Q6 – hostname & Q5 – droid:** trong LNK stream 46, `TrackerDataBlock` (sig `0xA0000003`) cho `MachineID = logging-vm` và `DroidFileId = ec2ab952-7e4d-11f1-89ad-a2dead7852ad` (server muốn **lowercase, không ngoặc**).
5. **Q3 – share path:** file chứa `\\tsclient\HauntedHouse` (ổ RDP redirect) — nguồn của folder.

Solver: [solve/solve.py](../solve/solve.py) → in ra cả 6 đáp án. Chạy:
```bash
pip install olefile
python solve/solve.py <thư mục AutomaticDestinations>
```

## 4. Câu Q7 — "original name" (chưa giải)

**Cấu trúc rename data trong stream 46 (867 byte):**
- LNK hợp lệ (byte 0–490): `LinkTargetIDList` trỏ tới `NoNeedToWonder` (tên hiện tại).
- Phần đuôi (490–867): **remnant** của một LNK cũ hơn với tên `SoulSearch`. Khi Windows ghi đè stream bằng LNK mới ngắn hơn, OLE **không cắt** phần dư ⇒ đuôi giữ lại LNK cũ. Đây chính là "rename data" (Q4).

⇒ Về forensics, **original name = `SoulSearch`** (folder từng tên SoulSearch, đổi thành NoNeedToWonder). Tuy nhiên service **từ chối** `SoulSearch` và mọi biến thể (đã thử chậm để loại trừ rate-limit: mọi casing, có/không dấu cách, dạng path, `NoNeedToWonder`, `HauntedHouse`, tên 8.3). Folder chỉ có đúng 2 tên này (cùng File Droid). ⇒ Q7 để `needs_verification`; **không bịa flag**.

## 5. Trạng thái xác minh

6/7 câu được service xác nhận `✔ Correct`. Flag chỉ lộ khi đủ 7 ⇒ chưa có flag. Đáp án đúng đã lưu trong manifest.

## 6. Bài học & lỗi thường gặp

- **Jump List = OLE compound file**; parse bằng `olefile`, đọc `DestList` để map entry→stream, mỗi stream là LNK.
- **TrackerDataBlock** là nơi lấy hostname + droid GUID chuẩn; đừng lấy droid từ DestList (offset field khác, dễ lệch 8 byte).
- **File Droid (ObjectID) bền vững qua rename** — dùng để lần theo lịch sử tên/di chuyển của folder.
- **Remnant do OLE không truncate**: overwrite stream ngắn hơn để lại đuôi LNK cũ — nơi giấu tên trước khi đổi.
- **Định dạng đáp án quan trọng**: GUID phải lowercase-no-braces; format là `OLE CF` chứ không phải `CDF V2`.
- **Lỗi còn tồn:** Q7 forensic rõ là `SoulSearch` nhưng service không nhận — cần đối chiếu đáp án chuẩn của tác giả.
