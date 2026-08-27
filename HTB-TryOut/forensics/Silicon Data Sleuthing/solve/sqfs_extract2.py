#!/usr/bin/env python3
"""SquashFS 4.0 (xz, u16 metadata size words variant) full extractor.
Walks dirs, reads files (blocks + fragments), dumps /etc/openwrt_release.
"""
import struct, lzma, sys, os

IMG = sys.argv[1] if len(sys.argv) > 1 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\sqfs_root"
data = open(IMG, 'rb').read()

magic, inodes, mtime, blksz, fragcnt, comp, blog, flags, nids, smaj, smin = \
    struct.unpack_from('<IIIIIHHHHHH', data, 0)
root_ref, bytes_used, idtab, xtab, itab, dtab, ftab, etab = \
    struct.unpack_from('<QQQQQQQQ', data, 32)

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return None

def meta_blocks(start, end):
    pos = start
    while pos + 2 <= end and pos < len(data):
        (sz,) = struct.unpack_from('<H', data, pos)
        if sz == 0:
            break
        raw = data[pos+2:pos+2+sz]
        if len(raw) < sz:
            break
        yield pos, raw
        pos += 2 + sz
        if pos >= end:
            break

# ---- decompress inode + dir streams (dir table ends where frag index begins) ----
istream = b''
iblock = []   # (size_word_off_rel_itab, stream_off, len)
for w, raw in meta_blocks(itab, dtab):
    d = decomp(raw)
    if d is None:
        print('FAIL inode block', hex(w)); sys.exit(1)
    iblock.append((w - itab, len(istream), len(d)))
    istream += d

# dir table: walk until the fragment-index u64 region; find end by xz-magic scan.
# fragment index sits at ftab (raw u64). dir table's last block ends at the
# metadata block whose size word is at the fragment index value.
frag_idx = struct.unpack_from('<Q', data, ftab)[0]
dtab_end = frag_idx  # byte offset where fragment entries metadata block begins
dstream = b''
dblock = []
for w, raw in meta_blocks(dtab, dtab_end):
    d = decomp(raw)
    if d is None:
        print('FAIL dir block', hex(w)); sys.exit(1)
    dblock.append((w - dtab, len(dstream), len(d)))
    dstream += d

print(f"inode blocks: {[(hex(w), s, l) for w, s, l in iblock]}")
print(f"dir blocks:   {[(hex(w), s, l) for w, s, l in dblock]}")
print(f"fragment idx @ {ftab:#x} -> entries block at {frag_idx:#x}")

def inode_at(ref):
    hi, lo = ref >> 16, ref & 0xFFFF
    for (w, s, l) in iblock:
        if w == hi and lo + 4 <= l:
            return istream[s+lo:]
    return None

def dir_block_at(off, rel='dtab'):
    blocks = dblock if rel == 'dtab' else iblock
    stream = dstream if rel == 'dtab' else istream
    for (w, s, l) in blocks:
        if w == off:
            return stream[s:s+l]
    return None

def parse_inode(ib):
    t = struct.unpack_from('<H', ib, 0)[0]
    r = {'type': t}
    if t in (1, 2, 3, 4, 5, 6, 7):
        mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', ib, 2)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino)
        if t == 1:  # basic dir
            start, nlink, fsize, off, parent = struct.unpack_from('<IIHHI', ib, 16)
            r.update(start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                     offset=off, parent=parent)
        elif t == 2:  # basic reg
            start, frag, fsize, blist = struct.unpack_from('<IIII', ib, 16)
            r.update(start_block=start & 0x0FFFFFFF, frag=frag, fsize=fsize, blist=blist)
        elif t == 3:  # symlink
            nlink, tsize = struct.unpack_from('<II', ib, 16)
            r.update(nlink=nlink, tsize=tsize, target=ib[24:24+tsize])
    elif t in (8, 9, 10, 11, 12, 13, 14):
        ino = struct.unpack_from('<Q', ib, 0)[0]
        mode, uid, gid, mtime = struct.unpack_from('<HHHI', ib, 10)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino)
        if t == 8:  # ext dir
            start, nlink, fsize, off, parent, icount = struct.unpack_from('<IIHHIH', ib, 20)
            r.update(start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                     offset=off & 0x0FFFFFFF, parent=parent, icount=icount)
        elif t == 9:  # ext reg
            start, frag = struct.unpack_from('<II', ib, 20)
            fsize = struct.unpack_from('<Q', ib, 28)[0]
            sparse, nlink, blist, xattr = struct.unpack_from('<IIII', ib, 36)
            r.update(start_block=start & 0x0FFFFFFF, frag=frag, fsize=fsize,
                     blist=blist, sparse=sparse, nlink=nlink)
        elif t == 10:  # ext symlink
            nlink, tsize = struct.unpack_from('<II', ib, 20)
            r.update(nlink=nlink, tsize=tsize, target=ib[28:28+tsize])
    else:
        r['raw'] = ib[:24].hex()
    return r

