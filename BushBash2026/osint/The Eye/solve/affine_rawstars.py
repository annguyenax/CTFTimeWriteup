import contextlib, io, itertools, sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

im=cv2.imread("dots.png"); b,g,r=cv2.split(im)
red=(r>90)&(r>g*1.35)&(r>b*1.35)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"),np.ones((7,7),np.uint8))>0]=0
n,lab,stats,_=cv2.connectedComponentsWithStats((gray>15).astype("uint8"))
flat=lab.ravel(); wt=gray.ravel().astype(float); yy,xx=np.indices(gray.shape)
flux=np.bincount(flat,weights=wt,minlength=n)
sx=np.bincount(flat,weights=wt*xx.ravel(),minlength=n); sy=np.bincount(flat,weights=wt*yy.ravel(),minlength=n)
valid=np.array([i for i in range(1,n) if stats[i,4]>=2 and flux[i]>0])
valid=valid[np.argsort(flux[valid])[::-1]]
stars=np.array([[sx[i]/flux[i],sy[i]/flux[i]] for i in valid])
tree=cKDTree(stars)
words=np.array([[w[0],w[1]] for w in oc.words]); wtree=cKDTree(words)

radec=np.array([
[56.4567958643,24.3675414247],[56.3021628561,24.4670639573],[56.477085,24.554305],
[56.200992,24.289268],[57.296831,24.136498],[56.5816714492,23.9481438102],
[56.2190045645,24.1131330436],[57.2906889329,24.0532118300],[56.8712508473,24.1049344752]])
p=np.c_[(radec[:,0]-56.7)*np.cos(np.deg2rad(24.2)),radec[:,1]-24.2]
anchors=(2,6,7); base=np.c_[p[list(anchors)],np.ones(3)]
bary=np.c_[p,np.ones(9)]@np.linalg.inv(base)
src_edges=np.stack([p[anchors[1]]-p[anchors[0]],p[anchors[2]]-p[anchors[0]]],axis=1)
inv_src=np.linalg.inv(src_edges)
ciphertext=open("prayer.enc","rb").read(); best=[]; seen=set()

def process(rows):
    ids=np.asarray(rows,int); q=stars[ids]
    pred=np.einsum("ij,njk->nik",bary,q)
    dist,ind=tree.query(pred.reshape(-1,2)); dist=dist.reshape(-1,9); ind=ind.reshape(-1,9)
    dst_edges=np.stack([q[:,1]-q[:,0],q[:,2]-q[:,0]],axis=2); mats=dst_edges@inv_src
    sv=np.linalg.svd(mats,compute_uv=False); ratio=sv[:,0]/np.maximum(sv[:,1],1e-9); scale=np.sqrt(sv[:,0]*sv[:,1])
    rms=np.sqrt(np.mean(dist*dist,axis=1)); uniq=np.array([len(set(x))==9 for x in ind])
    keep=uniq&(ratio<3)&(scale>50)&(scale<1000)&(rms<12)
    for k in np.flatnonzero(keep):
        sig=tuple(ind[k]);
        if sig in seen: continue
        seen.add(sig)
        # Key labels should occur directly below the matched stars.
        wd,wi=wtree.query(stars[ind[k,:8]]+[0,18])
        codes=[oc.codes[int(x)] for x in wi]
        if max(wd)<55 and all(codes):
            key="".join(codes)
            try:
                plain=unpad(AES.new(bytes.fromhex(key),AES.MODE_ECB).decrypt(ciphertext),16)
                printable=sum(c in b"\r\n\t" or 32<=c<127 for c in plain)/len(plain)
                if b"bushbash{" in plain.lower() or printable>.85:
                    print("AES HIT",key,repr(plain),"ranks",(ind[k]+1).tolist(),"codes",codes,"wd",wd.tolist())
            except ValueError: pass
        best.append((float(rms[k]),float(ratio[k]),float(scale[k]),ind[k].copy(),dist[k].copy(),wi.copy(),wd.copy(),codes))

batch=[]
for row in itertools.permutations(range(80),3):
    batch.append(row)
    if len(batch)==20000: process(batch); batch=[]
process(batch); best.sort(key=lambda z:(z[0],z[1]))
print("candidates",len(seen))
for z in best[:80]:
    rms,ratio,scale,ind,dist,wi,wd,codes=z
    print("C",rms,ratio,scale,"ranks",(ind+1).tolist(),"d",np.round(dist,2).tolist(),"words",wi.tolist(),codes,"wd",np.round(wd,2).tolist())
