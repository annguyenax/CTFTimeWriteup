import easyocr, os, cv2, json, sys
base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
model_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
user_net_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
outdir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_per_image'
os.makedirs(outdir, exist_ok=True)
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

name = sys.argv[1]
variant = sys.argv[2]
img = cv2.imread(os.path.join(base, name+'.png'))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
if variant == 'plain':
    proc = gray
elif variant == 'otsu':
    _, proc = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
elif variant == 'inv':
    proc = 255-gray
up = cv2.resize(proc, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
items = ocr_img(up, 2)
with open(os.path.join(outdir, f'{name}_{variant}.json'), 'w') as f:
    json.dump(items, f, indent=1)
print('DONE', name, variant)
