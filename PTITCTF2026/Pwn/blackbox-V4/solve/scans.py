#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    s.send(fmt.encode()+b"\n"); time.sleep(0.08)
    try: return s.recv(4096)
    except Exception: return b'<T>'
for n in range(47, 76):
    d=ask("%%%d$s" % n)
    print(f"%{n}$s:", repr(d))
    if d==b'' or d==b'<T>':
        print("  (connection ended)")
        break
s.close()
