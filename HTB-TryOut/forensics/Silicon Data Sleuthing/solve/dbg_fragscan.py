import struct, lzma
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\squashfs.img", 'rb').read()

def decomp(b):
    try:
        return lzma.decompress(b)
    except Exception:
        return None

# fragment entries metadata block at 0x383d80
frag_idx = 0x383d80
w = struct.unpack_from('<H', data, frag_idx)[0]
frag_data = decomp(data[frag_idx+2: frag_idx+2+w])
print('frag entries decompressed:', len(frag_data))
needles = [b'DISTRIB', b'openwrt', b'22.', b'21.', b'23.', b'SNAPSHOT', b'r20']
for i in range(48):
    sb, csize, un = struct.unpack_from('<QII', frag_data, i*16)
    fblock = decomp(data[sb:sb+csize])
    if fblock is None:
        print('frag', i, 'decomp FAIL', hex(sb), csize)
        continue
    hits = []
    for nd in needles:
        if nd in fblock:
            hits.append(nd)
    if hits:
        print('frag', i, hex(sb), 'size', csize, 'decomp', len(fblock), 'hits', hits)
        for nd in (b'DISTRIB', b'openwrt', b'22.', b'21.'):
            j = fblock.find(nd)
            if j >= 0:
                print('   ctx:', fblock[max(0,j-30):j+60])
