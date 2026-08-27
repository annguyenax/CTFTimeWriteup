import struct, lzma, re
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img", 'rb').read()

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return None

frag_idx = 0x383d80
w = struct.unpack_from('<H', data, frag_idx)[0]
frag_data = decomp(data[frag_idx+2: frag_idx+2+w])

# scan all fragment blocks for root lines and passwd/shadow content
for i in range(48):
    sb, csize, un = struct.unpack_from('<QII', frag_data, i*16)
    fblock = decomp(data[sb:sb+csize])
    if fblock is None:
        continue
    for m in re.finditer(rb'root:([^:\n]*):', fblock):
        print('frag %d root line: %r' % (i, fblock[max(0, m.start()-5):m.start()+80]))
    if b'shadow' in fblock[:40] or fblock.startswith(b'root:'):
        pass

# extracted files byte-check
for fn in (r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\sqfs_root\ROOT\etc\shadow",
           r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\sqfs_root\ROOT\etc\passwd"):
    b = open(fn, 'rb').read()
    print(fn.split('\\')[-1], repr(b[:120]))
