#!/usr/bin/env python3
# User-friendly: runs the challenge binary, watches for child processes,
# scans their memory for PTITCTF flag, prints findings.
# Usage:  python run_and_scan.py [input_string]
import sys, time, subprocess, os, ctypes
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
k32=ctypes.windll.kernel32
class MBI(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def scan_pid(pid):
    h=k32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    if not h: return []
    a=0;m=MBI();out=[]
    while a<0x7fffffffffff:
        if k32.VirtualQueryEx(h,ctypes.c_void_p(a),ctypes.byref(m),ctypes.sizeof(m))==0: break
        if m.State==0x1000 and m.Protect&0xff not in (0,1) and 0<m.RegionSize<0x1000000:
            b=ctypes.create_string_buffer(m.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(m.BaseAddress),b,m.RegionSize,ctypes.byref(rd)):
                d=b.raw[:rd.value]
                for key in (b'PTITCTF', b'sealed', b'4mCnFu'):
                    i=d.find(key)
                    if i!=-1: out.append((m.BaseAddress+i,key,d[max(0,i-8):i+120]))
        a+=m.RegionSize
    k32.CloseHandle(h); return out

import psutil
def main():
    inp=sys.argv[1].encode()+b'\n' if len(sys.argv)>1 else None
    p=subprocess.Popen(['live_chall.exe'], stdin=subprocess.PIPE if inp else None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Started PID", p.pid)
    if inp:
        time.sleep(0.15)
        try: p.stdin.write(inp); p.stdin.flush()
        except Exception as e: print("  (input write:", e, ")")
    results=[]
    for _ in range(40):  # ~4 seconds
        try:
            pp=psutil.Process(p.pid)
            for c in pp.children(recursive=True):
                f=scan_pid(c.pid)
                if f: results.append(('child', c.pid, c.name(), f))
        except Exception: pass
        f=scan_pid(p.pid)
        if f: results.append(('self', p.pid, 'chall', f))
        if p.poll() is not None: break
        time.sleep(0.1)
    print("Parent exited?", p.poll() is not None)
    try:
        out=p.communicate(timeout=1)[0]
        print("stdout:", out)
    except Exception: 
        p.kill()
    print("=== FLAG FOUND ===")
    for kind,pid,name,f in results:
        print(f"[{kind}] pid={pid} name={name}")
        for addr,key,data in f:
            print(f"   {key} at {hex(addr)}: {data}")
    if not results:
        print("(no PTITCTF found in process memory; no child process seen)")

if __name__=='__main__':
    main()
