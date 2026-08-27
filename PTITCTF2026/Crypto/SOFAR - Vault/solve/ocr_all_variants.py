import easyocr, os, cv2, json, sys
base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
model_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
user_net_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir, user_network_directory=user_net_dir, download_enabled=False)

def ocr_img(img, scale):
    out = reader.readtext(img, detail=1, paragraph=False)
    items=[]
    for (bbox, text, conf) in out:
        xs=[pt[0] for pt in bbox]; ys=[pt[1] for pt in bbox]
        cx=sum(xs)/4/scale; cy=sum(ys)/4/scale
        items.append((round(cy),round(cx),text,round(float(conf),2)))
    items.sort()
    return items

results = {}
for name in ['F','QF','SF','R1','R2','R3','R16','R32']:
    img = cv2.imread(os.path.join(base, name+'.png'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants = {}
    up = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    variants['plain2x'] = ocr_img(up, 2)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    up2 = cv2.resize(th, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    variants['otsu2x'] = ocr_img(up2, 2)
    ad = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 15)
    up3 = cv2.resize(ad, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    variants['adaptive2x'] = ocr_img(up3, 2)
    inv = 255-gray
    up4 = cv2.resize(inv, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    variants['inv2x'] = ocr_img(up4, 2)
    results[name] = variants

with open(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_all_variants.json','w') as f:
    json.dump(results, f, indent=1)
for name, variants in results.items():
    print('='*20, name)
    for vname, items in variants.items():
        for (cy,cx,t,c) in items:
            print(f'  [{vname}] y={cy:4d} x={cx:4d}  {t!r} ({c})')
    sys.stdout.flush()
