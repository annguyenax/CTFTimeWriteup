# MMO

- **Event:** PTITCTF2026
- **Category / tags:** Reverse / Nuitka / packed Python
- **Flag format:** `PTITCTF{...}` (the primary proxy API URL)
- **Attachments:** `main.exe` (PE32+, 26217984 bytes)
- **Status:** solved

## Prompt (verbatim)

Một người bạn làm trong lĩnh vực MMO, gian lận hắn ta có 1 phần mềm lấy proxy miễn phí. Hãy cho biết phần mềm proxy đó lấy dữ liệu chính từ API nào?

## Recon

Outer `main.exe` is a **Nuitka onefile** bootstrap (MinGW-w64 GCC 14.2.0), not PyInstaller. Tiny `.text`; payload is PE resource **RT_RCDATA / ID 27** at file offset `0x3FD24`: magic `KAY` + zstd.

SHA256 `5cbe2adb59cde80413b5a248f52ed30fca4071c425862ca2f9df50f672a25890`.

## Extraction

1. Parse PE resource tree → RT_RCDATA/27.
2. Slice after `KAY`, zstd-decompress (25,954,453 → ~88 MB).
3. Walk UTF-16LE path + uint64 size entries into `solve/unpacked/` (67 files).

Inner app is Nuitka **standalone** Python 3.10 + PyQt5 (`gui_proxy.py`, `proxy_checker.py`). Window title: `Tool Crawl Proxy - Chia sẻ miễn phí cho cộng đồng MMO - t.me/hunght1890`.

## API

Literal URL in inner `main.exe` at `0x1073380`, bound to `ProxyChecker.get_config_api`:

```
https://raw.githubusercontent.com/HungHT1890/free_proxy_list_api/refs/heads/main/api.json
```

That JSON is the aggregator the program itself fetches (`http` / `socks4` / `socks5` arrays). `https://api.myip.com` is only the live-check / country lookup, not the proxy list source.

The Nuitka `u` prefix on unicode constants is not part of the URL.

## Flag

```
PTITCTF{https://raw.githubusercontent.com/HungHT1890/free_proxy_list_api/refs/heads/main/api.json}
```

## Verification

URL is an ASCII string in inner `unpacked/main.exe` (offset `0x10733a3` for `HungHT1890`). Secondary URLs (`api.myip.com`, Qt/github issue links) are not the proxy-list API.

## Dead ends

- Treating the outer PE as PyInstaller/Electron.
- Full-frame zstd on the resource (need stream reader after `KAY`).
