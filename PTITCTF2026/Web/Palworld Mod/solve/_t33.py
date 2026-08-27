import sys, requests
sys.path.insert(0, ".")
import palforge as pf
BASE="http://144.79.188.39:36534"; pf.BASE=BASE
tok=pf.login(*pf.ADMIN); h={"Authorization":f"Bearer {tok}"}
mods=requests.get(f"{BASE}/api/mods/",headers=h,timeout=15).json()
print("count",mods.get("count"))
for m in mods.get("results",[]):
    d=requests.get(f"{BASE}/api/mods/%s/"%m["id"],headers=h,timeout=15).json()
    print("id=%s owner=%s v=%s t=%s notes=%r"%(m["id"],m["owner"],m["mod_version"],m["title"],d.get("release_notes")))
    for b in d.get("builds",[]):
        print("   build",b["id"],"storage=",b.get("storage_path"),"fl=",repr(b.get("filelist_content"))[:100])
