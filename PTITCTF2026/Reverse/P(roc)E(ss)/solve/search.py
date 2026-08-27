#!/usr/bin/env python3
import struct
MASK = 0xffffffffffffffff
def fnv1a_64(data, seed=0xcbf29ce484222325):
    for b in data:
        seed ^= b; seed = (seed * 0x100000001b3) & MASK
    return seed
def smf(x):
    x&=MASK; x^=x>>30; x=(x*0xbf58476d1ce4e5b9)&MASK; x^=x>>27; x=(x*0x94d049bb133111eb)&MASK; x^=x>>31; return x
salt = bytes.fromhex('7f69fd375b06cd415d4b36aade3db1a1')
def ks(arg3):
    s=fnv1a_64(b'4mCnFu'); s=fnv1a_64(salt,s); s=fnv1a_64(struct.pack('<I',arg3),s)
    d=[]
    for _ in range(3):
        s=(s+0x9e3779b97f4a7c15)&MASK; d.append(smf(s))
    return list(struct.unpack('<6I', b''.join(x.to_bytes(8,'little') for x in d)))
def ror(x,n): return ((x>>n)|(x<<(32-n)))&0xffffffff
def rol(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff
def arx(a,b,k):
    s0,s1,s2,s3=k[0],k[1],k[2],k[3]; st=[s1,s2,s3]
    for r in range(27):
        a=((ror(a,8)+b)^s0)&0xffffffff; b=(rol(b,3)^a)&0xffffffff
        idx=r%3; st[idx]=((ror(st[idx],8)+s0)^r)&0xffffffff; s0=(rol(s0,3)^st[idx])&0xffffffff
    return a,b
def dec(blob,arg3):
    k=ks(arg3); out=bytearray(len(blob))
    for i in range(0,len(blob),8):
        a=(i//8)^k[4]; b=k[5]^arg3; a,b=arx(a,b,k); kb=struct.pack('<II',a,b)
        for j in range(8):
            if i+j<len(blob): out[i+j]=blob[i+j]^kb[j]
    return bytes(out)

data=open('live_chall.exe','rb').read()
rdata=data[0x3000:0x3000+0x4d18]
# try arg3 0..2000 on the decoy blob
blob=data[0x305c:0x305c+64]
print("decoy blob arg3 brute:")
for arg3 in range(0,2001):
    o=dec(blob,arg3)
    if o[:8]==b'PTITCTF{':
        print("FOUND arg3",arg3, o[:60]); break
else:
    print("  none")
# search all rdata offsets for a 64-byte blob decoding to PTITCTF{ with arg3=0
print("rdata offset search (arg3=0):")
hits=[]
for off in range(0,len(rdata)-64):
    b=rdata[off:off+64]
    o=dec(b,0)
    if o[:8]==b'PTITCTF{':
        hits.append(0x5000+off)
print("hits:", [hex(h) for h in hits])
