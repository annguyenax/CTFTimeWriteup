import contextlib,io,sys
import cv2,numpy as np
from scipy.spatial import cKDTree
with contextlib.redirect_stdout(io.StringIO()):
 sys.path.insert(0,'../the-eye'); import ocr_codes as oc
im=cv2.imread('dots.png');b,g,r=cv2.split(im);red=(r>90)&(r>g*1.35)&(r>b*1.35)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);gray[cv2.dilate(red.astype('uint8'),np.ones((7,7),np.uint8))>0]=0
n,L,S,_=cv2.connectedComponentsWithStats((gray>15).astype('uint8'));f=L.ravel();w=gray.ravel().astype(float);yy,xx=np.indices(gray.shape)
flux=np.bincount(f,weights=w,minlength=n);sx=np.bincount(f,weights=w*xx.ravel(),minlength=n);sy=np.bincount(f,weights=w*yy.ravel(),minlength=n)
v=np.array([i for i in range(1,n) if S[i,4]>=3 and flux[i]>0]);v=v[np.argsort(flux[v])[::-1]]
stars=np.array([[sx[i]/flux[i],sy[i]/flux[i]] for i in v]); words=np.array([[x[0],x[1]] for x in oc.words]);tree=cKDTree(words)
ranks=np.array([159,18,35,151,166,179,165,19,167])-1
for name,rank in zip(['Maia','Taygeta','Asterope','Celaeno','Pleione','Merope','Electra','Atlas','Alcyone'],ranks):
 p=stars[rank]; d,idx=tree.query(p+[0,18],k=10)
 print(name,'rank',rank+1,'star',p.tolist())
 for dd,i in zip(d,idx): print(' ',int(i),oc.codes[int(i)],words[int(i)].tolist(),round(float(dd),2))
