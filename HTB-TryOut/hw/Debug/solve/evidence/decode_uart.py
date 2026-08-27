import struct, sys, json, zipfile, io
# Understand Logic 2 internal .sal digital format by dumping structure
path = sys.argv[1]
raw = open(path, 'rb').read()
print("len", len(raw), "head", raw[:16].hex())
assert raw[:8] == b"<SALEAE>"
ver, typ = struct.unpack_from("<ii", raw, 8)
print("ver", ver, "type", typ)
# dump first 200 bytes as hex with offsets
for i in range(0, min(200, len(raw)), 16):
    chunk = raw[i:i+16]
    print("%04X  %s  %s" % (i, chunk.hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in chunk)))
