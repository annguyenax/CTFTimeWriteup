# Silicon Data Sleuthing — HTB TryOut (forensics, easy)

## Tóm tắt
Cho một dump flash router 16 MiB (`chal_router_dump.bin`, OpenWrt). Service (nc)
hỏi 8 câu về firmware; trả lời đủ 8 câu sẽ in flag. **Phần hash cuối của flag đổi
theo từng instance**, nên phải trích câu trả lời từ dump rồi tự động trả lời.

## Bố cục flash
| Offset | Nội dung |
|---|---|
| `0x180000` | uImage (kernel) |
| `0x42c2c8` | squashfs (xz) — rootfs read-only: OpenWrt **23.05.0**, kernel **5.15.134** |
| overlay | JFFS2 (rootfs_data) — chứa `/etc/*` đã cấu hình |

## Điểm mấu chốt khi trích JFFS2 overlay
- Node dùng nodetype **`0xe001`** (dirent) / **`0xe002`** (inode) — có set feature
  bits ở nibble cao, khác `0x2001/0x2002` chuẩn (nên parser ngây thơ bỏ sót).
- File `/etc/*` nén **LZMA của OpenWrt** (compr `8`): raw-LZMA1, `lc=0 lp=0 pb=0`,
  dict `0x10000`. Tự dựng header LZMA-alone (`prop=0`, dict, dsize) để giải.
- Node dài 0 là metadata-only (chmod...), **không** được ghi đè dữ liệu; dùng
  `isize` của version mới nhất làm kích thước file.

## Câu trả lời (trích từ overlay)
| Câu hỏi | Trả lời | Nguồn |
|---|---|---|
| OpenWRT version | `23.05.0` | squashfs `/etc/openwrt_release` |
| Kernel version | `5.15.134` | squashfs `/lib/modules/<ver>` |
| Root password hash (cả dòng) | `root:$1$YfuRJudo$cXCiIJXn9fWLIt8WY2Okp1:19804:0:99999:7:::` | JFFS2 `/etc/shadow` (LZMA) |
| PPPoE username | `yohZ5ah` | JFFS2 `/etc/config/network` |
| PPPoE password | `ae-h+i$i^Ngohroorie!bieng6kee7oh` | // |
| WiFi SSID | `VLT-AP01` | JFFS2 `/etc/config/wireless` |
| WiFi Password | `french-halves-vehicular-favorable` | // (`option key`) |
| 3 WAN ports redirect WAN→LAN | `1778,2289,8088` | JFFS2 `/etc/config/firewall` (`src_dport` của 3 `config redirect` DNAT) |

## Chạy
```
python solve/solve.py 154.57.164.82 32170
```
Script parse JFFS2, giải LZMA, tính đáp án rồi tự động trả lời quiz và ghi
`final_flag.txt`.

## Flag (verified live 2026-08-20)
`HTB{Y0u'v3_m4st3r3d_0p3nWRT_d4t4_3xtr4ct10n!!_4ae20e9bfcec8b9436f6de0df9f00b94}`
(prefix cố định là "achievement", hash cuối đổi theo instance.)

## Khắc phục
Không nhúng secret (mật khẩu PPPoE/WiFi, hash root) dạng khôi phục được trong
firmware phân phối; mã hoá partition cấu hình, xoá secret trước khi ship, dùng
per-device provisioning.
