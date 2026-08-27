#!/usr/bin/env python3
import subprocess, time, os, ctypes
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
k32=ctypes.windll.kernel32
class MBI(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def scan(pid):
    h=k32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    if not h: return []
    a=0;m=MBI();out=set()
    while a<0x7fffffffffff:
        if k32.VirtualQueryEx(h,ctypes.c_void_p(a),ctypes.byref(m),ctypes.sizeof(m))==0: break
        if m.State==0x1000 and m.Protect&0xff not in (0,1) and 0<m.RegionSize<0x1000000:
            b=ctypes.create_string_buffer(m.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(m.BaseAddress),b,m.RegionSize,ctypes.byref(rd)):
                d=b.raw[:rd.value]
                i=0
                while True:
                    i=d.find(b'PTITCTF{', i)
                    if i<0: break
                    flag=d[i:i+100].split(b'\x00')[0].split(b'\n')[0].split(b'\r')[0]
                    out.add(flag)
                    i+=1
        a+=m.RegionSize
    k32.CloseHandle(h); return out

# ensure 4mCnFu.exe (ping) running
import shutil
shutil.copy(r"C:\Windows\System32\ping.exe","4mCnFu.exe")
pp=subprocess.Popen(["4mCnFu.exe","-t","127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.3)
decoy=b'PTITCTF{75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43}'

for attempt in range(10):
    p=subprocess.Popen(["live_chall.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    flags=set()
    # scan rapidly while the process runs
    while p.poll() is None:
        flags |= scan(p.pid)
    flags |= scan(p.pid)
    out=p.stdout.read() if p.poll() is not None else p.communicate(timeout=1)[0]
    real=[f for f in flags if f!=decoy]
    print(f"attempt {attempt}: out={out!r}")
    for f in real:
        print("  REAL FLAG:", f.decode(errors='replace'))
    if real:
        break
    time.sleep(0.05)

pp.terminate()
