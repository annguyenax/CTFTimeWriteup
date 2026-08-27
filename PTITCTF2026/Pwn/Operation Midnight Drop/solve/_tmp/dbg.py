import socket, struct, sys, re, time
HOST, PORT = sys.argv[1], int(sys.argv[2])

def rd(s, t=1.5):
    s.settimeout(t); buf=b""
    try:
        while True:
            d=s.recv(4096)
            if not d: break
            buf+=d
    except socket.timeout: pass
    return buf

s=socket.create_connection((HOST,PORT))
banner=rd(s,1.5)
print("BANNER:", banner)
m=re.search(rb"session token: ([0-9a-f]{8})", banner)
token=int(m.group(1),16)
print("token", hex(token))

def checksum(ptype, plen, payload):
    x=((((ptype<<24)&0xffffffff)^token)&0xffffffff)^plen
    x^=0x31415926; x&=0xffffffff
    for i in range(plen):
        x=((x<<5)|(x>>27))&0xffffffff
        x=(x+((i*0x45d9f3b)^payload[i]))&0xffffffff
    return x&0xffffffff

def packet(ptype,payload):
    plen=len(payload); ck=checksum(ptype,plen,payload)
    pkt=struct.pack("<I",ptype)+struct.pack("<I",plen)+struct.pack("<I",ck)+payload
    s.sendall(pkt)
    return rd(s,1.2)

print("--- send type=1 HELLO ---")
print(packet(1,b""))

print("--- send AUTH ---")
print(packet(2,struct.pack("<I",(token^0xc0ffee00)&0xffffffff)))
s.close()
