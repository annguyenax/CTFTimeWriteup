#!/usr/bin/env python3
data=bytearray(open('live_chall.exe','rb').read())
def va2off(va): return 0x400 + (va - (0x140000000+0x1000))
# patch 0x140001ec6 (call rdx = free page) -> call puts (0x140003798)
# rel32 = 0x140003798 - (0x140001ec6+5) = 0x18cd
off=va2off(0x140001ec6)
old=data[off:off+2]
data[off:off+5]=b'\xe8\xcd\x18\x00\x00'
print(f"patched {hex(0x140001ec6)}: {old.hex()} -> e8cd180000 (call puts)")
open('live_chall_p3.exe','wb').write(bytes(data))
print("written live_chall_p3.exe")
