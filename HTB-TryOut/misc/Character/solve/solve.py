#!/usr/bin/env python3
"""Character (HTB TryOut, misc, very easy)

Service asks for a flag index and returns one character. Walk 0..N.
"""
import socket, re, sys, time

def recv_until(s, needle, limit=8192):
    buf = b""
    while needle not in buf and len(buf) < limit:
        d = s.recv(4096)
        if not d:
            break
        buf += d
    return buf

def solve(host, port):
    s = socket.create_connection((host, port), timeout=10)
    s.settimeout(5)
    recv_until(s, b"index:")
    flag = []
    for i in range(0, 128):
        s.sendall(("%d\n" % i).encode())
        data = recv_until(s, b"index:")
        text = data.decode("latin1", "replace")
        m = re.search(r"Character at Index \d+: (.)", text)
        if not m:
            print("STOP at", i, repr(text))
            break
        flag.append(m.group(1))
        if flag[-1] == "}" and "".join(flag).startswith("HTB{"):
            break
    out = "".join(flag)
    print(out)
    m = re.search(r"HTB\{[^}]*\}", out)
    if m:
        open("final_flag.txt", "w").write(m.group(0) + "\n")
        print("FLAG:", m.group(0))
        return m.group(0)
    return None

if __name__ == "__main__":
    h, p = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.73", 30760)
    solve(h, p)
