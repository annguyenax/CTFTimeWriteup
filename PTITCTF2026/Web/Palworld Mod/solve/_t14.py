import sys, requests
sys.path.insert(0, ".")
import palforge as pf
BASE = pf.BASE
tok = pf.login(*pf.ADMIN)
h = {"Authorization":f"Bearer {tok}"}
for mid in [6,7,8,9,10]:
    try:
        d = requests.get(f"{BASE}/api/mods/{mid}/", headers=h, timeout=15).json()
        print("=== mod", mid, d.get("title"), "v=",d.get("mod_version"), "owner=",d.get("owner"))
        print("  notes:", d.get("release_notes"))
        for b in d.get("builds",[]):
            print("   build", b.get("id"), "storage=", b.get("storage_path"))
            print("   filelist:", repr(b.get("filelist_content")))
    except Exception as e:
        print(mid,"err",e)
