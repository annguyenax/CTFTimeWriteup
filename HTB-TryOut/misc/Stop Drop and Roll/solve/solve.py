#!/usr/bin/env python3
"""Stop Drop and Roll (HTB TryOut, misc, very easy)

GORGE -> STOP, PHREAK -> DROP, FIRE -> ROLL.
Comma-separated scenarios; hyphen-separated replies.
"""
import socket, re, sys

MAP = {"GORGE": "STOP", "PHREAK": "DROP", "FIRE": "ROLL"}

def recv_until(s, needle, limit=16384):
    buf = b""
    while needle not in buf and len(buf) < limit:
        d = s.recv(4096)
        if not d:
            break
        buf += d
    return buf

def parse_scenario(blob):
    text = blob.decode("latin1", "replace")
    # only consider lines after the game actually starts
    if "Ok then" in text:
        text = text.split("Ok then", 1)[1]
    lines = [ln.strip() for ln in text.replace("\r", "").split("\n") if ln.strip()]
    for ln in reversed(lines):
        if ln.startswith("What do you do"):
            continue
        toks = [t.strip() for t in ln.replace("!", "").split(",")]
        if toks and all(t in MAP for t in toks):
            return toks
    return None

def solve(host, port):
    s = socket.create_connection((host, port), timeout=10)
    s.settimeout(6)
    recv_until(s, b"(y/n)")
    s.sendall(b"y\n")
    acc = b""
    flag = None
    for rnd in range(520):
        chunk = b""
        while b"What do you do?" not in chunk and b"HTB{" not in chunk and len(chunk) < 8192:
            d = s.recv(4096)
            if not d:
                break
            chunk += d
        acc += chunk
        if b"HTB{" in acc:
            break
        if not chunk:
            break
        scen = parse_scenario(chunk)
        if not scen:
            print("NO PARSE round", rnd, chunk[-300:])
            break
        reply = "-".join(MAP[t] for t in scen)
        s.sendall((reply + "\n").encode())
    text = acc.decode("latin1", "replace")
    print(text[-1000:])
    m = re.search(r"HTB\{[^}]*\}", text)
    if m:
        flag = m.group(0)
        open("final_flag.txt", "w").write(flag + "\n")
        print("FLAG:", flag)
    return flag

if __name__ == "__main__":
    h, p = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.82", 31142)
    solve(h, p)
