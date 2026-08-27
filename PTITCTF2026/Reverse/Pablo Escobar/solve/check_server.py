import requests
import json
import os

s = requests.Session()
r_login = s.post('http://144.79.188.36:6500/api/session', json={'username': 'luongvd', 'password': 'luongvd'})
print('Login status:', r_login.status_code, r_login.text)

r_images = s.get('http://144.79.188.36:6500/api/images')
print('Images status:', r_images.status_code)
data = r_images.json()

os.makedirs('live_inbox', exist_ok=True)
with open('live_inbox/images_listing.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Total images listed: {len(data.get('images', []))}")
for img in data.get('images', []):
    img_id = img.get('id')
    name = img.get('name')
    msg = img.get('message')
    created = img.get('createdAt')
    url = img.get('url')
    print(f"ID: {img_id} | Created: {created} | Name: {name} | Msg: {msg}")
    
    # Download image
    r_file = s.get(f"http://144.79.188.36:6500{url}")
    if r_file.status_code == 200:
        filename = f"live_inbox/{img_id}_{name}"
        with open(filename, 'wb') as f:
            f.write(r_file.content)
        print(f"  -> Saved {filename} ({len(r_file.content)} bytes)")
    else:
        print(f"  -> Failed to download: {r_file.status_code} {r_file.text}")

print("\n--- Probing direct ID access from 1 to 20 ---")
for i in range(1, 20):
    r_direct = s.get(f"http://144.79.188.36:6500/api/images/{i}")
    print(f"GET /api/images/{i} -> Status: {r_direct.status_code}, Length: {len(r_direct.content)}")
    if r_direct.status_code == 200 and len(r_direct.content) > 100:
        with open(f"live_inbox/direct_{i}.jpg", "wb") as f:
            f.write(r_direct.content)
