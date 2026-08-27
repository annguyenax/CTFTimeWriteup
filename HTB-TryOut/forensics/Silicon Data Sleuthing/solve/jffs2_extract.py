#!/usr/bin/env python3
"""Minimal JFFS2 (raw) parser for chal_router_dump.bin.

Walks the raw flash dump linearly, collecting inode + dirent nodes
(keeping highest version per (ino) / (pino,name)), then reconstructs
the file tree, decompressing node payloads (zlib/rtime/none).
"""
import struct, sys, zlib, os

JFFS2_MAGIC = 0x1985
NODETYPE_DIRENT = 0x2001
NODETYPE_INODE = 0x2002
NODETYPE_CLEANMARKER = 0x2003
NODETYPE_PADDING = 0x2004
NODETYPE_SUMMARY = 0x2006
NODETYPE_XATTR = 0x2008
NODETYPE_XREF = 0x2009

COMPR_ZLIB = 6
COMPR_RTIME = 2
COMPR_NONE = 0
COMPR_ZERO = 1

def crc32(data, crc=0):
    # JFFS2 uses kernel crc32(seed,...): zlib.crc32(data, seed ^ 0xFFFFFFFF) ^ 0xFFFFFFFF
    return (zlib.crc32(data, crc ^ 0xFFFFFFFF) ^ 0xFFFFFFFF) & 0xffffffff

class Inode:
    __slots__ = ('ino','version','mode','isize','offset','csize','dsize','compr','data')

class Dirent:
    __slots__ = ('pino','version','ino','nsize','type','name')

def parse(data, start, end):
    inodes = {}
    dirents = {}
    pos = start
    n = 0
    skipped = 0
    while pos + 12 <= end:
        magic, ntype = struct.unpack_from('<HH', data, pos)
        if magic != JFFS2_MAGIC:
            pos += 1
            skipped += 1
            continue
        totlen = struct.unpack_from('<I', data, pos + 4)[0]
        if totlen < 12 or pos + totlen > end:
            pos += 2
            skipped += 1
            continue
        hdr = data[pos:pos + 12]
        if crc32(hdr[:8]) != struct.unpack_from('<I', hdr, 8)[0]:
            pos += 2
            skipped += 1
            continue
        if ntype == NODETYPE_INODE:
            if totlen < 68:
                pos += totlen; continue
            (ino, version, mode, uid, gid, isize, atime, mtime, ctime,
             offset, csize, dsize, compr, usercompr, flags) = struct.unpack_from('<IIIIIIIIIIIIBBH', data, pos + 12)
            node_crc = struct.unpack_from('<I', data, pos + 64)[0]
            # node_crc covers sizeof(ri)-8 = 60 bytes (data_crc at 60 not included)
            if crc32(data[pos:pos + 60]) != node_crc:
                pos += totlen; continue
            payload = data[pos + 68: pos + 68 + csize] if csize else b''
            cur = inodes.get(ino)
            if cur is None or version > cur.version:
                inodes[ino] = Inode()
                inodes[ino].ino = ino
                inodes[ino].version = version
                inodes[ino].mode = mode
                inodes[ino].isize = isize
                inodes[ino].offset = offset
                inodes[ino].csize = csize
                inodes[ino].dsize = dsize
                inodes[ino].compr = compr
                inodes[ino].data = payload
            n += 1
        elif ntype == NODETYPE_DIRENT:
            if totlen < 40:
                pos += totlen; continue
            (pino, version, ino, mctime, nsize, dtype) = struct.unpack_from('<IIIIBB', data, pos + 12)
            name = data[pos + 40: pos + 40 + nsize]
            node_crc = struct.unpack_from('<I', data, pos + 36)[0]
            name_crc = struct.unpack_from('<I', data, pos + 32)[0]
            if crc32(data[pos:pos + 32]) != node_crc or crc32(name) != name_crc:
                pos += totlen; continue
            key = (pino, name)
            cur = dirents.get(key)
            if cur is None or version > cur.version:
                d = Dirent(); d.pino = pino; d.version = version; d.ino = ino
                d.nsize = nsize; d.type = dtype; d.name = name
                dirents[key] = d
            n += 1
        pos += (totlen + 3) & ~3  # nodes are 4-byte aligned
    return inodes, dirents, skipped, pos

def decompress(inode):
    c = inode.compr
    d = inode.data
    if c == COMPR_NONE:
        return d
    if c == COMPR_ZLIB:
        try:
            return zlib.decompress(d)
        except Exception:
            return b'<zlib-error>'
    if c == COMPR_RTIME:
        return rtime_decompress(d, inode.dsize)
    if c == COMPR_ZERO:
        return b'\x00' * inode.dsize
    return b'<compr=%d>' % c

def rtime_decompress(data, dsize):
    out = bytearray()
    i = 0
    while i < len(data) and len(out) < dsize:
        if data[i] == 0:
            if i + 1 >= len(data): break
            count = data[i+1]
            if i + 2 >= len(data): break
            rep = data[i+2]
            out.extend(bytes([rep]) * count)
            i += 3
        else:
            out.append(data[i]); i += 1
    return bytes(out)

def build_tree(inodes, dirents):
    # directory ino -> list of (name, target_ino, type)
    tree = {1: []}
    seen = set()
    for (pino, name), d in dirents.items():
        if name in (b'.', b'..'):
            continue
        tree.setdefault(pino, []).append((name, d.ino, d.type))
        seen.add((pino, name))
    return tree

def fmt_mode(mode):
    import stat
    try:
        return stat.filemode(mode)
    except Exception:
        return '%o' % mode

def main():
    path = sys.argv[1]
    outdir = sys.argv[2]
    data = open(path, 'rb').read()
    # find JFFS2 start: first occurrence of magic 0x85 0x19
    idx = data.find(b'\x85\x19')
    print('first JFFS2 magic at 0x%X' % idx)
    # Use the first *valid* node header as the region start (avoid false positives)
    pos = idx
    while pos < len(data) - 12:
        if data[pos:pos+2] == b'\x85\x19':
            t = struct.unpack_from('<I', data, pos + 4)[0]
            if 12 <= t <= 8192 and crc32(data[pos:pos+8]) == struct.unpack_from('<I', data, pos + 8)[0]:
                break
        pos += 2
    print('valid JFFS2 region start at 0x%X' % pos)
    inodes, dirents, skipped, lastpos = parse(data, pos, len(data))
    print('inodes=%d dirents=%d skipped=%d last node at 0x%X' % (len(inodes), len(dirents), skipped, lastpos))
    tree = build_tree(inodes, dirents)

    def walk(ino, path):
        for name, tino, dtype in tree.get(ino, []):
            if tino not in inodes:
                continue
            inode = inodes[tino]
            full = os.path.join(path, name.decode('latin1'))
            if dtype == 2:  # directory
                os.makedirs(full, exist_ok=True)
                walk(tino, full)
            else:
                content = decompress(inode)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, 'wb') as f:
                    f.write(content)
                if len(content) < 4096:
                    print('  %s (%d bytes) compr=%d' % (full, len(content), inode.compr))
    walk(1, outdir)

if __name__ == '__main__':
    main()
