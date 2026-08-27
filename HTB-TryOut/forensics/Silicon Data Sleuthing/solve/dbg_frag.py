import struct, lzma
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img", 'rb').read()

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return None

# fragment blocks: xz magic at 0x2cf3c (frag0), 0x3a7c8 (frag1), 0x4497c (frag2)
for m in (0x2cf3c, 0x3a7c8, 0x4497c):
    u16 = struct.unpack_from('<H', data, m-2)[0]
    u32 = struct.unpack_from('<I', data, m-4)[0]
    print('%#x: u16@-2=%#x(%d) u32@-4=%#x(%d)' % (m, u16, u16, u32, u32))

# try u32 size word at m-4: compressed size = low 31 bits
m = 0x2cf3c
w = struct.unpack_from('<I', data, m-4)[0]
print('frag0 size word u32:', hex(w), 'bit31:', bool(w & 0x80000000), 'size:', w & 0x7fffffff)
csize = w & 0x7fffffff
blk = data[m:m+csize]
d = decomp(blk)
print('frag0 decompressed:', len(d) if d else None)
# try u16 at m-2
w16 = struct.unpack_from('<H', data, m-2)[0]
print('frag0 u16:', hex(w16), 'bit15:', bool(w16 & 0x8000), 'size:', w16 & 0x7fff)
d2 = decomp(data[m:m+(w16 & 0x7fff)])
print('frag0 u16 decompressed:', len(d2) if d2 else None)

# fragment entry sizes: frag0 size=55436 (uncompressed block size?), check decompressed len
# board_detect: frag 0, off 0, fsize 205 -> read d[0:205]
print('board_detect content:', d[:205] if d and len(d) >= 205 else None)

# busybox block list: u32 entries at inode+32; data at 0x60
istream = b''
def meta_blocks(start, end):
    pos = start
    while pos + 2 <= end:
        (sz,) = struct.unpack_from('<H', data, pos)
        if sz == 0:
            break
        yield pos, data[pos+2:pos+2+sz]
        pos += 2 + sz
        if pos >= end:
            break
for w, raw in meta_blocks(0x37e924, 0x380bc4):
    istream += decomp(raw)
bb = istream[63:63+40]
print('busybox inode:', bb.hex(' '))
start, frag, sparse, fsize = struct.unpack_from('<IIII', bb, 16)
print('busybox start=%#x frag=%#x sparse=%d fsize=%d' % (start, frag, sparse, fsize))
nblocks = (fsize + 262144 - 1) // 262144
print('nblocks:', nblocks)
blist = struct.unpack_from('<%dI' % nblocks, bb, 32)
print('block list:', [hex(x) for x in blist])
# read blocks
out = b''
pos = start
for entry in blist:
    comp = not (entry & 0x80000000)
    csize = entry & 0x7fffffff
    chunk = data[pos:pos+csize]
    out += decomp(chunk) if comp else chunk
    pos += csize
print('busybox first 16 bytes:', out[:16])
print('busybox len:', len(out))
