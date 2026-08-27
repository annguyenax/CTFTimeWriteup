import cv2, numpy as np, os, easyocr
base=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
m=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
u=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
reader=easyocr.Reader(['en'],gpu=False,model_storage_directory=m,user_network_directory=u,download_enabled=False)

for name in ['QF','SF','R16','R32','R3']:
    gray=cv2.imread(os.path.join(base,name+'.png'),cv2.IMREAD_GRAYSCALE)
    _,b=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # find dark text regions (labels are dark text on light bg after Otsu? check)
    # Determine text polarity
    darkpix=(b<128).sum(); lightpix=(b>128).sum()
    # assume text is minority polarity
    text_mask = b<128 if darkpix < lightpix else b>128
    text_mask = (text_mask*255).astype(np.uint8)
    n,lab,stats,cent=cv2.connectedComponentsWithStats(text_mask,8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,a=stats[i]
        if w<4 or h<4: continue
        if w>80 or h>80: continue
        comps.append((x,y,w,h,a,cent[i]))
    # group comps by row proximity into label clusters
    comps.sort(key=lambda c:(c[1]//40, c[0]))
    # OCR each component crop
    results=[]
    for (x,y,w,h,a,cc) in comps:
        pad=3
        crop=gray[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
        crop_up=cv2.resize(crop,None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC)
        txt=reader.recognize(crop_up)
        if txt:
            results.append((y+h/2, x+w/2, txt[0][1]))
    results.sort()
    print(f'=== {name} === (dark:{darkpix} light:{lightpix})')
    for y,x,t in results:
        print(f'  y={y:5.1f} x={x:5.1f}  {t}')
