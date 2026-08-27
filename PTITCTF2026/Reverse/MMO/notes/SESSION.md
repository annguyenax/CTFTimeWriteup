# PTITCTF2026 Reverse / MMO — session notes

Challenge (verbatim): Một người bạn làm trong lĩnh vực MMO, gian lận hắn ta có 1 phần mềm lấy proxy miễn phí. Hãy cho biết phần mềm proxy đó lấy dữ liệu chính từ API nào?

Binary: `D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\MMO\files\main.exe`
- SHA256: `5cbe2adb59cde80413b5a248f52ed30fca4071c425862ca2f9df50f672a25890` (verified)
- Size: 26217984 bytes (~26 MB)

## 1. Binary type

Outer `main.exe` is a **Nuitka onefile** Windows PE64 bootstrap, not PyInstaller/Electron/.NET/Go/AutoIt.

Evidence:
- PE32+ (machine 0x8664, optional magic 0x20B), 12 sections, CLR directory empty
- Compiler: MinGW-W64 GCC 14.2.0 (Brecht Sanders)
- Strings: `NUITKA_ONEFILE_PARENT`, `NUITKA_ONEFILE_DIRECTORY`, `NUITKA_ORIGINAL_ARGV0`, `Error, couldn't find attached data header.`
- Code/.text is tiny (~112 KB); almost all size is `.rsrc` (0x18DF50C)
- No overlay (last section ends at EOF)
- Assembly identity in manifest: `name="Mini" version="1.0.0.0"`

Nuitka Windows onefile stores the archive as **RT_RCDATA (type 10) / ID 27**:
- File offset `0x3FD24`
- Size `25954456`
- Magic `KAY` + zstd frame (`28 B5 2F FD`)

`KAY` = compressed payload (`KA` + `Y`). Filenames in the archive are UTF-16LE; no per-file checksum (temp-dir / stream-compression mode, not cache checksum mode).

## 2. Extraction

1. Parse PE resource tree → RT_RCDATA/27
2. Slice payload after `KAY`, zstd-decompress (Python `zstandard`, 25,954,453 → 88,494,987 bytes)
3. Walk entries: UTF-16LE NUL-terminated path, `uint64` size, then raw bytes
4. Output: `D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\MMO\solve\unpacked\` (67 files)

First extracted file is the real app: `unpacked\main.exe` (17,626,112 bytes), Nuitka **standalone** Python 3.10 + PyQt5:
- `python310.dll`, Qt5/PyQt5, `requests`, `certifi`, `zstandard`, `_ssl.pyd`, etc.
- Compiled modules: `gui_proxy.py`, `proxy_checker.py`, `icon_rc.py`

Decompressed payload also kept as `solve\payload.bin`.

## 3. API endpoint (literal in inner binary)

Nuitka constants blob in inner `main.exe`:

- Offset `0x1073380`:
  `https://raw.githubusercontent.com/HungHT1890/free_proxy_list_api/refs/heads/main/api.json`
- Bound to `ProxyChecker.get_config_api` (`proxy_checker.py`)
- Log strings: `Đã lấy thành công list api proxy`, `Lỗi khi lấy api proxy`, `Không lấy được list api proxy - liên hệ t.me/hunght1890`

`get_proxy_from_api` then pulls IP:port lists from URLs in that JSON (`http` / `socks4` / `socks5` arrays). The JSON is an aggregator; the **primary API the program itself fetches** is the HungHT1890 `api.json`.

Secondary URL (not the proxy-list source): `https://api.myip.com` used by `check_proxy` / country lookup. UI test servers: Google, Facebook, Youtube, Ipify, Gmail.

App identity:
- Window title: `Tool Crawl Proxy - Chia sẻ miễn phí cho cộng đồng MMO - t.me/hunght1890`
- Modes: “Lấy - Check Live Die” / “Lấy - Không check”
- Author: hunght1890 (matches the GitHub repo in the API URL)

The `u` prefix on strings (`uhttps://...`) is Nuitka’s unicode constant tag, not part of the URL.

## 4. Flag

Verified URL is literally in the inner binary at `0x1073380`.

Candidate (and reported) flag:

```
PTITCTF{https://raw.githubusercontent.com/HungHT1890/free_proxy_list_api/refs/heads/main/api.json}
```

Written to `writeup\final_flag.txt`.

## 5. Evidence paths

| What | Path |
|------|------|
| Outer sample | `files\main.exe` |
| Decompressed onefile payload | `solve\payload.bin` |
| Inner Nuitka app | `solve\unpacked\main.exe` |
| Extracted dist | `solve\unpacked\` |
| ASCII strings (outer) | `solve\strings_ascii.txt` |
| ASCII strings (inner) | `solve\inner_strings_ascii.txt` |
| Flag | `writeup\final_flag.txt` |
