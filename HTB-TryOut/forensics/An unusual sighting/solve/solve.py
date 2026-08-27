#!/usr/bin/env python3
"""
Solver for HTB TryOut forensics "An unusual sighting".

Evidence model:
  - sshd.log        : every successful SSH login (time, user, src_ip, port).
  - bash_history.txt: shell commands with timestamps (root's history).

Identification of the perpetrator (evidence chain):
  1. The bash history contains ONE block of clearly malicious commands
     (2024-02-19 04:00:18 -> 04:14:02): recon (whoami/uname/cat /etc/passwd
     /cat /etc/shadow/ps faux), download from a typosquatted domain
     (gnu-packages.com, impersonating gnu.org), shred -zu (evidence
     destruction) and ./setup (dropper execution).
  2. The ONLY SSH session that covers that exact time window is
     [2024-02-19 04:00:14] "Accepted password for root from 2.67.182.119
     port 60071" (session ended 04:38:17). No other session overlaps.
  3. 2.67.182.119 is the only source logging in as root outside the legit
     Feb-13 provisioning session, at an odd hour (04:00), with its own
     unique SSH key fingerprint (OPkBSs6okUKraq8pYo4XwwBg55QSo210F09FCe1-yj4).

Conclusion: perpetrator = 2.67.182.119  ->  HTB{2.67.182.119}
"""
import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "files" / "_work" / "forensics_an_unusual_sighting"
SSHD = BASE / "sshd.log"
BASH = BASE / "bash_history.txt"

TS = "%Y-%m-%d %H:%M:%S"

# Signatures of attacker activity inside the bash history
MALICIOUS = re.compile(
    r"(cat /etc/shadow|/etc/passwd|gnu-packages\.com|shred -zu|whoami|ps faux|uname -a)",
    re.IGNORECASE,
)


def parse_sshd(path: Path):
    """Return (ts, user, src_ip, port) for successful logins and (start,end,ip) sessions."""
    logins, sessions = [], []
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\[([^\]]+)\] Accepted password for (\S+) from ([0-9.]+) port (\d+) ssh2", line)
        if m:
            logins.append((m.group(1), m.group(2), m.group(3), m.group(4)))
            cur = (datetime.strptime(m.group(1), TS), m.group(3))
        m = re.match(r"\[([^\]]+)\] Disconnected from user \S+ ([0-9.]+) port \d+", line)
        if m and cur:
            sessions.append((cur[0], datetime.strptime(m.group(1), TS), cur[1]))
            cur = None
    return logins, sessions


def parse_bash(path: Path):
    return [
        (datetime.strptime(m.group(1), TS), m.group(2))
        for m in (re.match(r"\[([^\]]+)\] (.*)", l) for l in path.read_text(encoding="utf-8").splitlines())
        if m
    ]


def main():
    logins, sessions = parse_sshd(SSHD)
    history = parse_bash(BASH)

    # 1) Find the malicious command block in bash history
    bad = [(ts, cmd) for ts, cmd in history if MALICIOUS.search(cmd)]
    print("== Malicious-looking bash history entries ==")
    for ts, cmd in bad:
        print(f"  [{ts.strftime(TS)}] {cmd}")

    # 2) Which SSH session covers those timestamps?
    lo = min(ts for ts, _ in bad)
    hi = max(ts for ts, _ in bad)
    print(f"\nMalicious block window: {lo} .. {hi}")

    print("\n== SSH sessions overlapping that window ==")
    suspects = set()
    for start, end, ip in sessions:
        if start <= hi and end >= lo:
            print(f"  {start} .. {end}  ip={ip}")
            suspects.add(ip)

    # 3) Cross-check: the accepted login for the attacker session
    print("\n== Successful logins == (context for all sessions)")
    for ts, user, ip, port in logins:
        print(f"  {ts}  {user:8s} {ip:>15s}:{port}")

    if len(suspects) == 1:
        flag = f"HTB{{{suspects.pop()}}}"
        print(f"\nFLAG: {flag}")
    else:
        print("\nAmbiguous; review manually.")


if __name__ == "__main__":
    main()
