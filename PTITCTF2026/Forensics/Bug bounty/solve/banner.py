#!/usr/bin/env python3
# Dump raw TCP banner/menu:  python3 banner.py 144.79.188.39 35259
import sys, socket
host, port = sys.argv[1], int(sys.argv[2])
s = socket.socket(); s.settimeout(8)
s.connect((host, port))
data = b""
try:
    while True:
        c = s.recv(4096)
        if not c: break
        data += c
        if len(data) > 20000: break
except socket.timeout:
    pass
print("=== RAW BANNER (%d bytes) ===" % len(data))
sys.stdout.write(data.decode('utf-8', 'replace'))
print("\n=== END ===")
s.close()
