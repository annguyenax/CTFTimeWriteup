import cv2,numpy as np
from scipy.spatial import cKDTree
im=cv2.imread('dots.png'); b,g,r=cv2.split(im); red=(r>90)&(r>g*1.35)&(r>b*1.35)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); gray[cv2.dilate(red.astype('uint8'),np.ones((7,7),np.uint8))>0]=0
n,lab,st,cen=cv2.connectedComponentsWithStats((gray>15).astype('uint8'))
flat=lab.ravel();wt=gray.ravel().astype(float); yy,xx=np.indices(gray.shape)
flux=np.bincount(flat,weights=wt,minlength=n);sx=np.bincount(flat,weights=wt*xx.ravel(),minlength=n);sy=np.bincount(flat,weights=wt*yy.ravel(),minlength=n)
order=np.argsort(flux[1:])[::-1]+1
obs_all=np.array([[sx[i]/flux[i],sy[i]/flux[i]] for i in order])
rd=np.array([[56.4567,24.3678],[56.3021,24.4672],[56.4771,24.5547],[56.2008,24.2894],[57.2967,24.1367],[56.5817,23.9483],[56.21875,24.1133],[57.2904,24.0533],[56.87125,24.105]])
p=np.c_[(rd[:,0]-rd[:,0].mean())*np.cos(np.deg2rad(24.2)),rd[:,1]-rd[:,1].mean()]
D=np.linalg.norm(p[:,None]-p[None,:],axis=2);a,b=np.unravel_index(np.argmax(D),D.shape)
for N in (12,16,20,30,40,60,100):
 obs=obs_all[:N];tree=cKDTree(obs);u,v=np.where(~np.eye(N,dtype=bool));q=obs[v]-obs[u];ql=np.linalg.norm(q,axis=1);best=[]
 for refl in (False,True):
  pp=p.copy();pp[:,0]*=(-1 if refl else 1);dp=pp[b]-pp[a];ss=ql/np.linalg.norm(dp);keep=(ss>100)&(ss<3000);uu=u[keep];qq=q[keep];sc=ss[keep];ang=np.arctan2(qq[:,1],qq[:,0])-np.arctan2(dp[1],dp[0]);ca=np.cos(ang);sa=np.sin(ang);base=pp-pp[a]
  px=(base[:,0][None,:]*ca[:,None]-base[:,1][None,:]*sa[:,None])*sc[:,None]+obs[uu,0,None];py=(base[:,0][None,:]*sa[:,None]+base[:,1][None,:]*ca[:,None])*sc[:,None]+obs[uu,1,None];pred=np.stack([px,py],2);d,idx=tree.query(pred.reshape(-1,2));d=d.reshape(-1,9);idx=idx.reshape(-1,9)
  for ci in range(len(sc)):
   if len(set(idx[ci]))==9:best.append((np.sqrt(np.mean((d[ci]/sc[ci])**2)),refl,sc[ci],pred[ci],d[ci],idx[ci]))
 best.sort(key=lambda z:z[0]);z=best[0];print('\nN',N,'score refl scale',z[:3]);print(np.round(z[3],1));print('near',np.round(obs[z[5]],1));print('d',np.round(z[4],1));print('ranks',z[5]+1)
