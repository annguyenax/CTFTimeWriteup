#!/usr/bin/env python3
"""
LIT2026 / crypto / faulty_image_1_haha

The PNG was tampered by INSERTING the 4-byte marker b'haha' (68 61 68 61)
into the file every 100 bytes (stride 104: 100 original bytes + 4 inserted).
This corrupts the DEFLATE stream inside IDAT so no viewer can open it.

Fix: walk the file keeping 100 bytes then skipping the 4-byte 'haha' marker,
which restores the original IDAT; it then decompresses cleanly and the image
(containing the flag as text) renders.
"""
import zlib, struct, binascii, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'files/corrupt.png'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'recovered.png'


def chunk(typ, data):
    return struct.pack('>I', len(data)) + typ + data + \
        struct.pack('>I', binascii.crc32(typ + data) & 0xffffffff)


def main():
    d = open(SRC, 'rb').read()
    out = bytearray()
    i = 0
    while i < len(d):
        out += d[i:i + 100]
        i += 100
        if d[i:i + 4] == b'haha':      # drop the inserted marker
            i += 4
    fixed = bytes(out)

    idat_len = struct.unpack('>I', fixed[33:37])[0]     # 2155, original length
    idat = fixed[41:41 + idat_len]
    raw = zlib.decompress(idat)
    assert len(raw) == 150 * (1 + 400 * 3), 'unexpected raw size'

    ihdr = struct.pack('>IIBBBBB', 400, 150, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + \
        chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')
    open(OUT, 'wb').write(png)
    print(f'recovered {OUT} ({len(png)} bytes); open it to read the flag')


if __name__ == '__main__':
    main()
