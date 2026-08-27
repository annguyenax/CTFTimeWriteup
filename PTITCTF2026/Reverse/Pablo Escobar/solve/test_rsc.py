import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

base = "http://144.79.188.36:6500"

s = requests.Session()
s.post(f"{base}/api/session", json={"username": "luongvd", "password": "luongvd"})

print("--- 1. Testing RSC Headers on GET / ---")
rsc_headers = {
    "RSC": "1",
    "Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(main)%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
    "Next-Url": "/",
}

r_rsc = s.get(base, headers=rsc_headers)
print("RSC Status:", r_rsc.status_code)
print("RSC Preview:\n", r_rsc.text[:1000])

with open("rsc_response.txt", "w", encoding="utf-8") as f:
    f.write(r_rsc.text)

print("\n--- 2. Testing RSC on /api/images/3 ---")
r_rsc_3 = s.get(f"{base}/api/images/3", headers=rsc_headers)
print("RSC Image 3 Status:", r_rsc_3.status_code, "Body:", r_rsc_3.text)
