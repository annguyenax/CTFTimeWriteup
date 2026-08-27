#!/usr/bin/env python3
"""Log in as luongvd/luongvd and download inbox images."""
from __future__ import annotations

import argparse
import json
import urllib.request
import http.cookiejar
from pathlib import Path

DEFAULT_BASE = "http://144.79.188.36:6500"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--user", default="luongvd")
    ap.add_argument("--password", default="luongvd")
    ap.add_argument("--out", type=Path, default=Path("inbox"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request(
        args.base + "/api/session",
        data=json.dumps({"username": args.user, "password": args.password}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener.open(req, timeout=20) as r:
        print("login", r.read().decode())

    with opener.open(args.base + "/api/images", timeout=20) as r:
        listing = json.loads(r.read())
    (args.out / "images.json").write_text(
        json.dumps(listing, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(listing, indent=2, ensure_ascii=False))

    for img in listing.get("images", []):
        dest = args.out / f"{img['id']}_{img['name']}"
        with opener.open(args.base + img["url"], timeout=60) as r:
            dest.write_bytes(r.read())
        print("saved", dest, "msg=", img.get("message"))


if __name__ == "__main__":
    main()
