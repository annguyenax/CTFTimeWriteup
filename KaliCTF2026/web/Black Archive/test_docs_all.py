import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

url_docs = "https://ctf.marabit.xyz/api/documents"
r = session.get(url_docs, verify=False)
print(r.text)
