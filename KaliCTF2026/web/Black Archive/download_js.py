import requests

url = "https://ctf.marabit.xyz/assets/index-DAIoPkJd.js"
r = requests.get(url, verify=False)
with open("index.js", "wb") as f:
    f.write(r.content)
print("Saved index.js. Size:", len(r.content))
