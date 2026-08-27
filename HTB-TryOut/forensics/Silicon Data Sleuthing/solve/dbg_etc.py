import struct, lzma
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img", 'rb').read()

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception as e:
        return None

# frag0 entry: start 0x2cf3c, size 55436. Next frag block at 0x3a7c8.
d1 = decomp(data[0x2cf3c:0x2cf3c+55436])
print('decompress [0x2cf3c : +55436]:', len(d1) if d1 else None)
d2 = decomp(data[0x2cf3c:0x3a7c8])
print('decompress [0x2cf3c : 0x3a7c8]:', len(d2) if d2 else None)
d3 = decomp(data[0x2cf3c:])
print('decompress [0x2cf3c:EOF]:', len(d3) if d3 else None)

# board_detect check via each
for nm, d in (('d1', d1), ('d2', d2), ('d3', d3)):
    if d:
        print(nm, 'first 40:', d[:40])

# find /etc/openwrt_release: ref from etc listing. Walk: root->etc->openwrt_release
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

istream = b''
ib = []
for w, raw in meta_blocks(0x37e924, 0x380bc4):
    d = decomp(raw)
    ib.append((w - 0x37e924, len(istream), len(d)))
    istream += d
dstream = b''
db = []
for w, raw in meta_blocks(0x380bc4, 0x383ee2):
    d = decomp(raw)
    db.append((w - 0x380bc4, len(dstream), len(d)))
    dstream += d

def inode_at(ref):
    hi, lo = ref >> 16, ref & 0xFFFF
    for (w, s, l) in ib:
        if w == hi:
            return istream[s+lo:]
    return None

def stream_at(blocks, off, stream):
    for (w, s, l) in blocks:
        if w == off:
            return stream[s:s+l]
    return None

# etc dir inode: ref (0x662<<16)|0x625
etc = inode_at((0x662 << 16) | 0x625)
t = struct.unpack_from('<H', etc, 0)[0]
start, nlink, fsize, off, parent = struct.unpack_from('<IIHHI', etc, 16)
print('etc inode: type', t, 'start_block', hex(start), 'nlink', nlink, 'fsize', fsize, 'offset', hex(off), 'parent', parent)
blk = stream_at(db, start, dstream)
pos = off
entries = []
end = len(blk)
while pos + 12 <= end:
    cnt, base_block, base_ino = struct.unpack_from('<III', blk, pos)
    pos += 12
    for _ in range(cnt + 1):
        off2, ino_d, etype, esize = struct.unpack_from('<HHHH', blk, pos)
        pos += 8
        name = blk[pos:pos+esize+1]
        pos += esize + 1
        entries.append((name, (base_block << 16) | off2, etype, base_ino + ino_d))
print('etc entries:')
for nm, ref, et, ino in entries:
    mark = ' <== ' if b'openwrt' in nm else ''
    print('  ', nm, hex(ref), et, ino, mark)
