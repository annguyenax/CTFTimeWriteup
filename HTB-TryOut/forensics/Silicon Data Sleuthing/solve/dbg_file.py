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

for name, off in [('board_detect', 31), ('busybox', 63), ('ipcalc.sh', None)]:
    seg = istream[off:off+40]
    print(name, 'ino bytes:', seg.hex(' '))
    t = struct.unpack_from('<H', seg, 0)[0]
    mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', seg, 2)
    start, frag, fsize, blist = struct.unpack_from('<IIII', seg, 16)
    print('  type=%d mode=%o ino=%d start_block=%#x frag=%#x fsize=%d blist_off=%d' % (t, mode, ino, start, frag, fsize, blist))
    print('  frag idx=%d frag_off=%d' % (frag & 0xffff, (frag >> 16) & 0xffffffff))

print()
for m in [0x26dfc, 0x2cf3c, 0x3a7c8, 0x4497c]:
    u16 = struct.unpack_from('<H', data, m-2)[0]
    u32 = struct.unpack_from('<I', data, m-4)[0]
    print('  %#x: u16@-2=%#x u32@-4=%#x' % (m, u16, u32))
