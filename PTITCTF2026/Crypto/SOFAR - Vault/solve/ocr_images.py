import easyocr, glob, os, sys, json

base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
model_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_models'
user_net_dir = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_user_net'
os.makedirs(model_dir, exist_ok=True)
os.makedirs(user_net_dir, exist_ok=True)

reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir,
                        user_network_directory=user_net_dir, download_enabled=True)

files = sorted(glob.glob(os.path.join(base, '*.png')))
results = {}
for p in files:
    name = os.path.basename(p)
    try:
        out = reader.readtext(p, detail=1, paragraph=False)
        # collect lines sorted by vertical position
        lines = []
        for (bbox, text, conf) in out:
            y = bbox[0][1]
            lines.append((y, text, round(float(conf), 3)))
        lines.sort()
        results[name] = lines
        print(f'=== {name} ===')
        for y, t, c in lines:
            print(f'  [{y:4d}] ({c}) {t}')
    except Exception as e:
        print(f'=== {name} ERROR: {e}')
    sys.stdout.flush()

with open(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\ocr_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print('DONE')
