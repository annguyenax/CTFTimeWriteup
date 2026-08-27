import cv2, numpy as np, os, easyocr
base=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
m=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
u=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
reader=easyocr.Reader(['en'],gpu=False,model_storage_directory=m,user_network_directory=u,download_enabled=False)

for name in ['F','QF','SF','R1','R2','R3','R16','R32']:
    gray=cv2.imread(os.path.join(base,name+'.png'),cv2.IMREAD_GRAYSCALE)
    _,b=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    darkpix=(b<128).sum(); lightpix=(b>128).sum()
    text_mask = (b<128) if darkpix<lightpix else (b>128)
    tm=text_mask.astype(np.uint8)*255
    # dilate to merge letters of a label
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(9,5))
    dm=cv2.dilate(tm,kernel)
    n,lab,stats,cent=cv2.connectedComponentsWithStats(dm,8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,a=stats[i]
        if a<30: continue
        comps.append((x,y,w,h,cent[i]))
    comps.sort(key=lambda c:(round(c[1],-1), c[0]))
    results=[]
    for (x,y,w,h,cc) in comps:
        pad=2
        crop=gray[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
        cu=cv2.resize(crop,None,fx=4,fy=4,interpolation=cv2.INTER_CUBIC)
        txt=reader.recognize(cu)
        if txt:
            t=txt[0][1]
            results.append((y+h/2, x+w/2, t, a))
    results.sort()
    print(f'=== {name} === count={len(results)}')
    for y,x,t,a in results:
        print(f'  y={y:5.1f} x={x:5.1f} a={a:5d}  {t}')
