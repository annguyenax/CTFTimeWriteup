#!/usr/bin/env python3
"""Probe SquashFS 4.0 (xz) layout: decompress inode+dir metadata streams,
resolve root inode ref encoding empirically, locate openwrt_release dirent."""
import struct, lzma, sys

IMG = sys.argv[1] if len(sys.argv) > 1 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img"
data = open(IMG, 'rb').read()
print("file size", len(data))

magic, inodes, mtime, blksz, fragcnt, comp, blog, flags, nids, smaj, smin = \
    struct.unpack_from('<IIIIIHHHHHH', data, 0)
root_ref, bytes_used, idtab, xtab, itab, dtab, ftab, etab = \
    struct.unpack_from('<QQQQQQQQ', data, 32)
print(f"magic={magic:08x} inodes={inodes} blksz={blksz} comp={comp} ver={smaj}.{smin}")
print(f"root_ref={root_ref:#x} bytes_used={bytes_used:#x}")
print(f"itab={itab:#x} dtab={dtab:#x} ftab={ftab:#x} etab={etab:#x} idtab={idtab:#x}")

def decomp(blk):
    return lzma.decompress(blk)

def read_meta_stream(start, end):
    out = b''
    blocks = []  # (file_off_of_size_word, compressed_size, decompressed_size)
    pos = start
    while pos + 4 <= len(data) and pos < end:
        (sz,) = struct.unpack_from('<I', data, pos)
        s0 = pos
        pos += 4
        comp = sz & 0x80000000
        sz &= 0x7FFFFFFF
        blk = data[pos:pos+sz]
        pos += sz
        if comp:
            d = decomp(blk)
        else:
            d = blk
        blocks.append((s0, sz, len(d)))
        out += d
        if len(out) > 64*1024*1024:
            break
    return out, blocks

istream, iblocks = read_meta_stream(itab, dtab)
dstream, dblocks = read_meta_stream(dtab, ftab)
print(f"inode stream: {len(istream)} bytes, {len(iblocks)} blocks, last block file_off={iblocks[-1][0]:#x}")
print(f"dir stream:   {len(dstream)} bytes, {len(dblocks)} blocks, last block file_off={dblocks[-1][0]:#x}")

# block boundaries in decompressed stream
boundaries = []
so = 0
for (foff, csz, dsz) in iblocks:
    boundaries.append((foff, so, dsz))
    so += dsz
print("inode block boundaries:", [(hex(f), s, d) for f, s, d in boundaries])

def parse_inode_at(buf, off):
    """Try to parse inode header at buf[off:]. Return dict or None."""
    if off + 16 > len(buf):
        return None
    t = struct.unpack_from('<H', buf, off)[0]
    if t in (1, 2, 3, 4, 5, 6, 7):
        # basic: type,mode,uid,guid,mtime,inode_number
        mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', buf, off+2)
        return dict(kind='basic', type=t, mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino)
    if t in (8, 9, 10, 11, 12, 13, 14):
        # extended: inode_number u64 then type
        ino = struct.unpack_from('<Q', buf, off)[0]
        mode, uid, gid, mtime = struct.unpack_from('<HHHI', buf, off+10)
        return dict(kind='ext', type=t, ino=ino, mode=mode, uid=uid, gid=gid, mtime=mtime)
    return None

ref = root_ref
hi = ref >> 16
lo = ref & 0xFFFF
print(f"\nroot_ref hi(16)={hi:#x} lo(16)={lo:#x}")

cands = {}
# I1: stream offset = hi
cands['I1 stream_off=hi'] = (istream, hi)
# I2: block file offset = itab+hi, inode at lo within decompressed block
for (foff, s_off, dsz) in boundaries:
    if foff == itab + hi:
        cands['I2 block_file=itab+hi @lo'] = (istream[s_off:s_off+dsz], lo)
        break
else:
    print("I2: no block with file offset itab+hi =", hex(itab+hi))
# I3: block containing stream offset hi (first block with s_off+dsz > hi), inode at (hi - s_off)
for (foff, s_off, dsz) in boundaries:
    if s_off + dsz > hi:
        cands['I3 block_containing_hi @(hi-s_off)'] = (istream[s_off:s_off+dsz], hi - s_off)
        break
# I4: block containing stream offset hi, inode at lo
for (foff, s_off, dsz) in boundaries:
    if s_off + dsz > hi:
        cands['I4 block_containing_hi @lo'] = (istream[s_off:s_off+dsz], lo)
        break
# I5: stream offset hi but low16=lo added? inode at hi (basic dirs have ino at 16)
cands['I1b'] = (istream, hi)

for name, (buf, off) in cands.items():
    p = parse_inode_at(buf, off)
    print(f"{name}: offset {off} -> {p}")

# Search dir stream for openwrt names
import re
for needle in (b'openwrt_release', b'openwrt_version', b'openwrt_banner', b'DISTRIB_'):
    idx = 0
    found = []
    while True:
        i = dstream.find(needle, idx)
        if i < 0:
            break
        found.append(i)
        idx = i + 1
    print(f"dirstream {needle}: {[hex(x) for x in found[:10]]}")
    for i in found[:3]:
        print("   ctx:", dstream[max(0,i-48):i+32])
# also inode stream
for needle in (b'openwrt_release', b'DISTRIB_'):
    i = istream.find(needle)
    print(f"inodestream {needle}: {hex(i) if i>=0 else None}")
