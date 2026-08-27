import struct
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1.bin", 'rb').read()
# Logic 2 internal .sal digital format:
# header: <SALEAE> (8) + version (4) + type (4)
# For internal save (type 100), structure differs from export (type 0).
# Let's brute-inspect: print all little-endian uint64 and uint32 candidate offsets
print("len", len(data))
for off in range(16, 80, 4):
    u32 = struct.unpack_from("<I", data, off)[0]
    u64 = struct.unpack_from("<Q", data, off)[0]
    f64 = struct.unpack_from("<d", data, off)[0]
    print("off %d: u32=%d u64=%d f64=%.6g" % (off, u32, u64, f64))
