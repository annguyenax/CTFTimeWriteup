#!/usr/bin/env python3
"""Targeted ext2 extraction: /opt/router-web-panel/* and init scripts."""
import struct, sys, os

def load(path):
    data = open(path, 'rb').read()
    sb = data[1024:2048]
    s_log_block_size = struct.unpack_from('<I', sb, 24)[0]
    s_blocks_per_group = struct.unpack_from('<I', sb, 32)[0]
    s_inodes_per_group = struct.unpack_from('<I', sb, 40)[0]
    s_inode_size = struct.unpack_from('<H', sb, 88)[0] or 128
    s_blocks_count = struct.unpack_from('<I', sb, 4)[0]
    block_size = 1024 << s_log_block_size
    groups = (s_blocks_count + s_blocks_per_group - 1) // s_blocks_per_group
    gd_offset = 2048 if block_size >= 1024 else 1024
    gd = []
    for g in range(groups):
        off = gd_offset + g * 32
        gd.append(struct.unpack_from('<III', data, off))  # bitmap, ibitmap, itable

    def read_block(b):
        return data[b * block_size:(b + 1) * block_size]

    def inode(num):
        g = (num - 1) // s_inodes_per_group
        idx = (num - 1) % s_inodes_per_group
        off = gd[g][2] * block_size + idx * s_inode_size
        ino = data[off:off + s_inode_size]
        mode = struct.unpack_from('<H', ino, 0)[0]
        size = struct.unpack_from('<I', ino, 4)[0]
        ib = list(struct.unpack_from('<15I', ino, 40))
        return mode, size, ib

    def contents(ib, size):
        out = b''
        for b in ib[:12]:
            if not b: continue
            out += read_block(b)
            if len(out) >= size: return out[:size]
        if ib[12]:
            for b in struct.unpack('<%dI' % (block_size // 4), read_block(ib[12])):
                if not b: continue
                out += read_block(b)
                if len(out) >= size: return out[:size]
        if ib[13]:  # double indirect
            for b in struct.unpack('<%dI' % (block_size // 4), read_block(ib[13])):
                if not b: continue
                for b2 in struct.unpack('<%dI' % (block_size // 4), read_block(b)):
                    if not b2: continue
                    out += read_block(b2)
                    if len(out) >= size: return out[:size]
        return out[:size]

    def lookup(dir_ino, name):
        mode, size, ib = inode(dir_ino)
        blob = contents(ib, size)
        off = 0
        while off + 9 <= len(blob):
            inum, rec_len, name_len, ftype = struct.unpack_from('<IHBB', blob, off)
            if rec_len == 0: break
            nm = blob[off + 8:off + 8 + name_len].decode('latin1', 'replace')
            if nm == name:
                return inum
            off += rec_len
        return None

    def extract(dir_ino, prefix):
        mode, size, ib = inode(dir_ino)
        blob = contents(ib, size)
        off = 0
        out = []
        while off + 9 <= len(blob):
            inum, rec_len, name_len, ftype = struct.unpack_from('<IHBB', blob, off)
            if rec_len == 0: break
            nm = blob[off + 8:off + 8 + name_len].decode('latin1', 'replace')
            if nm not in ('.', '..'):
                m, s, i2 = inode(inum)
                out.append((prefix + '/' + nm, inum, m, s))
            off += rec_len
        return out

    return lookup, extract, inode, contents

if __name__ == '__main__':
    lookup, extract, inode, contents = load(sys.argv[1])
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    # /opt
    opt = lookup(2, 'opt')
    # /opt/router-web-panel
    rwp = lookup(opt, 'router-web-panel')
    print('opt inode', opt, 'rwp inode', rwp)
    for p, num, m, s in extract(rwp, '/opt/router-web-panel'):
        print(p, hex(m), s)
        if m & 0xF000 == 0x8000:
            _, _, ib = inode(num)
            blob = contents(ib, s)
            fn = os.path.join(outdir, p.lstrip('/').replace('/', '_'))
            with open(fn, 'wb') as f:
                f.write(blob[:s])
            print('  ->', fn)
    # init scripts
    etc = lookup(2, 'etc')
    initd = lookup(etc, 'init.d')
    for p, num, m, s in extract(initd, '/etc/init.d'):
        if 'router' in p:
            _, _, ib = inode(num)
            blob = contents(ib, s)
            fn = os.path.join(outdir, p.lstrip('/').replace('/', '_'))
            with open(fn, 'wb') as f:
                f.write(blob[:s])
            print('script ->', fn)
    # /usr/bin/router-web-panel binary
    usr = lookup(2, 'usr')
    usrbin = lookup(usr, 'bin')
    n = lookup(usrbin, 'router-web-panel')
    if n:
        _, s, ib = inode(n)
        blob = contents(ib, s)
        with open(os.path.join(outdir, 'router-web-panel.bin'), 'wb') as f:
            f.write(blob[:s])
        print('binary ->', os.path.join(outdir, 'router-web-panel.bin'), 'size', s)
    # /opt/router-web-panel/templates/*
    tdir = lookup(rwp, 'templates')
    if tdir:
        for p, num, m, s in extract(tdir, '/templates'):
            if m & 0xF000 == 0x8000:
                _, _, ib = inode(num)
                blob = contents(ib, s)
                fn = os.path.join(outdir, 'tpl_' + p.rsplit('/', 1)[-1])
                with open(fn, 'wb') as f:
                    f.write(blob[:s])
                print('template ->', fn)
    # /etc/passwd, /etc/shadow
    for name in ('passwd', 'shadow'):
        n = lookup(etc, name)
        if n:
            _, _, ib = inode(n)
            _, s, _ = inode(n)
            blob = contents(ib, s)
            with open(os.path.join(outdir, name), 'wb') as f:
                f.write(blob[:s])
            print('etc/%s -> saved' % name)
