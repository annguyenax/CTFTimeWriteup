import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
u = "u%d"%random.randint(10000,99999); pw="pass12345"
requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
tok = pf.login(u,pw)

def trigger(tok, zipcomp):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipcomp) as zf:
        zf.writestr("data.txt", b"x")
    bio.seek(0)
    pid = pf.create_platform(tok, "tr%d"%random.randint(0,9999), name="z")
    mid = pf.create_mod(tok, "v%d"%random.randint(0,9999), title="z")
    bid = pf.create_build(tok, mid, pid)
    return requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/",
        headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)

r = trigger(tok, zipfile.ZIP_LZMA)
print("LZMA trigger ->", r.status_code, r.text[:80])
time.sleep(2)
c = requests.get(f"{BASE}/rlmark.txt", timeout=8)
print("rlmark status:", c.status_code)
print("body:", repr(c.content[:200]))
