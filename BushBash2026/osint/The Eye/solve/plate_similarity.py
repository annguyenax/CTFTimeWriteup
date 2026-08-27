import contextlib, io, itertools, sys
import cv2
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from skimage.transform import SimilarityTransform

im=cv2.imread("dots.png"); b,g,r=cv2.split(im)
red=(r>90)&(r>g*1.35)&(r>b*1.35)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"),np.ones((7,7),np.uint8))>0]=0
n,lab,stats,_=cv2.connectedComponentsWithStats((gray>15).astype("uint8"))
flat=lab.ravel(); wt=gray.ravel().astype(float); yy,xx=np.indices(gray.shape)
flux=np.bincount(flat,weights=wt,minlength=n)
sx=np.bincount(flat,weights=wt*xx.ravel(),minlength=n); sy=np.bincount(flat,weights=wt*yy.ravel(),minlength=n)
valid=np.array([i for i in range(1,n) if stats[i,4]>=3 and flux[i]>0]); valid=valid[np.argsort(flux[valid])[::-1]]
img=np.array([[sx[i]/flux[i],sy[i]/flux[i]] for i in valid]); itree=cKDTree(img)

gaia=pd.read_csv("gaia_pleiades.csv").sort_values("phot_g_mean_mag")
ra=gaia.ra.to_numpy(); dec=gaia.dec.to_numpy(); dec0=np.deg2rad(24.2)
cat=np.c_[(ra-56.7)*np.cos(dec0),dec-24.2]

def triangles(points,N):
    desc=[]; ids=[]
    for comb in itertools.combinations(range(N),3):
        q=points[list(comb)]
        d=np.array([np.linalg.norm(q[1]-q[2]),np.linalg.norm(q[0]-q[2]),np.linalg.norm(q[0]-q[1])])
        order=np.argsort(d) # vertices opposite shortest/middle/longest sides
        sides=np.sort(d)
        if sides[0]<1e-9 or sides[0]/sides[2]<.12: continue
        desc.append(sides[:2]/sides[2]); ids.append(np.array(comb)[order])
    return np.asarray(desc),np.asarray(ids)

cd,ci=triangles(cat,100); idesc,ii=triangles(img,110)
ctree=cKDTree(cd)
d,j=ctree.query(idesc,k=8)
pairs=[]
for row in range(len(ii)):
    for kk in range(8):
        if d[row,kk]<.035: pairs.append((float(d[row,kk]),int(j[row,kk]),row))
pairs.sort()
print("triangle_pairs",len(pairs),"best_error",pairs[0][0] if pairs else None)

best=[]; signatures=set()
for err,cidx,iidx in pairs[:100000]:
    model=SimilarityTransform()
    if not model.estimate(cat[ci[cidx]],img[ii[iidx]]): continue
    scale=model.scale
    if not (50<scale<1000): continue
    pred=model(cat[:600]); inside=(pred[:,0]>=0)&(pred[:,0]<im.shape[1])&(pred[:,1]>=0)&(pred[:,1]<im.shape[0])
    dist,rank=itree.query(pred)
    strict=int(np.sum(inside&(dist<3))); loose=int(np.sum(inside&(dist<8)))
    top=int(np.sum(inside[:100]&(dist[:100]<6)&(rank[:100]<200)))
    sig=(round(model.scale,2),round(model.rotation,3),round(model.translation[0],1),round(model.translation[1],1))
    if sig in signatures: continue
    signatures.add(sig)
    best.append((top,strict,loose,-err,model.params.copy()))
best.sort(reverse=True,key=lambda z:z[:4])
for rank,z in enumerate(best[:40],1):
    top,strict,loose,ne,mat=z
    model=SimilarityTransform(matrix=mat); pred=model(cat[:15]); dist,ind=itree.query(pred)
    print("MODEL",rank,"top",top,"strict",strict,"loose",loose,"err",-ne,"scale",model.scale,"rot",model.rotation,"trans",model.translation.tolist())
    print("catalog15 image_ranks",(ind+1).tolist(),"dist",np.round(dist,2).tolist(),"xy",np.round(pred,1).tolist())
