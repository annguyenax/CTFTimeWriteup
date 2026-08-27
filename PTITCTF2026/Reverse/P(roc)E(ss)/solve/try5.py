#!/usr/bin/env python3
import subprocess, time, shutil, threading, os
data=bytearray(open('live_chall.exe','rb').read())
data[0x400+(0x2657-0x1000):0x400+(0x2657-0x1000)+2]=b'\xeb\xfe'
open('4mCnFu.exe','wb').write(bytes(data))
pp=subprocess.Popen(['4mCnFu.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.3)
p=subprocess.Popen(['live_chall_p3.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(1.0)
# read whatever stdout is available
import os as _os
out=b''
try:
    out = p.stdout.read()
except Exception:
    pass
print("p3 stdout:", out)
# also if p still running, kill it
p.kill()
pp.terminate()
