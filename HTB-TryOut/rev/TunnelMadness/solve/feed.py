#!/usr/bin/env python3
# Feed the verified 59-move maze key to the live TunnelMadness service and print the flag.
import socket, re, time, sys
PATH = "UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR"
host, port = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.82", 30636)
s = socket.create_connection((host, port), timeout=12); s.settimeout(8); out = b""
for ch in PATH:
    s.sendall((ch + "\n").encode()); time.sleep(0.03)
time.sleep(0.8)
try:
    while True:
        d = s.recv(4096)
        if not d: break
        out += d
        if b"HTB{" in out: break
except Exception: pass
m = re.search(r"HTB\{[^}]*\}", out.decode("latin1", "replace"))
print("FLAG:", m.group(0) if m else "none")
