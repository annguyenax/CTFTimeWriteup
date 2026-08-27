# Evidence manifest — Transcendent Renovation (6/7, needs_verification)

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| ../solve.py | Trích 6 đáp án từ Jump List | Python + olefile | `python solve/solve.py <AutomaticDestinations dir>` | Solver tái lập |
| stream46.bin | Stream chứa entry NoNeedToWonder: LNK hiện tại + remnant SoulSearch + tracker (hostname/droid) | olefile openstream('46') | như trên | Bằng chứng cốt lõi Q3–Q7 |

## Đáp án (6/7 đã được service chấp nhận)

| # | Câu hỏi | Đáp án | Nguồn |
|---|---------|--------|-------|
| 1 | File format của Jump List | `OLE CF` | `file` → "Composite Document File V2" |
| 2 | automaticDestinations chứa NoNeedToWonder | `f01b4d95cf55d32a.automaticDestinations-ms` | grep tên trong file |
| 3 | Share path | `\\tsclient\HauntedHouse` | LinkInfo/stream 45 (ổ RDP redirect) |
| 4 | Stream chứa rename data | `46` | DestList entry → stream 0x46 |
| 5 | File Droid GUID | `ec2ab952-7e4d-11f1-89ad-a2dead7852ad` | LNK TrackerDataBlock DroidFileId (lowercase, no braces) |
| 6 | Hostname | `logging-vm` | LNK TrackerDataBlock MachineID |
| 7 | Original name | *chưa giải* — forensic = `SoulSearch` nhưng service từ chối | remnant LNK cũ trong stream 46 |

## Ghi chú Q7 (blocker)

- Stream 46 = 867 byte. LNK hợp lệ (0–490) trỏ tới `NoNeedToWonder` (hiện tại). Phần đuôi (490–867) là **remnant** của LNK cũ (khi folder tên `SoulSearch`) do stream bị ghi đè bằng LNK ngắn hơn (OLE không truncate). Đây chính là "rename data".
- Forensic ⇒ original = `SoulSearch`. Đã thử (chậm, tránh rate-limit): `SoulSearch`, mọi casing, `Soul Search`, path forms, `NoNeedToWonder`, `HauntedHouse`, 8.3 names — **tất cả Incorrect**. Không có cơ chế hint. Chỉ tồn tại 2 tên này cho folder (cùng File Droid). Q7 để lại `needs_verification`.

Artifact gốc: `files/TranscendentRenovation.zip` (nested `Administrator_JumpLists.zip`) — pw `dead7852`
SHA-256: `82b2d7c18545b83a7975cbb6dc427692dc3ecba17b6cca3e0de3dd8a5e880549`
