#!/usr/bin/env python3
"""
LIT2026 / crypto / faulty_image_2

The visible image (IDAT) just says "Nothing here lol!". The real flag hides in a
non-standard PNG chunk 'tIGr' (note the CRC on it is wrong so viewers ignore it).

- A tEXt chunk stores  XOR-Key = "636f64657469676572"  = hex for "codetiger".
- The tIGr chunk data = [4-byte big-endian length][ciphertext...].
  ciphertext XOR repeating key "codetiger" -> the flag (null-padded to length).
"""
import struct, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'files/corrupt2.png'


def chunks(d):
    off = 8
    while off < len(d) - 4:
        ln = struct.unpack('>I', d[off:off + 4])[0]
        typ = d[off + 4:off + 8]
        data = d[off + 8:off + 8 + ln]
        yield typ, data
        off += 12 + ln
        if typ == b'IEND':
            break


def solve():
    d = open(SRC, 'rb').read()
    text = tigr = None
    for typ, data in chunks(d):
        if typ == b'tEXt':
            text = data
        elif typ == b'tIGr':
            tigr = data
    # tEXt = b'XOR-Key\x00<hexstring>' ; the hex decodes to the ASCII key
    key = bytes.fromhex(text.split(b'\x00', 1)[1].decode())   # b'codetiger'
    n = struct.unpack('>I', tigr[:4])[0]                       # length prefix
    body = tigr[4:4 + n]
    dec = bytes(body[i] ^ key[i % len(key)] for i in range(n))
    return dec.rstrip(b'\x00').decode()


if __name__ == '__main__':
    print(solve())
