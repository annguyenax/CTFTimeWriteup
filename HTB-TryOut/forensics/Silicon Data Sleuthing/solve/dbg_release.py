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
sb, csize, un = struct.unpack_from('<QII', frag_data, 1*16)
fblock = decomp(data[sb:sb+csize])
print('frag1 block decompressed:', len(fblock))

# release file: starts with DISTRIB_ID='OpenWrt'
i = fblock.find(b"DISTRIB_ID='OpenWrt'")
print('release text at offset', i)
release = fblock[i:i+216]
print(release.decode('utf-8', 'replace'))
open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\openwrt_release.txt", 'wb').write(release)

# version file: 18 bytes - look for '23.05.0'
for m in re.finditer(rb'23\.05\.0', fblock):
    j = m.start()
    print('23.05.0 at', j, 'ctx:', fblock[max(0,j-20):j+25])
# version file content typically like '23.05.0\n' or with revision
