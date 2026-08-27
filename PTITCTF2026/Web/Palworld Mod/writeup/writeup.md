# Palworld Mod — Writeup

## 1. Executive Summary
- **Challenge Name:** Palworld Mod
- **Event:** PTIT CTF 2026
- **Category:** Web
- **Flag:** `PTITCTF{w3lc0mE_t0_th3_InfosecPTIT_h0uSe_h3r3_1S_y0uR_61af5da2e260_mil_vnd}`
- **Vulnerabilities:**
  1. Zip-slip arbitrary file write via `Path(settings.MEDIA_ROOT) / 'builds' / mod_version / platform_code / filename`.
  2. Length restriction bypass via Python `pathlib.Path` root reset: `Path(A) / '/B'` resets path to `/B`.
  3. Dynamic Codec Loading RCE: Overwriting standard library encoding codec (`/usr/local/lib/python3.11/encodings/iso8859_2.py`) and triggering dynamic import via multipart request header `Content-Type: multipart/form-data; charset=iso8859_2`.

---

## 2. Vulnerability Analysis

### 2.1 Zip-Slip Primitive
In `apps/mods/views.py`:
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_build_files(request, mod_pk, pk):
    ...
    mod_version = build.mod.mod_version
    platform_code = build.platform.code
    storage_dir = Path(settings.MEDIA_ROOT) / 'builds' / mod_version / platform_code
    storage_dir.mkdir(parents=True, exist_ok=True)
    ...
    for name in names:
        ...
        filename = Path(name).name
        if not filename:
            continue
        (storage_dir / filename).write_bytes(data)
```

`mod_version` and `platform_code` are user-controlled fields. However:
- `Mod.mod_version` has `max_length=20`.
- `Platform.code` has `max_length=20`.
- Serializer validation strictly enforces `len(field) <= 20`.

### 2.2 The Apparent "2-Character Limitation"
Relative path traversal from `/data/media/builds` to `/usr/local/lib/python3.11/encodings` requires:
`../../../usr/local/lib/python3.11/encodings` (43 characters).
Splitting across two 20-character fields:
- `mod_version = "../../../usr/local/lib"` (22 chars > 20)
- `platform_code = "python3.11/encodings"` (20 chars)
Or:
- `mod_version = "../../../usr/local"` (18 chars)
- `platform_code = "lib/python3.11/encodings"` (24 chars > 20)

### 2.3 The Root Reset Bypass
In Python's `pathlib.Path`:
Joining a Path with a component starting with a leading slash `/` discards the preceding components and resets the path:
```python
Path('/data/media/builds') / '/usr/local/lib' / 'python3.11/encodings'
# -> PosixPath('/usr/local/lib/python3.11/encodings')
```
- `mod_version = "/usr/local/lib"` (14 chars <= 20)
- `platform_code = "python3.11/encodings"` (20 chars <= 20)

Both values are <= 20 characters and easily pass validation.

### 2.4 Dynamic Codec Execution
CPython loads standard library codecs on-demand from `/usr/local/lib/python3.11/encodings/<codec>.py`.
When Django processes a multipart request containing `charset=<codec>`:
`django.http.request.HttpRequest` sets `request.encoding = "iso8859_2"`, and `MultiPartParser` invokes `chunk.decode("iso8859_2")`, which calls `__import__('encodings.iso8859_2')`.

By uploading a malicious `iso8859_2.py` into `/usr/local/lib/python3.11/encodings/` and sending a request with `Content-Type: multipart/form-data; charset=iso8859_2`, Python imports our code and executes arbitrary commands as root.

---

## 3. Exploit Steps

1. Register and login to obtain JWT access token.
2. Create platform with `code = "python3.11/encodings"`.
3. Create mod with `mod_version = "/usr/local/lib"`.
4. Create a build linking mod and platform.
5. Upload zip containing `é/iso8859_2.py` (UTF-8 filename entry prevents premature codec lookup during plant).
   - Writes payload to `/usr/local/lib/python3.11/encodings/iso8859_2.py`.
   - Payload extracts `os.environ['FLAG']` to `/usr/share/nginx/html/<out_file>`.
6. Send POST request with `Content-Type: multipart/form-data; boundary=boundary; charset=iso8859_2`.
7. Retrieve flag from `GET /<out_file>`.

---

## 4. Full Exploit Script
Refer to [solve.py](../solve/solve.py).
