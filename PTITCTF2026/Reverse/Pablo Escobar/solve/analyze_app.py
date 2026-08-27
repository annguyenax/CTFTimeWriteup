import requests
import re
import os
import json

base_url = "http://144.79.188.36:6500"
os.makedirs("app_static", exist_ok=True)

# 1. Fetch HTML and JS files
r = requests.get(base_url)
with open("app_static/index.html", "w", encoding="utf-8") as f:
    f.write(r.text)

js_files = re.findall(r'(?:src|href)="(/_next/static/[^"]+\.js)"', r.text)
print("JS files found in HTML:", js_files)

all_text = ""
for js_path in set(js_files):
    res = requests.get(base_url + js_path)
    filename = js_path.replace("/", "_")
    with open(f"app_static/{filename}", "w", encoding="utf-8") as f:
        f.write(res.text)
    all_text += res.text
    print(f"Downloaded {js_path} ({len(res.content)} bytes)")

# Search for chunks referenced inside JS
chunks = re.findall(r'["\']([a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+\.js)["\']', all_text)
print("Additional chunk references:", set(chunks))

for c in set(chunks):
    for prefix in ["/_next/static/chunks/", "/_next/static/chunks/pages/", "/_next/static/chunks/app/"]:
        c_url = base_url + prefix + c
        res = requests.get(c_url)
        if res.status_code == 200 and "html" not in res.headers.get("Content-Type", ""):
            print(f"Found chunk {prefix + c} ({len(res.content)} bytes)")
            with open(f"app_static/{c}", "w", encoding="utf-8") as f:
                f.write(res.text)
            all_text += res.text

# Search for strings of interest
print("\n--- Strings of Interest ---")
print("Flags:", re.findall(r'PTITCTF\{[^}]*\}', all_text, re.IGNORECASE))
print("Endpoints:", set(re.findall(r'["\'](/api/[a-zA-Z0-9_/:-]+)["\']', all_text)))
print("Role references:", set(re.findall(r'["\'](admin|user|role|recipient|flycam|drone|location|delivery|warehouse)["\']', all_text, re.IGNORECASE)))
