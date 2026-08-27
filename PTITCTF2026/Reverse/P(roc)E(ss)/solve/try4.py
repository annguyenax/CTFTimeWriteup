#!/usr/bin/env python3
import subprocess, time, shutil, os
# make 4mCnFu.exe = challenge binary patched to loop (stay alive)
data=bytearray(open('live_chall.exe','rb').read())
# patch main epilogue 0x140002657 leave;ret -> jmp self (loop)
off=0x400+(0x2657-0x1000)
data[off:off+2]=b'\xeb\xfe'
open('4mCnFu_loop.exe','wb').write(bytes(data))
shutil.copy('4mCnFu_loop.exe','4mCnFu.exe')

pp=subprocess.Popen(['4mCnFu.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.4)
print("4mCnFu (looped challenge) alive:", pp.poll() is None)

for exe in ['live_chall_p3.exe','live_chall.exe','live_chall_p2.exe']:
    p=subprocess.Popen([exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out=p.communicate(timeout=2)[0]
    except subprocess.TimeoutExpired:
        p.kill(); out=b'(timeout/loop)'
    print(f"[{exe}] out={out!r}")
pp.terminate()
