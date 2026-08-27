#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
def test(n):
    s=socket.socket(); s.settimeout(2); s.connect((HOST,PORT)); s.recv(300)
    s.send(b"A"*n)  # no newline
    d=b''
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            d+=c
    except Exception: pass
    s.close(); return d
# send varying lengths, count A's echoed before first prompt
for n in [20,22,23,24,25,26,30,48]:
    d=test(n)
    # count 'A' runs separated by '> '
    runs=re.findall(rb'A+', d)
    chunks=[len(r) for r in runs]
    print(f"n={n}: echo chunks={chunks} raw={d!r}")
    time.sleep(0.1)
