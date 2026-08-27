import requests

session = requests.Session()
url_login = "https://ctf.marabit.xyz/api/auth/login"
data = {"email": "analyst@blackarchive.local", "password": "ArchiveAccess2026!"}
session.post(url_login, json=data, verify=False)

url_overview = "https://ctf.marabit.xyz/api/admin/overview"
r = session.get(url_overview, verify=False)
print("Overview:", r.status_code, r.text)

url_import = "https://ctf.marabit.xyz/api/admin/yaml/import"
r2 = session.post(url_import, json={"yaml": "test"}, verify=False)
print("Import:", r2.status_code, r2.text)
