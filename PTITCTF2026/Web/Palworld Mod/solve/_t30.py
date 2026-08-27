import sys, requests
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36310"; pf.BASE=BASE
tok=pf.login(*pf.ADMIN); h={"Authorization":f"Bearer {tok}"}
s=requests.get(f"{BASE}/api/schema/",timeout=15).text
for kw in ["FLAG","SECRET","environ","PTIT","env["]:
    if kw in s:
        i=s.index(kw); print("SCHEMA HIT",kw, s[max(0,i-40):i+80])
print("schema len", len(s))
# check owner=1 mods release_notes
for mid in [6,11,12,16,20]:
    d=requests.get(f"{BASE}/api/mods/%d/"%mid,headers=h,timeout=15).json()
    print("mod",mid,"notes=",repr(d.get("release_notes")),"title=",d.get("title"))
