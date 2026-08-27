#!/usr/bin/env python3
"""Prepare a bounded panorama shortlist from tree-lined Canberra streets."""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'solve_vendor'))
import requests
from streetview import search_panoramas

STREETS=[
 ('Yarralumla','Schlich Street'),
 ("O'Connor",'Scrivener Street'),("O'Connor",'Miller Street'),("O'Connor",'Wattle Street'),("O'Connor",'Boronia Drive'),
 ('Ainslie','Duffy Street'),('Ainslie','Officer Crescent'),('Ainslie','Raymond Street'),('Ainslie','Paterson Street'),('Ainslie','Corroboree Park'),
 ('Narrabundah','Caley Crescent'),('Narrabundah','Green Street'),('Narrabundah','Finniss Crescent'),('Narrabundah','Sprent Street'),('Narrabundah','Carnegie Crescent'),('Narrabundah','Walker Crescent'),
 ('Weston','Wakelin Circuit'),('Weston','Chevalier Street'),('Weston','Rubbo Crescent'),
 ('Griffith','Jansz Crescent'),('Griffith','Stuart Street'),
 ('Lyneham','Goodwin Street'),('Lyneham','Wattle Street'),('Lyneham','Longstaff Street')]
UA={'User-Agent':'BushBash-CTF-OSINT/1.0'}
def dist(a,b):return math.hypot((a[0]-b[0])*111000,(a[1]-b[1])*91000)
def flat(g):
 c=g.get('coordinates',[])
 if g.get('type')=='LineString':return [(y,x) for x,y in c]
 if g.get('type')=='MultiLineString':return [(y,x) for line in c for x,y in line]
 return []
def samples(pts,n=6):
 if not pts:return []
 ids=sorted(set(round(i*(len(pts)-1)/max(1,n-1)) for i in range(min(n,len(pts)))))
 return [pts[i] for i in ids]
def geocode(suburb,street):
 q=quote(f'{street}, {suburb}, ACT, Australia')
 rows=requests.get(f'https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&polygon_geojson=1&q={q}',headers=UA,timeout=20).json()
 for r in rows:
  pts=flat(r.get('geojson',{}))
  if pts:return samples(pts)
 return []
def main():
 recs=[];seen=set()
 for suburb,street in STREETS:
  pts=geocode(suburb,street);print(suburb,street,len(pts),flush=True);time.sleep(1.05)
  for pt in pts:
   ps=[p for p in search_panoramas(*pt) if dist(pt,(p.lat,p.lon))<100]
   dated=[p for p in ps if p.date]
   if not dated:continue
   p=max(dated,key=lambda x:x.date)
   if p.pano_id in seen:continue
   seen.add(p.pano_id)
   for yaw in (p.heading,(p.heading+180)%360):
    recs.append(dict(suburb=suburb,street=street,lat=p.lat,lon=p.lon,date=p.date,panoid=p.pano_id,yaw=yaw))
 (ROOT/'candidate_panos.json').write_text(json.dumps(recs,indent=2),encoding='utf8')
 print('views',len(recs))
if __name__=='__main__':main()
