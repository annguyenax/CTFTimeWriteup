#!/usr/bin/env python3
import struct
import numpy as np

MASK = 0xffffffffffffffff
SALT = bytes.fromhex('56209ad9ea8cc85e92753344a88ae685')
KEY = b'ijllc'


def fnv1a_64(d, s=0xcbf29ce484222325):
    for b in d:
        s ^= b
        s = (s * 0x100000001b3) & MASK
    return s


def smf(x):
    x &= MASK
    x ^= x >> 30
    x = (x * 0xbf58476d1ce4e5b9) & MASK
    x ^= x >> 27
    x = (x * 0x94d049bb133111eb) & MASK
    x ^= x >> 31
    return x


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff


def rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def arx(a, b, k):
    s0, s1, s2, s3 = k[0], k[1], k[2], k[3]
    st = [s1, s2, s3]
    for r in range(27):
        a = ((ror(a, 8) + b) ^ s0) & 0xffffffff
        b = (rol(b, 3) ^ a) & 0xffffffff
        i = r % 3
        st[i] = ((ror(st[i], 8) + s0) ^ r) & 0xffffffff
        s0 = (rol(s0, 3) ^ st[i]) & 0xffffffff
    return a, b


def keystream_bytes(key, arg3, base_seed, nblocks):
    s = fnv1a_64(struct.pack('<I', arg3 & 0xffffffff), base_seed)
    words = []
    for _ in range(3):
        s = (s + 0x9e3779b97f4a7c15) & MASK
        words.append(smf(s))
    k = list(struct.unpack('<6I', b''.join(x.to_bytes(8, 'little') for x in words)))
    ks = b''
    for bi in range(nblocks):
        a = bi ^ k[4]
        b = k[5] ^ arg3
        a, b = arx(a, b, k)
        ks += struct.pack('<II', a, b)
    return ks


data = open('chall_new.exe', 'rb').read()
arr = np.frombuffer(data, dtype=np.uint8)
base_seed = fnv1a_64(SALT, fnv1a_64(KEY))

for wlen in [27, 30, 36]:
    nb = (wlen + 7) // 8
    kss = np.stack([np.frombuffer(keystream_bytes(KEY, a, base_seed, nb)[:wlen], dtype=np.uint8)
                    for a in range(65536)])
    seg = arr[0x3000:0x7e00]
    N = seg.shape[0] - wlen + 1
    for off in range(N):
        blob = seg[off:off + wlen]
        pt = blob[None, :] ^ kss  # (65536, wlen)
        ok = ((pt >= 48) & (pt <= 57)) | ((pt >= 65) & (pt <= 90)) | ((pt >= 97) & (pt <= 122)) \
             | (pt == 95) | (pt == 123) | (pt == 125)
        row_ok = ok.all(axis=1)
        if row_ok.any():
            has_us = ((pt == 95) | (pt == 123)).any(axis=1)
            m = row_ok & has_us
            idx = np.nonzero(m)[0]
            for a in idx:
                print(f'wlen={wlen} off={0x3000+off:#x} arg3={a:#x}: {pt[a].tobytes()!r}', flush=True)
    print(f'wlen={wlen} done', flush=True)
print('ALL DONE', flush=True)
