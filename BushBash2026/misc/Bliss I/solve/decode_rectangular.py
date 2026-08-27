#!/usr/bin/env python3
"""Recover the cloud as a 16x48 rectangular Data Matrix."""

import cv2
import numpy as np
import zxingcpp
from scipy.optimize import minimize

IMAGE=r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"
ROWS,COLS=16,48

def main():
    im=cv2.imread(IMAGE)
    sat=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)[:,:,1].astype(float)
    known=np.zeros((ROWS,COLS),bool); black=np.zeros((ROWS,COLS),bool)
    known[0,:]=known[-1,:]=known[:,0]=known[:,-1]=True
    black[0,:]=np.arange(COLS)%2==0;black[-1,:]=True;black[:,0]=True
    black[:,-1]=np.arange(ROWS)%2==1
    rr,cc=np.nonzero(known)
    target=np.where(black[rr,cc],-1.,1.);target-=target.mean();target/=np.linalg.norm(target)
    rng=np.random.default_rng(20260801); total=1_000_000
    params=np.column_stack((
        rng.uniform(930,1030,total),rng.uniform(690,800,total),
        rng.uniform(7,13,total),rng.uniform(-1.5,2,total),
        rng.uniform(-3,1.5,total),rng.uniform(12,20,total),
        rng.uniform(-.025,.025,total),rng.uniform(-.08,.08,total)))
    best=[]
    for start in range(0,total,2000):
        p=params[start:start+2000]
        x=np.rint(p[:,0,None]+cc*p[:,2,None]+rr*p[:,4,None]+cc*rr*p[:,6,None]).astype(int)
        y=np.rint(p[:,1,None]+cc*p[:,3,None]+rr*p[:,5,None]+cc*rr*p[:,7,None]).astype(int)
        v=sat[y,x];v-=v.mean(axis=1,keepdims=True);v/=np.sqrt((v*v).sum(axis=1,keepdims=True)+1e-9)
        score=v@target; ix=np.argpartition(score,-30)[-30:]
        best.extend((float(score[i]),p[i].copy()) for i in ix)
    best.sort(key=lambda x:x[0],reverse=True)

    sat32=sat.astype(np.float32)
    def objective(p):
        x=p[0]+cc*p[2]+rr*p[4]+cc*rr*p[6]
        y=p[1]+cc*p[3]+rr*p[5]+cc*rr*p[7]
        v=cv2.remap(sat32,x.astype(np.float32)[None,:],y.astype(np.float32)[None,:],cv2.INTER_LINEAR).ravel()
        v-=v.mean();v/=np.linalg.norm(v)+1e-9
        return -float(v@target)
    refined=[]
    for _,seed in best[:12]:
        res=minimize(objective,seed,method='Nelder-Mead',options={'maxiter':5000,'xatol':1e-4,'fatol':1e-8})
        refined.append((-float(res.fun),res.x))
    best=sorted(best+refined,key=lambda x:x[0],reverse=True)
    print('border',best[0][0],best[0][1])

    gr,gc=np.indices((ROWS,COLS))
    for rank,(score,p) in enumerate(best[:150]):
        samples=[]
        for dr in (-.3,0,.3):
            for dc in (-.3,0,.3):
                r=gr+dr;c=gc+dc
                x=p[0]+c*p[2]+r*p[4]+c*r*p[6]
                y=p[1]+c*p[3]+r*p[5]+c*r*p[7]
                samples.append(cv2.remap(sat32,x.astype(np.float32),y.astype(np.float32),cv2.INTER_LINEAR))
        raw=np.mean(samples,axis=0)
        threshold0,_=cv2.threshold(raw.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        for threshold in np.linspace(max(5,threshold0-45),min(230,threshold0+45),91):
            modules=raw<threshold;modules[known]=black[known]
            out=np.where(modules,0,255).astype(np.uint8)
            out=cv2.copyMakeBorder(cv2.resize(out,None,fx=12,fy=12,interpolation=cv2.INTER_NEAREST),24,24,24,24,cv2.BORDER_CONSTANT,value=255)
            result=zxingcpp.read_barcode(out)
            if result and result.text:
                print('DECODE',rank,score,threshold,repr(result.text))
                cv2.imwrite(r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\solve\recovered_rectangular.png",out)
                return
    print('No decode')

if __name__=='__main__':main()