def parse_listing(dirinfo):
    blk = dir_block_at(dirinfo['start_block'], 'dtab')
    if blk is None:
        return None, f"no dir block at {dirinfo['start_block']:#x}"
    entries = []
    pos = dirinfo['offset']
    end = len(blk)
    fsize = dirinfo['fsize']
    while pos + 12 <= end:
        cnt, base_block, base_ino = struct.unpack_from('<III', blk, pos)
        pos += 12
        for _ in range(cnt + 1):
            if pos + 8 > end:
                return entries, 'truncated-entry'
            off, ino_d, etype, esize = struct.unpack_from('<HHHH', blk, pos)
            pos += 8
            name = blk[pos:pos+esize+1]
            pos += esize + 1
            entries.append((name.decode('utf-8', 'replace'), (base_block << 16) | off,
                            etype, base_ino + ino_d))
    return entries, 'ok'

def read_file_data(finfo):
    """Return file bytes from a file inode dict."""
    fsize = finfo['fsize']
    frag = finfo['frag']
    frag_idx_n = frag & 0xFFFF
    frag_off = (frag >> 16) & 0xFFFFFFFF
    out = b''
    # data blocks
    if finfo['start_block'] != 0xFFFFFFF and finfo['start_block'] != 0:
        # block list: u16 entries (small files). Each entry: bit15? compressed flag + size
        nblocks = (fsize + blksz - 1) // blksz if fsize else 0
        bl = finfo['blist']
        # block list location: for basic reg it's right after the 32-byte header
        # we get raw inode bytes via finfo['_raw'] if provided
        raw = finfo['_raw']
        hdr = 32 if finfo['type'] == 2 else 52
        pos = finfo['start_block']
        for i in range(nblocks):
            entry = struct.unpack_from('<H', raw, hdr + 2*i)[0]
            csize = entry & 0x7FFF
            comp = (entry & 0x8000) == 0
            chunk = data[pos:pos+csize]
            if comp:
                d = decomp(chunk)
                out += d if d is not None else chunk
            else:
                out += chunk
            pos += csize
        out = out[:fsize]
    # fragment
    if frag_idx_n != 0xFFFF and len(out) < fsize:
        # read fragment entry
        frag_blk = frag_idx
        # fragment entries metadata block at frag_idx (decompressed 768 bytes)
        frag_data = decomp(data[frag_blk+2:frag_blk+2+struct.unpack_from('<H', data, frag_blk)[0]])
        sb, sz, un = struct.unpack_from('<QII', frag_data, frag_idx_n*16)
        # fragment data block at sb: [size word][xz data]
        w2 = struct.unpack_from('<H', data, sb-2)[0] if sb >= 2 else 0
        w4 = struct.unpack_from('<I', data, sb-4)[0] if sb >= 4 else 0
        # try u32 header at sb-4, else u16 at sb-2
        for (woff, wval, is_u32) in ((sb-4, w4, True), (sb-2, w2, False)):
            csize = wval & 0x7FFFFFFF if is_u32 else (wval & 0x7FFF)
            comp = (wval & (0x80000000 if is_u32 else 0x8000)) == 0
            blk = data[woff+4:woff+4+csize] if is_u32 else data[woff+2:woff+2+csize]
            d = decomp(blk) if comp else blk
            if d is not None and frag_off + len(out) < len(d) + 1:
                out += d[frag_off:frag_off + (fsize - len(out))]
                break
    return out

def walk_dir(ref, path, depth=0):
    ib = inode_at(ref)
    if ib is None:
        print('  '*depth + f'[no inode for ref {ref:#x}]')
        return
    info = parse_inode(ib)
    info['_raw'] = ib
    t = info['type']
    if t in (1, 8):  # dir
        entries, err = parse_listing(info)
        print('  '*depth + f'{path}/ (dir, ino={info["ino"]}, {len(entries) if entries else err})')
        for (name, cref, etype, ino) in (entries or []):
            walk_dir(cref, os.path.join(path, name), depth+1)
    elif t in (2, 9):  # file
        content = read_file_data(info)
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, 'wb') as f:
            f.write(content)
        print('  '*depth + f'{path} ({len(content)} bytes)')
    elif t in (3, 10):  # symlink
        print('  '*depth + f'{path} -> {info.get("target", b"?").decode("utf-8", "replace")} (symlink)')
    else:
        print('  '*depth + f'{path} (type {t})')

os.makedirs(OUT, exist_ok=True)
walk_dir(root_ref, os.path.join(OUT, 'ROOT'))
print('\n--- /etc/openwrt_release ---')
try:
    print(open(os.path.join(OUT, 'ROOT', 'etc', 'openwrt_release'), 'rb').read().decode())
except Exception as e:
    print('ERR', e)
