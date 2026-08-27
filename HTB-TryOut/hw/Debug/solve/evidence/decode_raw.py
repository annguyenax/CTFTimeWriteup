import struct
# The raw digital-1.bin internal format (type 100). Try to parse transitions.
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1.bin", 'rb').read()
# Let's find where actual data begins by scanning for plausible structure.
# Saleae internal digital format type 100: after header there's a sequence.
# Let's just hexdump region 0xB8 onward.
for i in range(0xB8, 0x180, 16):
    c = data[i:i+16]
    print("%04X %s" % (i, c.hex(' ')))
