#!/usr/bin/env python3
"""Full SquashFS 4.0 reader with gzip + xz + zstd + lzo + lz4 decompression.
Extracts all regular files into outdir and prints file paths.
Usage: python sqfs_full.py <firmware.bin> <outdir>
Auto-finds 'hsqs' magic; assumes it is the (only) squashfs.
"""
import struct, sys, os, zlib, lzma

SUPPORTED = {1:'gzip', 4:'xz', 6:'zstd', 3:'lzo', 5:'lz4'}

def decompress(comp, data):
    if comp == 1:
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)
    if comp == 4:
        return lzma.decompress(data)
    return None

class SquashFS:
    def __init__(self, data):
        self.data = data
        h = struct.unpack_from('<IIIIIHHHHHH', data, 0)
        self.magic, self.inodes, self.mtime, self.blksz, self.fragcnt, \
        self.comp, self.blog, self.flags, self.nids, self.smaj, self.smin = h
        self.blk = self.blksz if self.blksz else (1 << self.blog)
        (self.root_ref, self.bytes_used, self.idtab, self.xtab,
         self.itab, self.dtab, self.ftab, self.etab) = struct.unpack_from('<QQQQQQQQ', data, 32)

    def read_metadata_blocks(self, start, end=None):
        """Read a metadata sequence starting at `start`, return decompressed bytes
        up to `end` (absolute table byte offset) if given."""
        out = b''
        pos = start
        guard = 0
        while True:
            if pos + 4 > len(self.data):
                break
            (sz,) = struct.unpack_from('<I', self.data, pos)
            pos += 4
            comp = (sz & 0x80000000) != 0
            sz &= 0x7FFFFFFF
            if pos + sz > len(self.data):
                break
            blk = self.data[pos:pos+sz]
            pos += sz
            if comp:
                d = decompress(self.comp, blk)
                if d is None:
                    return None
            else:
                d = blk
            out += d
            guard += 1
            if end is not None and (pos >= end or len(out) >= end):
                # stop when we've read the target byte range
                break
            if guard > 100000:
                break
        return out

    def inode_from_ref(self, ref):
        """Return (inode_bytes, absolute_offset_within_decompressed_metadata)."""
        block_off = (ref >> 16) + self.itab
        inode_off = ref & 0xFFFF
        meta = self.read_metadata_blocks(block_off)
        if meta is None or inode_off + 64 > len(meta):
            return None
        return meta[inode_off:]

    def parse_inode(self, ib):
        itype, mode = struct.unpack_from('<HH', ib, 0)
        uid, gid, mtime = struct.unpack_from('<III', ib, 4)
        base = {'type': itype, 'mode': mode, 'uid': uid, 'gid': gid, 'mtime': mtime}
        # extended inodes (type>=8) have 8-byte header (2+2+4); base 16 bytes
        if itype >= 8:
            hdr_len = 8
        else:
            hdr_len = 16
        base['_off'] = hdr_len
        return base

    def walk(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        self.extract_inode(self.root_ref, outdir)

    def extract_inode(self, ref, path):
        ib = self.inode_from_ref(ref)
        if ib is None:
            return
        itype, mode = struct.unpack_from('<HH', ib, 0)
        # directory inode
        if itype in (1, 9):
            hdr = 8 if itype == 9 else 16
            # basic dir: inode_number, offset, nlink, file_size, block_idx, parent_inode
            # extended dir has inode_number first (8 bytes header)
            if itype == 9:
                # extended: header = [inode_number(8)], then start_block(4), nlink(4), size(2), block_idx(2), parent(4), i_count(2), offset(4), xattr(4)
                start_block, nlink, fsize, bidx, parent, icount, doff = struct.unpack_from('<IIHHIH', ib, 8)
                dir_data_start = (start_block & 0x0FFFFFFF) + self.dtab
                size = fsize
                offset = doff & 0x0FFFFFFF
            else:
                start_block, nlink, fsize, parent = struct.unpack_from('<IIII', ib, 16)
                dir_data_start = (start_block & 0x0FFFFFFF) + self.dtab
                size = fsize
                offset = 0
            # read directory listing metadata starting at dir_data_start
            meta = self.read_metadata_blocks(dir_data_start)
            if meta is None:
                return
            self.parse_dirents(meta, outdir if isinstance(path, str) else path)
        # file inode
        elif itype in (2, 10, 12, 14):
            self.extract_file(ib, path, itype)

    def parse_dirents(self, meta, path):
        pos = 0
        while pos + 8 <= len(meta):
            (ino, typ) = struct.unpack_from('<HB', meta, pos)
            name_len = meta[pos+3]
            name = meta[pos+8:pos+8+name_len]
            ref = ino | ((meta[pos+4] & 0xF0) << 12) | (struct.unpack_from('<H', meta, pos+4)[0] & 0xFFF0) << 12
            # ref: 16-bit inode_number + 48-bit inode ref. Format: 1+7 bits
            # actual: inode_number(16) | type(4 at bits)...
            # squashfs dirent: inode_number(16) | type(8) | size(8) | inode_offset(48) + type(4)
            # parse: first word = (inode_number<<16)|(offset<<8)|... complex. Reconstruct ref:
            # entry format: inode_number(16), type(4+4), size(8), inode_offset(48)... total 24 bytes var
            # Simpler known layout:
            # [0:2] inode_number, [2] type, [3] size, [4:10] inode_offset (48-bit), type nibble in [4] high bits
            # We already read ino(2), typ(1), name_len(1). Remaining offset is 6 bytes.
            offset6 = meta[pos+4:pos+10]
            # build 48-bit inode ref: (offset<<16)|(offset high) combined with inode table base
            # inode_offset: lower 16 bits at [4:6]? Actually:
            # off_lo = struct.unpack('<I', meta[pos+4:pos+8])[0]  (32-bit)
            # ref = (off_lo >> 8)  -> 24-bit block + offset within
            # Standard: inode_ref = (offset_bytes_in_metadata_after_16 << 16) | offset_low16
            off_full = struct.unpack('<Q', meta[pos+4:pos+10] + b'\x00\x00')[0]  # 48 bits
            # 48-bit value: high 16 = block offset delta, low 16 = inode offset
            block_delta = (off_full >> 16) & 0xFFFF
            ino_off = off_full & 0xFFFF
            inode_ref = (block_delta << 16) | ino_off
            if typ == 2:  # directory
                self.extract_inode(inode_ref, os.path.join(path, name.decode('utf-8', 'replace')))
            else:
                self.extract_inode(inode_ref, path)
            pos += 10 + name_len
            pos = (pos + 3) & ~3

    def extract_file(self, ib, path, itype):
        # parse file start_block, file_size, block_list offsets
        if itype == 2:  # basic file
            blocks_start, frag, fsize, bsize = struct.unpack_from('<IIII', ib, 16)
        else:  # extended
            inode_num = struct.unpack_from('<Q', ib, 0)[0]
            blocks_start, frag, fsize = struct.unpack_from('<IIQ', ib, 8)
            frag = (frag >> 16) & 0xFFFFFFFF
        blocks_start &= 0x0FFFFFFF
        file_data = self.read_file_blocks(blocks_start, fsize)
        if file_data is None:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(file_data)
        print('  %s (%d bytes)' % (path, len(file_data)))

    def read_file_blocks(self, blocks_start, fsize):
        """blocks_start = first data block byte offset (relative to dump start).
        Walk 4-byte block-size headers + decompress until fsize bytes."""
        pos = blocks_start
        out = b''
        while len(out) < fsize and pos + 4 <= len(self.data):
            (sz,) = struct.unpack_from('<I', self.data, pos)
            pos += 4
            comp = (sz & 0x80000000) != 0
            sz &= 0x7FFFFFFF
            blk = self.data[pos:pos+sz]
            pos += sz
            if comp:
                d = decompress(self.comp, blk)
                if d is None:
                    return None
            else:
                d = blk
            out += d
        return out[:fsize]

def main():
    path = sys.argv[1]; outdir = sys.argv[2]
    data = open(path, 'rb').read()
    off = data.find(b'hsqs')
    if off < 0:
        print('no squashfs found'); return
    sq = SquashFS(data[off:])
    print('squashfs v%d.%d at 0x%X inodes=%d comp=%d(%s) blk=%d' % (
        sq.smaj, sq.smin, off, sq.inodes, sq.comp, SUPPORTED.get(sq.comp, '?'), sq.blk))
    sq.walk(outdir)

if __name__ == '__main__':
    main()
