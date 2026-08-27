#!/usr/bin/env python3
"""Probe a short evidence-led list of park-edge street hypotheses."""
from __future__ import annotations
import io, json, math, sys
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "solve_vendor"))
import requests
from PIL import Image, ImageDraw
from streetview import search_panoramas

PLACES = {
    "corroboree": (-35.26843, 149.14222),
    "oconnor_wetlands": (-35.25895, 149.11712),
    "wakefield_gardens": (-35.26590, 149.13635),
    "haig_park_east": (-35.27420, 149.13420),
}

def dist(a,b):
    return math.hypot((a[0]-b[0])*111000, (a[1]-b[1])*91000)

def thumb(pid,yaw):
    u=("https://streetviewpixels-pa.googleapis.com/v1/thumbnail?"+
       f"panoid={quote(pid)}&cb_client=maps_sv.tactile&w=512&h=384&yaw={yaw:.1f}&pitch=0&thumbfov=78")
    r=requests.get(u,timeout=20); r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGB")

def main():
    out=ROOT/"sv_places"; out.mkdir(exist_ok=True)
    recs=[]; seen=set()
    for label,center in PLACES.items():
        # 3x3 points at roughly 120 m spacing around the place.
        for iy in (-1,0,1):
            for ix in (-1,0,1):
                pt=(center[0]+iy*0.00108,center[1]+ix*0.00132)
                panos=[p for p in search_panoramas(*pt) if dist(pt,(p.lat,p.lon))<130 and p.date]
                panos.sort(key=lambda p:p.date)
                if not panos: continue
                p=panos[0]
                if p.pano_id in seen: continue
                seen.add(p.pano_id)
                for yaw in (p.heading,(p.heading+180)%360):
                    try:
                        im=thumb(p.pano_id,yaw)
                    except Exception as exc:
                        print("skip", label, p.pano_id, exc)
                        continue
                    fn=f"{len(recs):03}_{label}_{p.date}_{round(yaw)}.jpg"
                    im.save(out/fn,quality=90)
                    recs.append(dict(file=fn,place=label,lat=p.lat,lon=p.lon,date=p.date,panoid=p.pano_id,yaw=yaw))
                    time.sleep(0.35)
    (out/"metadata.json").write_text(json.dumps(recs,indent=2),encoding="utf-8")
    cols=4; cw,ch=256,216
    sheet=Image.new("RGB",(cols*cw,math.ceil(len(recs)/cols)*ch),"white"); d=ImageDraw.Draw(sheet)
    for i,r in enumerate(recs):
        im=Image.open(out/r["file"]).resize((cw,192)); x=(i%cols)*cw;y=(i//cols)*ch
        sheet.paste(im,(x,y)); d.text((x+2,y+194),f"{i:02} {r['place'][:13]} {r['date']}",fill="black")
    sheet.save(out/"contact.jpg",quality=92)
    print(json.dumps(recs,indent=2))

if __name__=="__main__": main()
