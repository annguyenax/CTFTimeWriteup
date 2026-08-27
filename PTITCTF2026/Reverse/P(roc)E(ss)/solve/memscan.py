#!/usr/bin/env python3
import ctypes, subprocess, time, os, struct
from ctypes import wintypes

# Windows constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT=0x1000; MEM_RESERVE=0x2000
PAGE_READWRITE=0x04; PAGE_READONLY=0x02; PAGE_EXECUTE_READWRITE=0x40; PAGE_EXECUTE_READ=0x20; PAGE_WRITECOPY=0x08; PAGE_EXECUTE_WRITECOPY=0x80

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),
              ("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]

kernel32=ctypes.windll.kernel32

def scan(pid):
    h=kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h: return None
    addr=0
    mbi=MEMORY_BASIC_INFORMATION()
    found=[]
    while addr < 0x7fffffffffff:
        ret=kernel32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi))
        if ret==0: break
        if mbi.State==MEM_COMMIT and mbi.Protect & 0xff not in (0, 0x01):
            sz=mbi.RegionSize
            if sz>0 and sz<0x2000000:
                buf=ctypes.create_string_buffer(sz)
                read=ctypes.c_size_t(0)
                if kernel32.ReadProcessMemory(h, ctypes.c_void_p(mbi.BaseAddress), buf, sz, ctypes.byref(read)):
                    data=buf.raw[:read.value]
                    idx=data.find(b'PTITCTF')
                    if idx!=-1:
                        found.append((mbi.BaseAddress+idx, data[idx:idx+100]))
        addr += mbi.RegionSize
    kernel32.CloseHandle(h)
    return found

# launch patched binary with stdin held
import sys
cmd=[os.path.join(os.getcwd(),'live_chall_patched.exe')]
# keep stdin open to prevent exit
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(0.3)
# write the filename and flush but keep pipe open
try:
    p.stdin.write(b'4mCnFu.exe\n'); p.stdin.flush()
except Exception as e:
    print("stdin err", e)
time.sleep(0.5)
print("pid", p.pid, "poll", p.poll())
found=scan(p.pid)
print("found:", found)
for f in found: print("FLAG?", f[1])
try: p.terminate()
except: pass
