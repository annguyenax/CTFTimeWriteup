#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote
import json,math,sys,time
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'solve_vendor'))
import requests
from streetview import search_panoramas
STREETS=[('Holt','Britten-Jones Drive'),('Holt','Lindrum Crescent'),('Holt','Mockridge Crescent'),('Holt','Armstrong Crescent'),('Holt','Lionel Rose Street'),('Holt','Griffiths Street'),('Latham','Stretton Crescent'),('Latham','Solomon Crescent'),('Latham','Cleland Street'),('Macgregor','Osburn Drive'),('Macgregor','Hirschfeld Crescent'),('Macgregor','Clode Crescent'),('Flynn','Vickers Crescent'),('Flynn','Dolling Crescent'),('Melba','Sampson Close'),('Melba','Scarlett Street'),('Florey','Sloane Place'),('Macquarie','Biraban Place'),('Weetangera','Crace Street'),('Evatt','Stenhouse Close')]
UA={'User-Agent':'BushBash-CTF-OSINT/1.0'}
def flat(g):
 c=g.get('coordinates',[])
 if g.get('type')=='LineString':return [(y,x) for x,y in c]
 if g.get('type')=='MultiLineString':return [(y,x) for line in c for x,y in line]
 return []
def sample(p,n=7):return [p[i] for i in sorted(set(round(j*(len(p)-1)/max(1,n-1)) for j in range(min(n,len(p)))))] if p else []
def dist(a,b):return math.hypot((a[0]-b[0])*111000,(a[1]-b[1])*91000)
out=[];seen=set()
for suburb,street in STREETS:
 q=quote(f'{street}, {suburb}, ACT, Australia');rows=requests.get(f'https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&polygon_geojson=1&q={q}',headers=UA,timeout=20).json();pts=[]
 for row in rows:
  pts=flat(row.get('geojson',{}))
  if pts:break
 pts=sample(pts);print(suburb,street,len(pts),flush=True);time.sleep(1.05)
 for pt in pts:
  ps=[p for p in search_panoramas(*pt) if p.date and dist(pt,(p.lat,p.lon))<90]
  if not ps:continue
  p=min(ps,key=lambda x:x.date)
  if p.pano_id in seen:continue
  seen.add(p.pano_id)
  for yaw in (p.heading,(p.heading+180)%360):out.append(dict(suburb=suburb,street=street,lat=p.lat,lon=p.lon,date=p.date,panoid=p.pano_id,yaw=yaw))
(ROOT/'belconnen_old.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('views',len(out))
