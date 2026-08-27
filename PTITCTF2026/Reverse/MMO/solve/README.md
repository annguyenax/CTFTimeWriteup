# MMO solver notes

Outer `files/main.exe` is Nuitka onefile. Extracted tree is already in `solve/unpacked/`.

Primary API string (inner `unpacked/main.exe`):

```
https://raw.githubusercontent.com/HungHT1890/free_proxy_list_api/refs/heads/main/api.json
```

Re-extract:

1. PE resource RT_RCDATA / ID 27 at file offset `0x3FD24`.
2. Skip 3-byte `KAY`, zstd-decompress.
3. Walk UTF-16LE path + uint64 size.
