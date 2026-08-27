import easyocr, glob, os, sys, cv2
base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
model_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
user_net_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir, user_network_directory=user_net_dir, download_enabled=False)
for name in ['F','QF','SF','R1','R2','R3','R16','R32']:
    img = cv2.imread(os.path.join(base, name+'.png'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # upscale 2x
    up = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    out = reader.readtext(up, detail=1, paragraph=False)
    items=[]
    for (bbox, text, conf) in out:
        xs=[pt[0] for pt in bbox]; ys=[pt[1] for pt in bbox]
        cx=sum(xs)/4/2; cy=sum(ys)/4/2  # divide by scale
        items.append((round(cy),round(cx),text,round(float(conf),2)))
    items.sort()
    print(f'=== {name}.png ===')
    for cy,cx,t,c in items:
        print(f'  y={cy:4d} x={cx:4d}  {t}  ({c})')
    sys.stdout.flush()
