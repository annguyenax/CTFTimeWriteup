# L3ak APT — khôi phục ảnh đã xóa từ Windows thumbnail cache

## Tóm tắt

Handout là một Windows forensic collection gồm NTFS metadata, registry, browser,
Recent Items, uTorrent state, ActivitiesCache và thumbnail cache. Người dùng
`Max` đã tải `important files.7z`, giải nén rồi mở ít nhất hai ảnh `ARS-*` bằng
Photos. File gốc đã biến mất khỏi collection, nhưng Windows Explorer vẫn giữ
thumbnail độ phân giải 1280.

Parse `thumbcache_1280.db` khôi phục một poster “RIZZLER” có chuỗi:

```text
L3AK{For3nsics_hUm4n$_C4n_c00K_AI}
```

Trạng thái: **verified**. Hai CMMM entry có cache hash khác nhau chứa payload JPEG
giống hệt; hai lần solver replay từ archive gốc cũng cho cùng SHA-256
`daa218b9d1713248f7069667ace2e21bcc46b42980e8b87c955ab1ec341701a2`.

## Đề bài yêu cầu gì?

Một người khoe rằng mình có “super secret data” và đã gia nhập một APT. Ta nhận
bản sao hệ thống để kiểm tra lời khoe đó. Mục tiêu forensic thực tế là tìm dấu vết
file bí mật, lần theo cách người dùng truy cập nó và khôi phục nội dung còn sót.

File gốc:

- `files/L3AK_APT.zip`, 144,991,770 byte;
- SHA-256: `e681d3bacaa0b8ad36715e6b355981201816341dcef11d0829f80a7ac46c5a98`;
- 1,222 file, tổng dung lượng giải nén khoảng 705 MB.

## Kiến thức nền

### Recent Items và LNK

Windows tạo shortcut `.lnk` cho tài liệu/thư mục được mở gần đây. Dù file đích đã
bị xóa, LNK thường còn giữ đường dẫn, volume information và đôi khi ObjectId.
Đây là nguồn triage rất rẻ: đọc nó trước khi carve `$MFT` hoặc disk image.

### ActivitiesCache

Connected Devices Platform lưu user activities trong `ActivitiesCache.db` và WAL.
Payload của activity có thể chứa tên app, display text, đường dẫn file, URI và
NTFS ObjectId. WAL quan trọng vì record mới có thể chưa được checkpoint vào DB.

### Windows thumbnail cache

Explorer lưu thumbnail trong các file `thumbcache_<size>.db`. Database và từng
entry bắt đầu bằng magic `CMMM`. Với định dạng trong challenge, entry chứa:

```text
signature | entry_size | cache_hash | identifier_length | padding_size
          | data_size | dimensions/metadata | checksums | identifier | payload
```

Các trường length cho phép lấy chính xác JPEG/PNG. Tìm `FFD8`/`FFD9` đơn thuần dễ
bắt nhầm marker trong metadata hoặc cắt sai một JPEG.

## Quá trình phân tích

### 1. Kiểm kê archive

Liệt kê ZIP cho thấy đây không phải raw disk image mà là triage collection:

- `$MFT`, `$LogFile`, `$Extend/$J`;
- registry hives và 120 EVTX;
- Chrome/Edge/Discord/uTorrent artefacts;
- `ActivitiesCache.db` cùng WAL;
- `thumbcache_16.db` đến `thumbcache_2560.db`.

Do đề nhắc “secret data”, giả thuyết ưu tiên là tìm Recent/Downloads/Documents
trước. Các LNK quyết định gồm:

```text
C:\Users\Max\Downloads\important files.7z
C:\Users\Max\Downloads\important files\Projects\media\ARS-CB-047.png
C:\Users\Max\Downloads\important files\Projects\media\ARS-SEC-154.png
```

### 2. Xác nhận archive từng được tải đầy đủ

`AppData/Roaming/uTorrent/important files.torrent` là metadata bencode:

```text
name         = important files.7z
length       = 7,168,714
piece length = 32,768
created by   = qBittorrent v5.2.3
```

`resume.dat` cho thêm bằng chứng:

```text
path         = C:\Users\Max\Downloads\important files.7z
downloaded   = 7,168,714
corrupt      = 0
hashfails    = 0
added_on     = 2026-06-07 21:21:56 UTC
completed_on = 2026-06-07 21:22:13 UTC
```

Như vậy file đã tải đủ. Không cần liên hệ tracker hay peer—vừa không cần thiết,
vừa trái với hướng giải offline.

### 3. Dựng activity timeline

Mở `ActivitiesCache.db` read-only cùng file WAL rồi lọc payload theo IOC đã biết:

```sql
SELECT ActivityType, LastModifiedTime, CAST(Payload AS TEXT)
FROM Activity
WHERE instr(CAST(Payload AS TEXT), 'important files') > 0
   OR instr(CAST(Payload AS TEXT), 'ARS-') > 0;
```

