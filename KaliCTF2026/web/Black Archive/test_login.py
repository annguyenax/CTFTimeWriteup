import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}

r = session.post(url_login, json=data, verify=False)
print("Login:", r.status_code, r.text)

url_me = "https://ctf.marabit.xyz/api/auth/me"
r2 = session.get(url_me, verify=False)
print("Me:", r2.status_code, r2.text)

url_docs = "https://ctf.marabit.xyz/api/documents"
r3 = session.get(url_docs, verify=False)
print("Docs:", r3.status_code, r3.text[:500])
