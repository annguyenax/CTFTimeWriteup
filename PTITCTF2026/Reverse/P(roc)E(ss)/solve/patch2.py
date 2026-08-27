#!/usr/bin/env python3
import struct
data=bytearray(open('live_chall.exe','rb').read())
def va2off(va): return 0x400 + (va - (0x140000000+0x1000))
def patch(va, new):
    off=va2off(va)
    old=data[off:off+len(new)]
    data[off:off+len(new)]=new
    print(f"patch {hex(va)}: {old.hex()} -> {new.hex()}")

# NOP the free calls (call rdx = FF D2, call r10 = 41 FF D2)
patch(0x140001ec6, b'\x90\x90')           # call rdx (free page after decrypt)
patch(0x140001ee7, b'\x90\x90\x90')       # call r10 (free)
patch(0x140001e85, b'\x90\x90\x90')       # call r10 (free)
patch(0x140001e97, b'\x90\x90')           # call rdx (free)
# loop forever after the message instead of returning
patch(0x140002652, b'\xeb\xfe\x90\x90\x90')  # jmp self
open('live_chall_p2.exe','wb').write(bytes(data))
print("written live_chall_p2.exe")
