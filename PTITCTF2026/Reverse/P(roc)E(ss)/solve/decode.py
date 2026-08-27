#!/usr/bin/env python3
import struct

def fnv1a_64(data, seed=0xcbf29ce484222325):
    for b in data:
        seed ^= b
        seed = (seed * 0x100000001b3) & 0xffffffffffffffff
    return seed

def splitmix64(x):
    x = (x + 0x9e3779b97f4a7c15) & 0xffffffffffffffff
    x ^= x >> 30
    x = (x * 0xbf58476d1ce4e5b9) & 0xffffffffffffffff
    x ^= x >> 27
    x = (x * 0x94d049bb133111eb) & 0xffffffffffffffff
    x ^= x >> 31
    return x

salt = bytes.fromhex('7f69fd375b06cd415d4b36aade3db1a1')

def keystream(arg3, nbytes=24):
    seed = fnv1a_64(b'4mCnFu')
    seed = fnv1a_64(salt, seed)
    seed = fnv1a_64(struct.pack('<I', arg3), seed)
    ks = b''
    while len(ks) < nbytes:
        seed = splitmix64(seed)
        ks += seed.to_bytes(8, 'little')
    return ks[:nbytes]

data = open('live_chall.exe','rb').read()
def va2off(va): return 0x3000 + (va - (0x140000000+0x5000))

# candidate blobs
blobs = {
  'decoy_blob': (0x14000505c, 57),
  'exe_blob': (0x14000503c, 57),
}

for name,(va,n) in blobs.items():
    blob = data[va2off(va):va2off(va)+n]
    for arg3 in [0, 57, 0x40, 0x10, 0x40, 0x18, 0x1000]:
        ks = keystream(arg3, n)
        out = bytes([b ^ k for b,k in zip(blob, ks)])
        print(f"[{name}] arg3={arg3:#x}: {out!r}")
    print()
