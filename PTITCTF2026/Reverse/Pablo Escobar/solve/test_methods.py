import requests
import json

base = "http://144.79.188.36:6500"

print("--- 1. Inspecting Server Response Headers ---")
r = requests.get(base)
print("Home Headers:")
for k, v in r.headers.items():
    print(f"  {k}: {v}")

s = requests.Session()
r_login = s.post(f"{base}/api/session", json={"username": "luongvd", "password": "luongvd"})
print("\nSession Headers:")
for k, v in r_login.headers.items():
    print(f"  {k}: {v}")

r_img3 = s.get(f"{base}/api/images/3")
print(f"\nGET /api/images/3 -> Status: {r_img3.status_code}")
for k, v in r_img3.headers.items():
    print(f"  {k}: {v}")
print(f"Body: {r_img3.text}")

print("\n--- 2. Testing HTTP Methods on /api/images/3 ---")
for method in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE", "CONNECT"]:
    try:
        res = s.request(method, f"{base}/api/images/3")
        print(f"Method {method:7s} -> {res.status_code} | {res.text[:100]}")
    except Exception as e:
        print(f"Method {method:7s} -> Error: {e}")

print("\n--- 3. Testing Range Requests & Cache Headers ---")
range_headers = [
    {"Range": "bytes=0-100"},
    {"Range": "bytes=0-"},
    {"Range": "bytes=-100"},
    {"If-Range": "*"},
    {"If-Match": "*"},
    {"If-None-Match": "*"},
]
for h in range_headers:
    res = s.get(f"{base}/api/images/3", headers=h)
    print(f"Header {h} -> Status {res.status_code} | Len: {len(res.content)}")
