#!/usr/bin/env python3
"""Correct SquashFS 4.0 (xz, 2-byte metadata size words variant) reader.
Extracts /etc/openwrt_release + /etc/openwrt_version and walks the tree.
"""
import struct, lzma, sys, os

IMG = sys.argv[1] if len(sys.argv) > 1 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img"
data = open(IMG, 'rb').read()

magic, inodes, mtime, blksz, fragcnt, comp, blog, flags, nids, smaj, smin = \
    struct.unpack_from('<IIIIIHHHHHH', data, 0)
root_ref, bytes_used, idtab, xtab, itab, dtab, ftab, etab = \
    struct.unpack_from('<QQQQQQQQ', data, 32)

def meta_blocks(start, end):
    """Yield (size_word_offset, compressed_len, raw_compressed) metadata blocks
    from `start` until `end` (exclusive). Uses u16 size words (this variant)."""
    pos = start
    while pos + 2 <= end and pos < len(data):
        (sz,) = struct.unpack_from('<H', data, pos)
        if sz == 0:
            break
        raw = data[pos+2:pos+2+sz]
        if len(raw) < sz:
            break
        yield pos, sz, raw
        pos += 2 + sz
        if pos >= end:
            break

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return b  # assume stored uncompressed

# Build decompressed inode table stream with per-block info
istream = b''
iblock_off = []   # (size_word_file_off, decompressed_stream_off, decompressed_len)
for (w_off, csz, raw) in meta_blocks(itab, dtab):
    d = decomp(raw)
    iblock_off.append((w_off, len(istream), len(d)))
    istream += d

dstream = b''
dblock_off = []
for (w_off, csz, raw) in meta_blocks(dtab, ftab):
    d = decomp(raw)
    dblock_off.append((w_off, len(dstream), len(d)))
    dstream += d

print(f"inode stream: {len(istream)} bytes, blocks: {[(hex(w), s, l) for w, s, l in iblock_off]}")
print(f"dir stream:   {len(dstream)} bytes, blocks: {[(hex(w), s, l) for w, s, l in dblock_off]}")

def inode_bytes(ref):
    """Return raw inode bytes for a 32-bit style ref:
       hi16 = byte offset of metadata size word rel. to itab, lo16 = offset in block."""
    hi, lo = ref >> 16, ref & 0xFFFF
    for (w_off, s_off, dlen) in iblock_off:
        if w_off - itab == hi:
            blk = istream[s_off:s_off+dlen]
            if lo + 4 <= len(blk):
                return blk[lo:]
    # fallback: locate by walking stream offsets
    for (w_off, s_off, dlen) in iblock_off:
        if s_off <= hi < s_off + dlen:
            blk = istream[s_off:s_off+dlen]
            off = hi - s_off
            if off + 4 <= len(blk):
                return blk[off:]
    return None

def parse_inode(ib):
    t = struct.unpack_from('<H', ib, 0)[0]
    r = {'type': t}
    if t == 1:  # basic dir
        mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', ib, 2)
        start, nlink, fsize, off, parent = struct.unpack_from('<IIHHI', ib, 16)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino,
                 start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                 offset=off, parent=parent)
    elif t == 2:  # basic reg
        mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', ib, 2)
        start, frag, fsize, blist = struct.unpack_from('<IIII', ib, 16)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino,
                 start_block=start & 0x0FFFFFFF, frag=frag, fsize=fsize, blist=blist)
    elif t == 8:  # ext dir
        ino = struct.unpack_from('<Q', ib, 0)[0]
        mode, uid, gid, mtime = struct.unpack_from('<HHHI', ib, 10)
        start, nlink, fsize, off, parent, icount = struct.unpack_from('<IIHHIH', ib, 20)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino,
                 start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                 offset=off & 0x0FFFFFFF, parent=parent, icount=icount)
    elif t == 9:  # ext reg
        ino = struct.unpack_from('<Q', ib, 0)[0]
        mode, uid, gid, mtime = struct.unpack_from('<HHHI', ib, 10)
        start, frag = struct.unpack_from('<II', ib, 20)
        fsize = struct.unpack_from('<Q', ib, 28)[0]
        sparse, nlink, blist, xattr = struct.unpack_from('<IIII', ib, 36)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino,
                 start_block=start & 0x0FFFFFFF, frag=frag, fsize=fsize,
                 blist=blist, sparse=sparse, nlink=nlink, xattr=xattr)
    else:
        r.update(raw=ib[:32].hex())
    return r

# ---- root inode ----
rib = inode_bytes(root_ref)
print(f"\nroot ref {root_ref:#x}: raw head = {rib[:16].hex() if rib else None}")
ri = parse_inode(rib) if rib else None
print("root inode:", ri)

def dir_listing(r):
    """Return list of (name, child_ref, child_type) for dir inode r."""
    start = r['start_block'] + dtab if False else r['start_block']
    # dir data: metadata block at byte offset `start_block` rel. to dtab, offset `offset`
    for (w_off, s_off, dlen) in dblock_off:
        if w_off - dtab == start:
            blk = dstream[s_off:s_off+dlen]
            break
    else:
        return None, f"no block for start {start:#x}"
    off = r['offset']
    entries = []
    pos = off
    while pos + 12 <= len(blk):
        cnt, dh_start, dh_ino = struct.unpack_from('<III', blk, pos)
        pos += 12
        for _ in range(cnt + 1):
            if pos + 8 > len(blk):
                return entries, 'truncated'
            e_off, e_ino, e_type, e_size = struct.unpack_from('<HHHH', blk, pos)
            pos += 8
            name = blk[pos:pos+e_size-1]
            pos += e_size
            pos = (pos + 3) & ~3
            # child inode ref: high16 = dir header start_block?? derive below
            entries.append((name.decode('utf-8', 'replace'), e_off, e_type, dh_start, e_ino))
        if pos >= len(blk) or len(entries) > 500:
            break
    return entries, 'ok'

entries, err = dir_listing(ri) if ri else (None, 'no root inode')
print(f"root listing err={err}")
if entries:
    for e in entries[:30]:
        print("  ", e)
