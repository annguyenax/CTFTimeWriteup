import struct, sys
# The _exp.bin files are likely the "expanded" data. Let me understand what they contain.
# digital-1_exp.bin: len 2977548, mostly 0x00/0xFF alternating in regular runs.
# Let me check if it's actually the raw sampled stream (1 byte per sample) but the sample
# rate is 25MHz and duration 37s -> that would be ~937M samples, far more than 2.9M.
# So _exp.bin is NOT per-sample. Let me look at the actual internal format.

# Re-examine: maybe digital-1_exp.bin is a transition-time list in uint64, but values 0x00/0xFF?
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1_exp.bin", 'rb').read()
print("len", len(data))
# Interpret as uint64 timestamps (sample indices)
import collections
# sample first 100 uint64
vals = struct.unpack_from("<%dQ" % 50, data, 0)
print("first 50 u64:", vals[:50])
# check where nonzero
for i in range(0, 200, 8):
    v = struct.unpack_from("<Q", data, i)[0]
    print(i, v)
