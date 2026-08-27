import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('live_inbox/images_listing.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

images = data.get('images', [])
print(f"Total images: {len(images)}")

# Sort by ID
images_sorted = sorted(images, key=lambda x: x['id'])

print("\n--- Original / Notable Images ---")
for img in images_sorted:
    img_id = img['id']
    size = img.get('size', 0)
    created = img.get('createdAt', '')
    name = img.get('name', '')
    msg = img.get('message', '')
    url = img.get('url', '')
    # Check if size > 1000 or ID < 20 or interesting name
    print(f"[{img_id:3d}] ({size:7d} B) {created} | Name: {name} | Msg: {msg}")
