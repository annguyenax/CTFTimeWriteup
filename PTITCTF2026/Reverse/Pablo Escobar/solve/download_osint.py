import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0'}
urls = [
    'https://tuoitre.vn/pha-xuong-ma-tuy-khung-nhat-viet-nam-thu-14-tan-ketamin-20250326115315802.htm',
    'https://vietnamnet.vn/trung-tuong-nguyen-van-vien-tran-danh-sinh-tu-voi-toi-pham-ma-tuy-2403212.html',
    'https://tienphong.vn/dot-kich-xuong-san-xuat-ma-tuy-khung-nhat-viet-nam-thu-14-tan-ketamin-post1728258.tpo',
    'https://cand.com.vn/Phong-su-Tu-lieu/trung-tuong-nguyen-van-vien-cuc-truong-cuc-canh-sat-dieu-tra-toi-pham-ve-ma-tuy-gian-nan-nhung-vinh-quang-i771891/'
]

os.makedirs('osint_images', exist_ok=True)

all_imgs = []
for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10)
        found = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', r.text)
        print(f"URL: {u} -> found {len(found)} image links")
        for img_url in found:
            if any(k in img_url for k in ['ma-tuy', 'ketamin', 'nguyen-van-vien', '47900', '17429786']):
                all_imgs.append(img_url)
    except Exception as e:
        print(f"Error {u}: {e}")

print(f"\nFiltered candidate images ({len(all_imgs)}):")
for idx, img_url in enumerate(set(all_imgs)):
    print(f"[{idx}] {img_url}")
    try:
        r = requests.get(img_url, headers=headers, timeout=10)
        ext = img_url.split('.')[-1].split('?')[0]
        fn = f"osint_images/img_{idx}.{ext}"
        with open(fn, 'wb') as f:
            f.write(r.content)
        print(f"  -> Saved {fn} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"  -> Failed {img_url}: {e}")
