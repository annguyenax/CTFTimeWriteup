import socket, struct, sys, re, time

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TOKEN = None

def connect():
    return socket.create_connection((HOST, PORT))

def rd(s, t=1.5):
    s.settimeout(t); buf=b""
    try:
        while True:
            d = s.recv(4096)
            if not d: break
            buf += d
    except socket.timeout:
        pass
    return buf

def checksum(ptype, plen, payload, token):
    x = ((((ptype << 24) & 0xffffffff) ^ token) & 0xffffffff) ^ plen
    x ^= 0x31415926; x &= 0xffffffff
    for i in range(plen):
        x = ((x << 5) | (x >> 27)) & 0xffffffff
        x = (x + ((i * 0x45d9f3b) ^ payload[i])) & 0xffffffff
    return x & 0xffffffff

def send_packet(s, ptype, payload):
    plen = len(payload)
    ck = checksum(ptype, plen, payload, TOKEN)
    # header as ASCII decimal/hex + raw payload
    hdr = f"{ptype}\n{plen}\n{ck:x}\n".encode()
    s.sendall(hdr + payload)

def get_token(s):
    global TOKEN
    banner = rd(s, 1.5)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    TOKEN = int(m.group(1), 16)
    return banner, TOKEN

if __name__ == "__main__":
    s = connect()
    banner, tok = get_token(s)
    print(banner.decode(errors="replace"))
    print("token =", hex(tok))
    print("--- HELLO ---")
    send_packet(s, 1, b"")
    print(rd(s, 1.2).decode(errors="replace"))
    print("--- AUTH ---")
    send_packet(s, 2, struct.pack("<I", (tok ^ 0xc0ffee00) & 0xffffffff))
    print(rd(s, 1.2).decode(errors="replace"))
    s.close()
