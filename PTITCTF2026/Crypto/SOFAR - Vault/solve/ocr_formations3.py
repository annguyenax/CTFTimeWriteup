import easyocr, os, sys, cv2, numpy as np
base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
m=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
u=r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
reader=easyocr.Reader(['en'],gpu=False,model_storage_directory=m,user_network_directory=u,download_enabled=False)

def ocr(img):
    out=reader.readtext(img,detail=1,paragraph=False)
    items=[]
    for (bb,t,c) in out:
        xs=[p[0] for p in bb]; ys=[p[1] for p in bb]
        items.append((sum(ys)/4,sum(xs)/4,t,round(float(c),2)))
    return items

for name in ['F','QF','SF','R1','R2','R3','R16','R32']:
    img=cv2.imread(os.path.join(base,name+'.png'))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # upscale 2.5x
    up=cv2.resize(gray,None,fx=2.5,fy=2.5,interpolation=cv2.INTER_CUBIC)
    items=ocr(up)
    items=[(y/2.5,x/2.5,t,c) for (y,x,t,c) in items]
    items.sort()
    print(f'=== {name} ===')
    for y,x,t,c in items:
        print(f'  y={y:5.1f} x={x:5.1f}  {t}  ({c})')
    sys.stdout.flush()
