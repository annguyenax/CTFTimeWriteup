#!/usr/bin/env python3
import subprocess, os, time, ctypes
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
k32=ctypes.windll.kernel32
class MBI(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def scan(pid):
    h=k32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    if not h: return []
    a=0; m=MBI(); out=[]
    while a<0x7fffffffffff:
        if k32.VirtualQueryEx(h,ctypes.c_void_p(a),ctypes.byref(m),ctypes.sizeof(m))==0: break
        if m.State==0x1000 and m.Protect&0xff not in (0,1) and 0<m.RegionSize<0x1000000:
            b=ctypes.create_string_buffer(m.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(m.BaseAddress),b,m.RegionSize,ctypes.byref(rd)):
                d=b.raw[:rd.value]
                if b'PTITCTF' in d:
                    i=d.find(b'PTITCTF'); out.append((m.BaseAddress+i, d[i:i+120]))
        a+=m.RegionSize
    k32.CloseHandle(h); return out

contents = {
  "4mCnFu.exe": b"4mCnFu.exe\n",
  "just4mCnFu": b"4mCnFu\n",
  "flagcontent": b"75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43\n",
  "fullflag": b"PTITCTF{75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43}\n",
}
for exe in ["live_chall_patched.exe","live_chall.exe"]:
    for name, content in contents.items():
        with open("4mCnFu.exe","wb") as f: f.write(content)
        p=subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs=b''
        try:
            outs=p.communicate(timeout=3)[0]
        except Exception:
            p.kill(); outs=b'(timeout)'
        mem=scan(p.pid)
        print(f"[{exe}] file={name}: out={outs!r} mem={[hex(a) for a,_ in mem]}")
        for a,s in mem: print("   MEM:", s)
        time.sleep(0.1)
