import socket, struct, sys, re, time
sys.path.insert(0, __file__.rsplit("\\",1)[0])
from client import connect, rd, send_packet, checksum

HOST = sys.argv[1]; PORT = int(sys.argv[2])
import client

def cks(ptype, plen, payload):
    return client.checksum(ptype, plen, payload, client.TOKEN)

s = connect()
banner = rd(s, 1.5)
m = re.search(rb"session token: ([0-9a-f]{8})", banner)
client.TOKEN = int(m.group(1), 16)
print("token", hex(client.TOKEN))

def pkt(ptype, payload, t=1.2):
    send_packet(s, ptype, payload)
    return rd(s, t)

# AUTH
r = pkt(2, struct.pack("<I", (client.TOKEN ^ 0xc0ffee00) & 0xffffffff))
print("AUTH:", r)
# small rule slot: rlen=1
r = pkt(3, struct.pack("<H",1)+b"A")
print("RULE:", r)
# report create
r = pkt(4, b"hello")
print("REPORT:", r)
# leaks
for ch in (b"D", b"P", b"R"):
    r = pkt(4, ch)
    print(f"leak {ch}:", r)
s.close()
