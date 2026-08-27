import requests

url = "https://ctf.marabit.xyz/login"
r = requests.get(url, verify=False)
print("Status:", r.status_code)
print("Headers:", r.headers)
print("Content:", r.text[:1000])
