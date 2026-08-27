#!/usr/bin/env python3
"""SquashFS 4.0 (xz, u16 metadata size words, packed data blocks, u32 block list)
full extractor for the HTB 'Silicon Data Sleuthing' router dump.
"""
import struct, lzma, sys, os

IMG = sys.argv[1] if len(sys.argv) > 1 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\sqfs_root"
BLK = 262144
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

istream = b''
ib = []
for w, raw in meta_blocks(itab, dtab):
    d = decomp(raw)
    ib.append((w - itab, len(istream), len(d)))
    istream += d

frag_idx = struct.unpack_from('<Q', data, ftab)[0]
dstream = b''
db = []
for w, raw in meta_blocks(dtab, ftab):
    d = decomp(raw)
    db.append((w - dtab, len(dstream), len(d)))
    dstream += d

def stream_off(blocks, w_off):
    for (w, s, l) in blocks:
        if w == w_off:
            return s
    return None

def inode_at(ref):
    hi, lo = ref >> 16, ref & 0xFFFF
    for (w, s, l) in ib:
        if w == hi and lo + 8 <= l:
            return istream[s+lo:]
    return None

def parse_inode(ib):
    t = struct.unpack_from('<H', ib, 0)[0]
    r = {'type': t}
    if t in (1, 2, 3, 4, 5, 6, 7):
        mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHI', ib, 2)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino)
        if t == 1:
            start, nlink, fsize, off, parent = struct.unpack_from('<IIHHI', ib, 16)
            r.update(start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                     offset=off, parent=parent)
        elif t == 2:
            start, frag_idx, frag_off, fsize = struct.unpack_from('<IIII', ib, 16)
            r.update(start_block=start & 0x0FFFFFFF, frag=frag_idx, frag_off=frag_off, fsize=fsize)
        elif t == 3:
            nlink, tsize = struct.unpack_from('<II', ib, 16)
            r.update(nlink=nlink, tsize=tsize, target=ib[24:24+tsize])
    elif t in (8, 9, 10, 11, 12, 13, 14):
        ino = struct.unpack_from('<Q', ib, 0)[0]
        mode, uid, gid, mtime = struct.unpack_from('<HHHI', ib, 10)
        r.update(mode=mode, uid=uid, gid=gid, mtime=mtime, ino=ino)
        if t == 8:
            start, nlink, fsize, off, parent, icount = struct.unpack_from('<IIHHIH', ib, 20)
            r.update(start_block=start & 0x0FFFFFFF, nlink=nlink, fsize=fsize,
                     offset=off & 0x0FFFFFFF, parent=parent, icount=icount)
        elif t == 9:
            start, frag = struct.unpack_from('<II', ib, 20)
            fsize = struct.unpack_from('<Q', ib, 28)[0]
            r.update(start_block=start & 0x0FFFFFFF, frag=frag, fsize=fsize)
    return r

def parse_listing(dinfo):
    so = stream_off(db, dinfo['start_block'])
    if so is None:
        return None, 'no block'
    seg = dstream[so + dinfo['offset']: so + dinfo['offset'] + dinfo['fsize']]
    entries = []
    pos = 0
    while pos + 12 <= len(seg):
        cnt, base_block, base_ino = struct.unpack_from('<III', seg, pos)
        pos += 12
        for _ in range(cnt + 1):
            if pos + 8 > len(seg):
                return entries, 'truncated'
            off, ino_d, etype, esize = struct.unpack_from('<HHHH', seg, pos)
            pos += 8
            name = seg[pos:pos+esize+1]
            pos += esize + 1
            entries.append((name, (base_block << 16) | off, etype, base_ino + ino_d))
    return entries, 'ok'

def read_file(finfo):
    fsize = finfo['fsize']
    frag_n = finfo['frag'] & 0xFFFF
    frag_off = finfo.get('frag_off', (finfo['frag'] >> 16) & 0xFFFFFFFF)
    out = b''
    if finfo['start_block'] not in (0, 0xFFFFFFF):
        nblocks = (fsize >> blog) if frag_n != 0xFFFF else (fsize + BLK - 1) // BLK
        pos = finfo['start_block']
        for i in range(nblocks):
            entry = struct.unpack_from('<I', finfo['_raw'], 32 + 4*i)[0]
            comp = not (entry & 0x80000000)
            csize = entry & 0x7FFFFFFF
            chunk = data[pos:pos+csize]
            if comp:
                d = decomp(chunk)
                if d is None:
                    d = chunk
                out += d
            else:
                out += chunk
            pos += csize
        out = out[:fsize]
    if frag_n != 0xFFFF and len(out) < fsize:
        frag_data = decomp(data[frag_idx+2: frag_idx+2 + struct.unpack_from('<H', data, frag_idx)[0]])
        sb, csize, un = struct.unpack_from('<QII', frag_data, frag_n*16)
        fblock = decomp(data[sb:sb+csize])
        if fblock is None:
            fblock = data[sb:sb+csize]
        part = fblock[frag_off:frag_off + (fsize - len(out))]
        out += part
    return out[:fsize]

def walk(ref, path, depth=0):
    ib = inode_at(ref)
    if ib is None:
        print('  '*depth + f'[no inode {ref:#x}]')
        return
    info = parse_inode(ib)
    info['_raw'] = ib
    t = info['type']
    if t in (1, 8):
        entries, err = parse_listing(info)
        print('  '*depth + f'{path}/ ({len(entries) if entries else 0} entries)')
        for (nm, cref, etype, ino) in (entries or []):
            walk(cref, os.path.join(path, nm.decode('utf-8', 'replace')), depth+1)
    elif t in (2, 9):
        content = read_file(info)
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
        print('  '*depth + f'{path} ({len(content)} B)')
    elif t in (3, 10):
        print('  '*depth + f'{path} -> {info.get("target", b"?").decode("utf-8", "replace")}')
    else:
        print('  '*depth + f'{path} (type {t})')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    walk(root_ref, os.path.join(OUT, 'ROOT'))
    rel = os.path.join(OUT, 'ROOT', 'etc', 'openwrt_release')
    print('\n=== /etc/openwrt_release ===')
    try:
        print(open(rel, 'rb').read().decode())
    except Exception as e:
        print('ERR', e)
