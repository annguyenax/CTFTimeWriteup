import struct, lzma
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img", 'rb').read()

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return None

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

def stream_off(blocks, w_off):
    for (w, s, l) in blocks:
        if w == w_off:
            return s
    return None

def inode_at(ref):
    hi, lo = ref >> 16, ref & 0xFFFF
    for (w, s, l) in ib:
        if w == hi:
            return istream[s+lo:]
    return None

# etc listing
so = stream_off(db, 0)
seg = dstream[so + 0x1136: so + 0x1136 + 992]
i = seg.find(b'openwrt')
print('openwrt at seg offset', hex(i))
print('around:', seg[i-40:i+60])
# parse headers+entries with positions
pos = 0
hdr_count = 0
print('\n--- parse walk ---')
while pos + 12 <= len(seg):
    cnt, base_block, base_ino = struct.unpack_from('<III', seg, pos)
    hdr_count += 1
    print('HDR at %#x: count=%d base_block=%#x base_ino=%d' % (pos, cnt, base_block, base_ino))
    pos += 12
    for _ in range(cnt + 1):
        off, ino_d, etype, esize = struct.unpack_from('<HHHH', seg, pos)
        pos += 8
        name = seg[pos:pos+esize+1]
        pos += esize + 1
        if b'openwrt' in name or name in (b'rc.d', b'rc.local', b'os-release'):
            print('   ENTRY %#x: off=%#x ino_d=%d type=%d size=%d name=%s ref=%#x ino=%d' % (
                pos-8-esize-1, off, ino_d, etype, esize, name, (base_block<<16)|off, base_ino+ino_d))
print('hdr_count', hdr_count, 'pos end', hex(pos), 'seg len', len(seg))

# check inode at stream 0x1912 (block 0) and 8192+0x1912 (block 1)
for ref in (0x1912, (0x662<<16)|0x1912, 0x1932, (0x662<<16)|0x1932):
    ib_ = inode_at(ref)
    if ib_:
        t = struct.unpack_from('<H', ib_, 0)[0]
        ino = struct.unpack_from('<I', ib_, 12)[0] if t < 8 else struct.unpack_from('<Q', ib_, 0)[0]
        print('ref %#x -> type %d ino %d' % (ref, t, ino))