Hai activity Photos xuất hiện:

| UTC | Display text | Đường dẫn |
|---|---|---|
| 2026-06-07 21:12:33 | `ARS-CB-047.png` | `Downloads\important files\Projects\media\...` |
| 2026-06-07 21:56:41 | Photos Session | `ARS-SEC-154.png` |

Record đầu còn có NTFS ObjectId. Windows Search gather log và NTUSER.DAT độc lập
xác nhận cùng tên file/đường dẫn.

### 4. Khôi phục thumbnail

Các cache có payload ảnh thật:

- `thumbcache_1280.db`: 6 JPEG;
- `thumbcache_768.db`: 4 JPEG;
- `thumbcache_256.db`: JPEG và PNG;
- các size nhỏ hơn chứa bản thu nhỏ tương ứng.

Hai cache hash sau trong `thumbcache_1280.db` chứa cùng poster RIZZLER:

```text
15c78729be0524d8
237b7fe66e1c61d4
```

Cả hai payload dài 185,015 byte và byte-identical. Các hash này còn lặp ở cache
768 và 256 với cùng hình ở độ phân giải tương ứng. Đây là corroboration độc lập
cho việc khôi phục, không phải một signature-carve trùng hợp.

## Solver và lệnh tối thiểu

Từ thư mục gốc event:

```powershell
python ".\Forensics\L3ak APT\solve\solve.py" `
  ".\Forensics\L3ak APT\files\L3AK_APT.zip" `
  ".\Forensics\L3ak APT\solve\evidence\rizzler.jpg"
```

Solver dùng Python standard library, không giải nén toàn collection. Nó:

1. đọc đúng `thumbcache_1280.db` từ ZIP;
2. duyệt entry theo `entry_size`;
3. tính payload offset từ `identifier_length` và `padding_size`;
4. yêu cầu tìm thấy cả hai cache hash;
5. yêu cầu hai payload giống nhau và có JPEG SOI/EOI hợp lệ;
6. ghi đúng một ảnh evidence.

## Xác minh flag

- Ảnh evidence chứa nguyên chuỗi trong dấu `{}`; `$` sau `hUm4n` là ký tự thật,
  không phải chữ `s`.
- Hai entry CMMM khác cache hash có payload giống hệt.
- Replay solver hai lần từ `L3AK_APT.zip` tạo cùng SHA-256
  `daa218b9d1713248f7069667ace2e21bcc46b42980e8b87c955ab1ec341701a2`.
- Không submit lên scoreboard theo phạm vi học tập offline.

## Nhánh không hiệu quả và lỗi thường gặp

- **Carve toàn `$MFT`/USN ngay:** metadata này hữu ích cho timeline nhưng không
  chứa nội dung của file PNG non-resident. Recent/Activity/thumbnail rẻ hơn nhiều.
- **Tải lại torrent từ Internet:** không cần; handout đã giữ thumbnail quyết định.
- **Carve JPEG chỉ bằng SOI/EOI:** tạo một số file truncated vì marker có thể xuất
  hiện không đúng boundary. Dùng `entry_size` và `data_size` của CMMM.
- **Bỏ qua WAL:** activity `ARS-*` nằm trong `ActivitiesCache.db-wal`; chỉ copy DB
  riêng có thể bỏ sót record mới.
- **Chỉ tin một thumbnail:** nên kiểm tra cùng ảnh ở cache hash/size khác và replay
  từ archive gốc.

## Bài học và checklist nhanh

1. Hash và liệt kê forensic collection trước.
2. Dùng tên file từ Recent/LNK làm IOC.
3. Correlate IOC với download-client state và ActivitiesCache/WAL.
4. Nếu file ảnh đã xóa, kiểm tra `thumbcache_*.db` trước disk carving.
5. Parse container theo length field; giữ cache hash và payload hash.
6. Xác minh bằng duplicate entry và deterministic replay.

HexStrike không được dùng: handout cục bộ đã chứa mọi artefact cần thiết và parser
CMMM nhỏ, có mục tiêu, nhanh hơn việc chuyển 138 MB sang Kali.

## Nguồn tham khảo

- [libyal/libwtcdb — Windows Explorer Thumbnail Cache format](https://github.com/libyal/libwtcdb/blob/main/documentation/Windows%20Explorer%20Thumbnail%20Cache%20database%20format.asciidoc) — cấu trúc database/entry thumbnail cache.
- [Eric Zimmerman — WxTCmd](https://github.com/EricZimmerman/WxTCmd) — implementation tham khảo cho việc parse Windows thumbnail cache.
- [Microsoft Learn — User activities](https://learn.microsoft.com/en-us/windows/apps/develop/windows-integration/user-activities) — khái niệm user activity và activity data trên Windows.
