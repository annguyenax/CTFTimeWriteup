#!/usr/bin/env python3
import struct

MASK = 0xffffffffffffffff
def fnv1a_64(data, seed=0xcbf29ce484222325):
    for b in data:
        seed ^= b
        seed = (seed * 0x100000001b3) & MASK
    return seed

def splitmix_finalize(x):
    x &= MASK
    x ^= x >> 30
    x = (x * 0xbf58476d1ce4e5b9) & MASK
    x ^= x >> 27
    x = (x * 0x94d049bb133111eb) & MASK
    x ^= x >> 31
    return x

def keystream_dwords(arg3):
    seed = fnv1a_64(b'4mCnFu')
    seed = fnv1a_64(salt, seed)
    seed = fnv1a_64(struct.pack('<I', arg3 & 0xffffffff), seed)
    dwords = []
    for _ in range(3):  # 24 bytes = 3 x 8 bytes
        seed = (seed + 0x9e3779b97f4a7c15) & MASK
        dwords.append(splitmix_finalize(seed))
    # dwords is 3 x 64-bit = 6 x 32-bit
    ks = b''.join(d.to_bytes(8,'little') for d in dwords)
    return list(struct.unpack('<6I', ks[:24]))

salt = bytes.fromhex('7f69fd375b06cd415d4b36aade3db1a1')

def ror(x, n): return ((x >> n) | (x << (32-n))) & 0xffffffff
def rol(x, n): return ((x << n) | (x >> (32-n))) & 0xffffffff

def arx(a, b, k):
    s0, s1, s2, s3 = k[0], k[1], k[2], k[3]
    state = [s1, s2, s3]
    for rnd in range(27):  # 0..0x1a inclusive
        tmp = s0
        a = ((ror(a,8) + b) ^ s0) & 0xffffffff
        b = ((rol(b,3)) ^ a) & 0xffffffff
        idx = rnd % 3
        state[idx] = ((ror(state[idx],8) + s0) ^ rnd) & 0xffffffff
        s0 = (rol(s0,3) ^ state[idx]) & 0xffffffff
    return a, b

def decode_blob(blob, arg3):
    k = keystream_dwords(arg3)
    out = bytearray(len(blob))
    for i in range(0, len(blob), 8):
        block_idx = i // 8
        a = (block_idx ^ k[4]) & 0xffffffff
        b = (k[5] ^ (arg3 & 0xffffffff)) & 0xffffffff
        a, b = arx(a, b, k)
        ks8 = struct.pack('<II', a, b)
        for j in range(8):
            if i+j < len(blob):
                out[i+j] = blob[i+j] ^ ks8[j]
    return bytes(out)

data = open('live_chall.exe','rb').read()
def va2off(va): return 0x3000 + (va - (0x140000000+0x5000))

blobs = {
  'decoy_blob_64': (0x14000505c, 64),
  'exe_blob_64': (0x14000503c, 64),
}
for name,(va,n) in blobs.items():
    blob = data[va2off(va):va2off(va)+n]
    for arg3 in [0, 1, 0x40, 0x18, 0x57, 0x1000]:
        out = decode_blob(blob, arg3)
        print(f"[{name}] arg3={arg3:#x}: {out[:57]!r}")
    print()
