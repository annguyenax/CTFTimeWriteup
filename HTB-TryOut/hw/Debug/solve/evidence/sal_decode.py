import struct, json, zipfile, io
# Logic 2 internal .sal digital format (type 100)
# Parse digital-1.bin (RX). Understand the binary layout after <SALEAE> header.
path = r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1.bin"
data = open(path, 'rb').read()
print("len", len(data))
# After <SALEAE>(8): version(int32), type(int32)
ver, typ = struct.unpack_from("<ii", data, 8)
print("ver", ver, "type", typ)
# dump bytes 16..160 as hex+ascii
for i in range(16, 176, 16):
    c = data[i:i+16]
    print("%04X %s | %s" % (i, c.hex(' '), ''.join(chr(b) if 32<=b<127 else '.' for b in c)))
