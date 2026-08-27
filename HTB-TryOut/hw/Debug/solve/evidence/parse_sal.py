import struct, sys, json, zipfile, io
path = sys.argv[1]
raw = open(path, 'rb').read()
print("len", len(raw))
print("head", raw[:16].hex())
assert raw[:8] == b"<SALEAE>"
ver, typ = struct.unpack_from("<ii", raw, 8)
print("ver", ver, "type", typ)
off = 16
if ver >= 1:
    chunk_count = struct.unpack_from("<Q", raw, off)[0]; off += 8
else:
    chunk_count = 1
print("chunk_count", chunk_count)
for ci in range(chunk_count):
    initial = struct.unpack_from("<I", raw, off)[0]; off += 4
    if ver >= 1:
        rate = struct.unpack_from("<d", raw, off)[0]; off += 8
    else:
        rate = None
    begin, end, n = struct.unpack_from("<ddQ", raw, off); off += 24
    times = list(struct.unpack_from("<%dd" % n, raw, off)); off += 8*n
    print("chunk", ci, "initial", initial, "rate", rate, "begin", begin, "end", end, "n", n)
    print("first times:", times[:20])
    print("last times:", times[-10:])
