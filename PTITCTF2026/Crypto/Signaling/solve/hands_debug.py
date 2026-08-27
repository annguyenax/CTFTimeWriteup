#!/usr/bin/env python3
import math, cv2, numpy as np
from pathlib import Path
VID = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4")
c = cv2.VideoCapture(str(VID))
ok, fr = c.read()
h,w = fr.shape[:2]
cx, cy = 553, 673
NAMES=["12","1:30","3","4:30","6","7:30","9","10:30"]

def scores(g):
    hs=[]
    for k in range(8):
        a=math.radians(k*45)
        dx, dy = math.sin(a), -math.cos(a)
        vals=[]
        for r in range(70, 160):
            x=int(round(cx+dx*r)); y=int(round(cy+dy*r))
            if 0<=x<w and 0<=y<h:
                vals.append(int(g[y,x]))
        hs.append(max(vals) if vals else 0)
    return hs

for fi in [0,40,50,70,100,200,300,450]:
    c.set(cv2.CAP_PROP_POS_FRAMES, fi)
    ok, fr = c.read()
    g=cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    hs=scores(g)
    order=np.argsort(hs)[::-1]
    print(f"f{fi:3d}", [(NAMES[i], hs[i]) for i in order[:4]], "all", hs)
