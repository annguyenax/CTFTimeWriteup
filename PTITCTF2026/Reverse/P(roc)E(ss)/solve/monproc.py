#!/usr/bin/env python3
import subprocess, os, time, ctypes, threading
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
k32=ctypes.windll.kernel32
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def scan(pid):
    h=k32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    if not h: return None
    addr=0; mbi=MEMORY_BASIC_INFORMATION(); found=[]
    while addr<0x7fffffffffff:
        r=k32.VirtualQueryEx(h,ctypes.c_void_p(addr),ctypes.byref(mbi),ctypes.sizeof(mbi))
        if r==0: break
        if mbi.State==0x1000 and mbi.Protect & 0xff not in (0,1) and 0<mbi.RegionSize<0x1000000:
            buf=ctypes.create_string_buffer(mbi.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(mbi.BaseAddress),buf,mbi.RegionSize,ctypes.byref(rd)):
                data=buf.raw[:rd.value]
                idx=data.find(b'PTITCTF')
                if idx!=-1: found.append((mbi.BaseAddress+idx,data[idx:idx+120]))
        addr+=mbi.RegionSize
    k32.CloseHandle(h); return found

import psutil
def run_and_monitor(exe, inp):
    p=subprocess.Popen(exe, stdin=subprocess.PIPE if inp is not None else None, stdout=subprocess.PIPE)
    if inp is not None:
        time.sleep(0.1); 
        try: p.stdin.write(inp); p.stdin.flush()
        except Exception as e: print("stdin",e)
    # monitor children
    results=[]
    for _ in range(20):
        try:
            pp=psutil.Process(p.pid)
            for c in pp.children(recursive=True):
                f=scan(c.pid)
                if f: results.append(('child',c.pid,f))
        except Exception: pass
        f=scan(p.pid)
        if f: results.append(('self',p.pid,f))
        time.sleep(0.05)
    try: p.terminate()
    except: pass
    return results

import psutil
for exe,inp in [("live_chall.exe",b"4mCnFu\n"),("live_chall.exe",None),("live_chall_patched.exe",b"4mCnFu\n")]:
    print("=== running",exe,"input",inp,"===")
    try:
        res=run_and_monitor(exe,inp)
        for kind,pid,f in res:
            print("  ",kind,pid,[ (hex(a),s) for a,s in f])
    except Exception as e:
        print("  err",e)
