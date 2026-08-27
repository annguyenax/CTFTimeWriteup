#!/usr/bin/env python3
import hashlib, struct

g = "0123456789bcdefghjkmnpqrstuvwxyz"

def combine(frags):
    out=[]
    for col in zip(*frags):
        x=0
        for c in col:
            x ^= (ord(c)&31)
        out.append(g[x])
    return "".join(out)

def ror8(b,n):
    n%=8; return ((b>>n)|(b<<(8-n)))&0xFF if n else b

def decrypt(ct, passphrase, rotation):
    seed=hashlib.sha256(b"zip-twist-v1|"+passphrase).digest()
    n=(len(ct)+31)//32
    blocks=[hashlib.sha256(seed+struct.pack(">I",i)).digest() for i in range(n)]
    c=ct[::-1]
    out=bytearray()
    for p,bb in enumerate(c):
        out.append(ror8(bb,rotation) ^ blocks[p//32][p%32])
    return bytes(out)

CT=open(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault\Maybe sth in here.bin','rb').read()

# 11-player formations, positions as 2-letter codes
F   = ["GK","LB","CB","CB","RB","LM","CM","CM","RM","ST","ST"]
R1  = ["GK","LB","CB","CB","RB","LM","CM","CM","RM","ST","ST"]
R2  = ["GK","LB","CB","CB","RB","LM","CM","CM","RM","ST","ST"]
QF  = ["GK","LB","CB","CB","RB","CM","CM","CM","LW","ST","RW"]
SF  = ["GK","CB","CB","CB","LWB","RWB","CM","CM","LW","ST","RW"]
R3  = ["GK","CB","CB","CB","LM","RM","CM","CM","CAM","ST","ST"]
R16 = ["GK","CB","CB","CB","LWB","RWB","CM","CM","CM","ST","ST"]
R32 = ["GK","CB","CB","CB","LM","RM","CM","CM","CAM","ST","ST"]

fs=[F,R1,R2,QF,SF,R3,R16,R32]

def test(order_desc, fl):
    codes=["".join(x) for x in fl]
    lens=set(len(c) for c in codes)
    if len(lens)!=1:
        print(f"{order_desc}: unequal {lens}")
        return
    S=combine(codes)
    print(f"{order_desc}: base32={S!r} len={len(S)}")
    cands=set()
    cands.add(S)
    # crockford decode S
    cvals={c:i for i,c in enumerate("0123456789ABCDEFGHJKMNPQRSTVWXYZ")}
    bits=''.join(format(cvals[c],'05b') for c in S.upper() if c in cvals)
    nb=len(bits)//8
    if nb>0:
        B=int(bits[:nb*8],2).to_bytes(nb,'big')
        cands.add(B)
        cands.add(bytes(B))
        try: cands.add(B.decode())
        except: pass
    for cand in cands:
        pb=cand if isinstance(cand,bytes) else cand.encode()
        for rot in range(8):
            pt=decrypt(CT,pb,rot)
            if pt[:2]==b'PK':
                print(f"  !! ZIP passphrase={cand!r} rot={rot}")
                open(rf'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\out.zip','wb').write(pt)
                return True
            if b'PTITCTF' in pt[:300] or b'flag' in pt[:300].lower() or b'SOFAR' in pt[:300]:
                print(f"  !! TEXT passphrase={cand!r} rot={rot} head={pt[:40]!r}")
                open(rf'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\solve\out.txt','wb').write(pt)
                return True
    return False

# try top->bottom and bottom->top, and 2-letter codes
for rev in [False, True]:
    fl=[f[::-1] if rev else f for f in fs]
    if test(f"2letter rev={rev}", fl): break
# single-letter encoding (first letter of each position)
def single(f): return "".join(p[0] for p in f)
for rev in [False, True]:
    fl=[single(f[::-1] if rev else f) for f in fs]
    if test(f"single rev={rev}", fl): break
