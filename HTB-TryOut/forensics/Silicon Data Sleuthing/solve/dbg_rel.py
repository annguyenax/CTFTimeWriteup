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

# etc listing: block 0, offset 0x1136, fsize 992
so = stream_off(db, 0)
seg = dstream[so + 0x1136: so + 0x1136 + 992]
pos = 0
entries = []
while pos + 12 <= len(seg):
    cnt, base_block, base_ino = struct.unpack_from('<III', seg, pos)
    pos += 12
    for _ in range(cnt + 1):
        off, ino_d, etype, esize = struct.unpack_from('<HHHH', seg, pos)
        pos += 8
        name = seg[pos:pos+esize+1]
        pos += esize + 1
        entries.append((name, (base_block << 16) | off, etype, base_ino + ino_d))
for nm, ref, et, ino in entries:
    print(nm, hex(ref), et, ino)
    if b'openwrt' in nm:
        target = ref
print('target ref:', hex(target) if 'target' in dir() else None)

# inode of openwrt_release
ib_ = inode_at(target)
print('inode bytes:', ib_[:64].hex(' '))
t = struct.unpack_from('<H', ib_, 0)[0]
print('type:', t)
if t == 2:
    mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', ib_, 2)
    start, frag, sparse, fsize = struct.unpack_from('<IIII', ib_, 16)
    print('mode=%o uid=%d gid=%d ino=%d start=%#x frag=%#x sparse=%d fsize=%d' % (mode, uid, gid, ino, start, frag, sparse, fsize))
elif t == 9:
    ino = struct.unpack_from('<Q', ib_, 0)[0]
    mode, uid, gid, mtime = struct.unpack_from('<HHHI', ib_, 10)
    start, frag = struct.unpack_from('<II', ib_, 20)
    fsize = struct.unpack_from('<Q', ib_, 28)[0]
    print('ext: ino=%d mode=%o start=%#x frag=%#x fsize=%d' % (ino, mode, start, frag, fsize))
    # try shifted-by-4 variants
    for shift in (4,):
        st2, fr2 = struct.unpack_from('<II', ib_, 20 + shift)
        fs2 = struct.unpack_from('<Q', ib_, 28 + shift)[0]
        print('  +%d: start=%#x frag=%#x fsize=%d' % (shift, st2, fr2, fs2))
