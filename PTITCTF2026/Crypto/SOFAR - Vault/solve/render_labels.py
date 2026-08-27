import cv2, numpy as np, os
base=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
# For each formation, detect label components (dilated) and render each crop natively as ASCII
for name in ['QF','SF','R16']:
    gray=cv2.imread(os.path.join(base,name+'.png'),cv2.IMREAD_GRAYSCALE)
    _,b=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    darkpix=(b<128).sum(); lightpix=(b>128).sum()
    tm = (b<128) if darkpix<lightpix else (b>128)
    tm=(tm*255).astype(np.uint8)
    k=cv2.getStructuringElement(cv2.MORPH_RECT,(7,5))
    dm=cv2.dilate(tm,k)
    n,lab,stats,cent=cv2.connectedComponentsWithStats(dm,8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,a=stats[i]
        if a<40: continue
        comps.append((x,y,w,h,a))
    comps.sort(key=lambda c:(c[1]//40, c[0]))
    print(f'==== {name} ==== {len(comps)} components')
    for (x,y,w,h,a) in comps:
        pad=1
        reg=gray[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
        # render as ascii (upscale 2x for readability)
        print(f'--- y={y}..{y+h} x={x}..{x+w} ---')
        for r in range(reg.shape[0]):
            line=''.join('@' if reg[r,c]<128 else '.' for c in range(reg.shape[1]))
            print('  '+line)
    print()
