#!/usr/bin/env python3
import struct
import numpy as np

MASK = 0xffffffffffffffff
SALT = bytes.fromhex('56209ad9ea8cc85e92753344a88ae685')
KEY = b'ijllc'
GOLDEN = np.uint64(0x9e3779b97f4a7c15)
A = np.uint64(0xbf58476d1ce4e5b9)
B = np.uint64(0x94d049bb133111eb)
PRIME = np.uint64(0x100000001b3)


def fnv1a_64(d, s=0xcbf29ce484222325):
    for b in d:
        s ^= b
        s = (s * 0x100000001b3) & MASK
    return s


def keystreams_vectorized(arg3s, nblocks):
    N = arg3s.shape[0]
    base_seed = fnv1a_64(SALT, fnv1a_64(KEY))
    seeds = np.full(N, base_seed, dtype=np.uint64)
    for shift in [0, 8, 16, 24]:
        byte = ((arg3s.astype(np.uint64) >> shift) & 0xff)
        seeds = (seeds ^ byte) * PRIME
    words = []
    for _ in range(3):
        seeds = seeds + GOLDEN
        z = seeds.copy()
        z ^= z >> np.uint64(30)
        z = z * A
        z ^= z >> np.uint64(27)
        z = z * B
        z ^= z >> np.uint64(31)
        words.append(z)
    k0 = (words[0] & 0xffffffff).astype(np.uint32)
    k1 = (words[0] >> 32).astype(np.uint32)
    k2 = (words[1] & 0xffffffff).astype(np.uint32)
    k3 = (words[1] >> 32).astype(np.uint32)
    k4 = (words[2] & 0xffffffff).astype(np.uint32)
    k5 = (words[2] >> 32).astype(np.uint32)

    def ror8(x):
        return (x >> np.uint32(8)) | (x << np.uint32(24))

    def rol3(x):
        return (x << np.uint32(3)) | (x >> np.uint32(29))

    out = np.empty((N, nblocks * 8), dtype=np.uint8)
    for bi in range(nblocks):
        a = (np.uint32(bi) ^ k4)
        b = k5 ^ arg3s
        s0 = k0.copy()
        s1 = k1.copy()
        s2 = k2.copy()
        s3 = k3.copy()
        for r in range(27):
            a = (ror8(a) + b) ^ s0
            b = rol3(b) ^ a
            i = r % 3
            if i == 0:
                s1 = (ror8(s1) + s0) ^ np.uint32(r)
                s0 = rol3(s0) ^ s1
            elif i == 1:
                s2 = (ror8(s2) + s0) ^ np.uint32(r)
                s0 = rol3(s0) ^ s2
            else:
                s3 = (ror8(s3) + s0) ^ np.uint32(r)
                s0 = rol3(s0) ^ s3
        out[:, bi * 8:bi * 8 + 4] = a.astype('<u4').view(np.uint8).reshape(N, 4)
        out[:, bi * 8 + 4:bi * 8 + 8] = b.astype('<u4').view(np.uint8).reshape(N, 4)
    return out


data = open('chall_new.exe', 'rb').read()
arr = np.frombuffer(data, dtype=np.uint8)

arg3s = np.arange(65536, dtype=np.uint32)
kss_full = keystreams_vectorized(arg3s, 6)  # up to 48 bytes

for wlen in [27, 30, 36, 24, 40, 48]:
    kss = kss_full[:, :wlen]
    seg = arr[0x2e00:0x7e00]
    N = seg.shape[0] - wlen + 1
    print(f'wlen={wlen} searching {N} offsets...', flush=True)
    CHUNK = 256
    for start in range(0, N, CHUNK):
        w = seg[start:start + CHUNK + wlen - 1]
        win = np.lib.stride_tricks.sliding_window_view(w, wlen)  # (C, wlen)
        pt = win[:, None, :] ^ kss[None, :, :]  # (C, 65536, wlen)
        ok = ((pt >= 48) & (pt <= 57)) | ((pt >= 65) & (pt <= 90)) | ((pt >= 97) & (pt <= 122)) \
             | (pt == 95) | (pt == 123) | (pt == 125)
        row_ok = ok.all(axis=2)
        has_us = ((pt == 95) | (pt == 123)).any(axis=2)
        m = row_ok & has_us
        idx = np.nonzero(m)
        for ci, ai in zip(*idx):
            off = 0x2e00 + start + ci
            print(f'wlen={wlen} off={off:#x} arg3={ai:#x}: {pt[ci, ai].tobytes()!r}', flush=True)
    print(f'wlen={wlen} done', flush=True)
print('ALL DONE', flush=True)
