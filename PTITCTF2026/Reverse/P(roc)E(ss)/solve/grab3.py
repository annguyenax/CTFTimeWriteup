#!/usr/bin/env python3
import subprocess, time, shutil, os, ctypes
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
k32=ctypes.windll.kernel32
class MBI(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def dump(pid):
    h=k32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    if not h: return set()
    a=0;m=MBI();out=set()
    while a<0x7fffffffffff:
        if k32.VirtualQueryEx(h,ctypes.c_void_p(a),ctypes.byref(m),ctypes.sizeof(m))==0: break
        if m.State==0x1000 and m.Protect&0xff not in (0,1) and 0<m.RegionSize<0x1000000:
            b=ctypes.create_string_buffer(m.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(m.BaseAddress),b,m.RegionSize,ctypes.byref(rd)):
                d=b.raw[:rd.value]
                for key in (b'PTITCTF{',):
                    i=0
                    while True:
                        i=d.find(key,i)
                        if i<0: break
                        out.add(d[i:i+120].split(b'\x00')[0].split(b'\n')[0].split(b'\r')[0])
                        i+=1
        a+=m.RegionSize
    k32.CloseHandle(h); return out

shutil.copy(r"C:\Windows\System32\ping.exe","4mCnFu.exe")
# run ping with stdout/stderr captured (NOT devnull)
pp=subprocess.Popen(["4mCnFu.exe","-t","127.0.0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(0.3)
p=subprocess.Popen(["live_chall.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# scan ping memory rapidly while challenge runs
found=set()
while p.poll() is None:
    found |= dump(pp.pid)
    time.sleep(0.001)
found |= dump(pp.pid)
chall_out=p.communicate(timeout=2)[0]
# read ping stdout (shellcode might print flag here)
try:
    ping_out=pp.stdout.read() if pp.stdout else b''
except Exception:
    ping_out=b''
print("chall stdout:", chall_out)
print("ping stdout tail:", ping_out[-200:] if ping_out else b'')
print("flags in ping memory:", [f.decode(errors='replace') for f in found])
p.kill(); pp.terminate()
