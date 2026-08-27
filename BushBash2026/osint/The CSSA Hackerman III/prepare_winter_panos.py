#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'solve_vendor'))
from streetview import search_panoramas
base=json.loads((ROOT/'candidate_panos.json').read_text())
out=[];seen=set()
for i,r in enumerate(base[::2]):
 ps=[p for p in search_panoramas(r['lat'],r['lon']) if p.date and 5<=int(p.date.split('-')[1])<=9]
 if not ps:continue
 p=max(ps,key=lambda x:x.date)
 if p.pano_id in seen:continue
 seen.add(p.pano_id)
 for yaw in (p.heading,(p.heading+180)%360):out.append({**{k:r[k] for k in ('suburb','street')},'lat':p.lat,'lon':p.lon,'date':p.date,'panoid':p.pano_id,'yaw':yaw})
 print(i,r['street'],p.date,flush=True)
(ROOT/'candidate_winter.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('views',len(out))
