import requests
BASE="http://144.79.188.39:36534"
for p in ["builds/2.4.1/steam_win/more_pals_per_base.pak",
          "builds/1.9.0/steam_win/legendary_pal_skins_pack.pak",
          "builds/4.0.0/steam_win/neon_pals_graphics_overhaul.pak",
          "flag.txt","flag","secret.txt"]:
    r=requests.get(f"{BASE}/media/{p}",timeout=8)
    print(p, r.status_code, repr(r.content[:80]))
# also check nginx html for flag files
for p in ["flag.txt","final.txt","f.txt","result.txt","out.txt","1.txt"]:
    r=requests.get(f"{BASE}/{p}",timeout=6)
    ishtml="doctype" in r.text[:40].lower() or "<html" in r.text[:200].lower()
    if not ishtml and len(r.text)<2000:
        print("HTMLFILE", p, r.status_code, repr(r.text[:80]))
