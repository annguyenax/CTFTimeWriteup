import cv2, numpy as np
from scipy.spatial import cKDTree
import contextlib,io
with contextlib.redirect_stdout(io.StringIO()): import ocr_codes as oc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

im=cv2.imread('dots.png'); b0,g0,r0=cv2.split(im)
red=(r0>90)&(r0>g0*1.35)&(r0>b0*1.35)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype('uint8'),np.ones((7,7),np.uint8))>0]=0
n,lab,st,cen=cv2.connectedComponentsWithStats((gray>15).astype('uint8'))
obs=[]
for i in range(1,n):
    if st[i,4]>=4:
        ys,xs=np.where(lab==i); wt=gray[ys,xs].astype(float)
        obs.append([(xs*wt).sum()/wt.sum(),(ys*wt).sum()/wt.sum()])
obs=np.array(obs); tree=cKDTree(obs)
wordxy=np.array([[w[0],w[1]-17] for w in oc.words]);wtree=cKDTree(wordxy);ciphertext=open('prayer.enc','rb').read()
rd=np.array([[56.4567,24.3678],[56.3021,24.4672],[56.4771,24.5547],[56.2008,24.2894],[57.2967,24.1367],[56.5817,23.9483],[56.21875,24.1133],[57.2904,24.0533],[56.87125,24.105]])
p=np.c_[(rd[:,0]-rd[:,0].mean())*np.cos(np.deg2rad(24.2)),rd[:,1]-rd[:,1].mean()]
D=np.linalg.norm(p[:,None]-p[None,:],axis=2); a,b=np.unravel_index(np.argmax(D),D.shape)
u,v=np.where(~np.eye(len(obs),dtype=bool)); q=obs[v]-obs[u]; qlen=np.linalg.norm(q,axis=1)
out=[]
for refl in (False,True):
    pp=p.copy(); pp[:,0]*=(-1 if refl else 1); dp=pp[b]-pp[a]
    scales=qlen/np.linalg.norm(dp); keep=(scales>20)&(scales<1000)
    uu=u[keep]; ss=scales[keep]; qq=q[keep]
    ang=np.arctan2(qq[:,1],qq[:,0])-np.arctan2(dp[1],dp[0]); ca=np.cos(ang);sa=np.sin(ang);base=pp-pp[a]
    px=(base[:,0][None,:]*ca[:,None]-base[:,1][None,:]*sa[:,None])*ss[:,None]+obs[uu,0,None]
    py=(base[:,0][None,:]*sa[:,None]+base[:,1][None,:]*ca[:,None])*ss[:,None]+obs[uu,1,None]
    pred=np.stack([px,py],2); d,idx=tree.query(pred.reshape(-1,2));d=d.reshape(-1,9);idx=idx.reshape(-1,9)
    tol=np.full_like(ss,5.0)
    counts=(d<tol[:,None]).sum(1)
    wd,wi=wtree.query(pred.reshape(-1,2));wd=wd.reshape(-1,9);wi=wi.reshape(-1,9)
    for ci in np.flatnonzero(counts>=5):
        hit=idx[ci,d[ci]<tol[ci]]
        if len(set(wi[ci,:8]))<8 or np.max(wd[ci,:8])>35: continue
        cs=[oc.codes[j] for j in wi[ci,:8]]
        try:
            plain=unpad(AES.new(bytes.fromhex(''.join(cs)),AES.MODE_ECB).decrypt(ciphertext),16)
            pr=sum(x in b'\n\r\t' or 32<=x<127 for x in plain)/len(plain)
            if pr>.8: print('REAL HIT',''.join(cs),plain,'scale',ss[ci],'refl',refl,'wd',wd[ci,:8])
        except ValueError: pass
        out.append((int(counts[ci]),len(set(hit)),float(np.sum(np.minimum(d[ci]/ss[ci],.2))),refl,float(ss[ci]),pred[ci],d[ci],idx[ci]))
out.sort(key=lambda z:(-z[0],-z[1],z[2]))
for z in out[:30]:
    print('\ncount unique cost reflection scale',z[:5])
    print('pred',np.round(z[5],1).tolist())
    print('near',np.round(obs[z[7]],1).tolist())
    print('dist',np.round(z[6],2).tolist())
