#!/usr/bin/env python3
import struct
MASK=0xffffffffffffffff
def fnv1a_64(d,s=0xcbf29ce484222325):
    for b in d: s^=b; s=(s*0x100000001b3)&MASK
    return s
def smf(x):
    x&=MASK; x^=x>>30; x=(x*0xbf58476d1ce4e5b9)&MASK; x^=x>>27; x=(x*0x94d049bb133111eb)&MASK; x^=x>>31; return x
salt=bytes.fromhex('7f69fd375b06cd415d4b36aade3db1a1')
def ks(a):
    s=fnv1a_64(b'4mCnFu'); s=fnv1a_64(salt,s); s=fnv1a_64(struct.pack('<I',a&0xffffffff),s)
    d=[]
    for _ in range(3): s=(s+0x9e3779b97f4a7c15)&MASK; d.append(smf(s))
    return list(struct.unpack('<6I', b''.join(x.to_bytes(8,'little') for x in d)))
def ror(x,n): return ((x>>n)|(x<<(32-n)))&0xffffffff
def rol(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff
def arx(a,b,k):
    s0,s1,s2,s3=k[0],k[1],k[2],k[3]; st=[s1,s2,s3]
    for r in range(27):
        a=((ror(a,8)+b)^s0)&0xffffffff; b=(rol(b,3)^a)&0xffffffff
        i=r%3; st[i]=((ror(st[i],8)+s0)^r)&0xffffffff; s0=(rol(s0,3)^st[i])&0xffffffff
    return a,b
def dec(blob,a):
    k=ks(a); o=bytearray(len(blob))
    for i in range(0,len(blob),8):
        aa=(i//8)^k[4]; bb=k[5]^a; aa,bb=arx(aa,bb,k); kb=struct.pack('<II',aa,bb)
        for j in range(8):
            if i+j<len(blob): o[i+j]=blob[i+j]^kb[j]
    return bytes(o)

ct=bytes.fromhex('62520fb8a3a473218f1d04fc50588e44c2036b5fdfce6f0b')
print('ciphertext:', ct.hex(), 'len', len(ct))
for arg3 in [0, 0xa, 0x39, 0x18, 3, 24, 0x637, 0x64, 0x80, 0x57, 1]:
    pt=dec(ct, arg3)
    print(f'arg3={arg3:#x}: hex={pt.hex()} ascii={pt!r}')
