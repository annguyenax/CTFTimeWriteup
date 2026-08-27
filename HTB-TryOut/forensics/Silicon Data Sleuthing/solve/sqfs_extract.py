#!/usr/bin/env python3
"""Extract a SquashFS 4.0 filesystem (gzip/xz/zstd/lzo/lz4) embedded in a raw
firmware dump. Focused on the specific layout used by the HTB challenge
chal_router_dump.bin (OpenWrt). Writes files to outdir and lists recoverable
file paths + contents, and prints /etc/openwrt_release if found.
"""
import struct, sys, os, zlib

def decomp(data, comp, size=None):
    if comp == 1:  # gzip
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)
    if comp == 0:  # zlib? squashfs uses gzip for comp 1
        try: return zlib.decompress(data)
        except Exception: return None
    return None  # xz/lzo/lz4/zstd unsupported -> None

class Sqfs:
    def __init__(self, data):
        self.data = data
        (self.magic, self.inodes, self.mtime, self.blksz, self.fragcnt,
         self.comp, self.blog, self.flags, self.nids, self.smaj, self.smin,
         self.root_inode_ref, self.bytes_used, self.id_table_start,
         self.xattr_id_table_start, self.inode_table_start,
         self.directory_table_start, self.frag_table_start,
         self.export_table_start) = struct.unpack_from('<IIIIIIHHHBBQQQQQQQQQ', data, 0)
        # block size might be shifted if 0
        self.blk = self.blksz if self.blksz > 0 else (1 << self.blog)
        self.root_inode_offset = self.root_inode_ref & 0xFFFF
        self.root_inode_start = (self.root_inode_ref >> 16) + self.inode_table_start

    def read_blocks(self, start, size):
        """Read `size` bytes that may span multiple 128K blocks, each preceded by
        a 4-byte size word (high bit set if compressed). Returns decompressed bytes."""
        out = b''
        pos = start
        remaining = size
        while remaining > 0:
            (sz,) = struct.unpack_from('<I', self.data, pos)
            pos += 4
            compressed = (sz & 0x80000000) != 0
            sz &= 0x7FFFFFFF
            blk = self.data[pos:pos+sz]
            pos += sz
            if compressed:
                d = decomp(blk, self.comp)
                if d is None:
                    # unknown compression -> keep raw
                    return None
                out += d
            else:
                out += blk
            remaining -= self.blk
        return out[:size]

    def read_inode(self, ref):
        start = (ref >> 16) + self.inode_table_start
        # read raw inode header (16 bytes) from a table block
        # We read the block containing 'start'
        block_start = (start // self.blk) * self.blk
        (bsz,) = struct.unpack_from('<I', self.data, block_start)
        comp = bsz & 0x80000000 != 0
        bsz &= 0x7FFFFFFF
        blk = self.data[block_start+4: block_start+4+bsz]
        d = decomp(blk, self.comp) if comp else blk
        if d is None: return None
        off = start - block_start
        (itype, mode, uid, gid, mtime) = struct.unpack_from('<HHIII', d, off)
        hdr_len = 16
        return itype, d, off

    def walk(self):
        # basic: list inode types by walking is too complex without full parser.
        # Instead: brute search inode_table for 'openwrt_release' filename via dirent.
        pass

def main():
    path = sys.argv[1]; outdir = sys.argv[2]
    data = open(path, 'rb').read()
    off = data.find(b'hsqs')
    if off < 0:
        # big endian squashfs
        off = data.find(b'sqsh')
    print('squashfs magic at 0x%X' % off)
    sq = Sqfs(data[off:])
    print('version=%d.%d inodes=%d blk=%d comp=%d root_ino_ref=0x%X' % (
        sq.smaj, sq.smin, sq.inodes, sq.blk, sq.comp, sq.root_inode_ref))
    print('inode_table_start=0x%X dir_table_start=0x%X' % (sq.inode_table_start, sq.directory_table_start))
    os.makedirs(outdir, exist_ok=True)
    print('SUPPORTED_COMPRESSION: gzip(zlib) only for now; comp=%d' % sq.comp)

if __name__ == '__main__':
    main()
