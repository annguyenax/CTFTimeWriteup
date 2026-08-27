import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

urls = [
    "https://ctf.marabit.xyz/api/documents/17/download",
    "https://ctf.marabit.xyz/api/documents/17/file",
    "https://ctf.marabit.xyz/api/documents/17/content"
]
for u in urls:
    r = session.get(u, verify=False)
    print(u, r.status_code, r.text[:200])
