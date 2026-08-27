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

def rol8(b,n):
    n%=8; return ((b<<n)|(b>>(8-n)))&0xFF if n else b
def ror8(b,n):
    n%=8; return ((b>>n)|(b<<(8-n)))&0xFF if n else b

def decrypt(ct, passphrase, rotation):
    seed=hashlib.sha256(b"zip-twist-v1|"+passphrase).digest()
    n=(len(ct)+31)//32
    blocks=[hashlib.sha256(seed+struct.pack(">I",i)).digest() for i in range(n)]
    c=ct[::-1]
    out=bytearray()
    for p,bb in enumerate(c):
        tmp=ror8(bb,rotation)
        out.append(tmp ^ blocks[p//32][p%32])
    return bytes(out)

CT=open(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault\Maybe sth in here.bin','rb').read()

F   = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
R1  = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
R2  = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
QF  = ["ST","LW","RW","CM","CM","CM","LB","CB","CB","RB","GK"]
SF  = ["ST","LW","RW","CM","CM","LWB","RWB","CB","CB","CB","GK"]
R3  = ["ST","ST","CAM","LM","RM","CM","CM","CB","CB","CB","GK"]
R16 = ["ST","ST","CM","CM","CM","LWB","RWB","CB","CB","CB","GK"]
R32 = ["ST","ST","CAM","LM","RM","CM","CM","CB","CB","CB","GK"]

fl=[F,R1,R2,QF,SF,R3,R16,R32]
codes=["".join(x) for x in fl]
print("lengths:", set(len(c) for c in codes))
for c in codes: print(" ", c)
S=combine(codes)
print("base32:", S, len(S))
print("decoded candidate passphrases:")
print(" as-is:", S)
cvals={c:i for i,c in enumerate("0123456789ABCDEFGHJKMNPQRSTVWXYZ")}
bits=''
for cc in S.upper():
    if cc in cvals:
        bits+=format(cvals[cc],'05b')
nbytes=len(bits)//8
if nbytes>0:
    B=int(bits[:nbytes*8],2).to_bytes(nbytes,'big')
    print(" crockford-decode bytes:", B)
    try: print(" as ascii:", B.decode())
    except: pass
