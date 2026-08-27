#!/usr/bin/env python3
"""Rank 16x48 Data Matrix URL candidates against the cloud pixels."""

import cv2
import numpy as np
import zxingcpp

IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"
CANDIDATES = [
    "https://bushbash.cssa.club/atmospherically-questionable-runes",
    "http://bushbash.cssa.club/atmospherically-questionable-runes",
    "https://bushbash.cssa.club/atmospherically-questionable-runes/",
    "https://bushbash.cssa.club/this-is-a-completely-random-route-name",
    "https://bushbash.cssa.club/never-trust-a-random-cloud-barcode",
]


def encode(text):
    b = zxingcpp.create_barcode(text, zxingcpp.BarcodeFormat.DataMatrix)
    a = np.asarray(zxingcpp.write_barcode_to_image(b, 1, False, False)) < 128
    return a


def main():
    im=cv2.imread(IMAGE)
    sat=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)[:,:,1].astype(float)
    encoded=[]
    for text in CANDIDATES:
        a=encode(text)
        print('shape',a.shape,text)
        if a.shape==(16,48):
            encoded.append((text,[a,np.flipud(a),np.fliplr(a),np.flip(a)]))
    rng=np.random.default_rng(20260801)
    total=200_000
    p=np.column_stack((
        rng.uniform(930,1030,total),rng.uniform(690,800,total),
        rng.uniform(7,13,total),rng.uniform(-1.5,2,total),
        rng.uniform(-3,1.5,total),rng.uniform(12,20,total),
        rng.uniform(-.025,.025,total),rng.uniform(-.08,.08,total)))
    rr,cc=np.indices((16,48));rr=rr.ravel();cc=cc.ravel()
    scores={t:-1.0 for t,_ in encoded}
    for start in range(0,total,1000):
        q=p[start:start+1000]
        x=np.rint(q[:,0,None]+cc*q[:,2,None]+rr*q[:,4,None]+cc*rr*q[:,6,None]).astype(int)
        y=np.rint(q[:,1,None]+cc*q[:,3,None]+rr*q[:,5,None]+cc*rr*q[:,7,None]).astype(int)
        values=sat[y,x];values-=values.mean(axis=1,keepdims=True)
        values/=np.sqrt((values*values).sum(axis=1,keepdims=True)+1e-9)
        for text,pats in encoded:
            scores[text]=max(scores[text],max(float(np.abs(values@np.where(a.ravel(),1.,-1.)/np.sqrt(a.size)).max()) for a in pats))
    print('RANKING')
    for text,score in sorted(scores.items(),key=lambda x:x[1],reverse=True):
        print(f'{score:.6f}',text)

if __name__=='__main__':main()
