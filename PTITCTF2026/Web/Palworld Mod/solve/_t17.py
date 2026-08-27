import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

tok,u=fresh()
# 1. upload a real file to /data/media via a build
pid = pf.create_platform(tok, "win%d"%random.randint(0,9999), name="z")
mid = pf.create_mod(tok, "2.4.1", title="z")
bid = pf.create_build(tok, mid, pid)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("real.txt", b"REALFILE")
bio.seek(0)
r=requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)
print("upload real ->", r.status_code)
# storage path = builds/2.4.1/<platformcode> ; try serving
served = requests.get(f"{BASE}/media/builds/2.4.1/win{''}/real.txt", timeout=8)
# find actual storage_path
detail = requests.get(f"{BASE}/api/mods/{mid}/", headers={"Authorization":f"Bearer {tok}"}, timeout=15).json()
for b in detail.get("builds",[]):
    sp=b.get("storage_path")
    print("build storage:", sp, "filelist:", b.get("filelist_content"))
    # serve the real file
    url = f"{BASE}/media/{sp}/real.txt"
    c = requests.get(url, timeout=8)
    print("serve", url, "->", c.status_code, repr(c.content[:40]))
