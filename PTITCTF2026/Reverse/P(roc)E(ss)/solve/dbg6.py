#!/usr/bin/env python3
import ctypes, os, time, subprocess, shutil
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF; CREATE_SUSPENDED=0x4; DEBUG_ONLY_THIS_PROCESS=0x2
class STARTUPINFO(ctypes.Structure):
    _fields_=[("cb",wintypes.DWORD),("lpReserved",wintypes.LPWSTR),("lpDesktop",wintypes.LPWSTR),("lpTitle",wintypes.LPWSTR),("dwX",wintypes.DWORD),("dwY",wintypes.DWORD),("dwXSize",wintypes.DWORD),("dwYSize",wintypes.DWORD),("dwXCountChars",wintypes.DWORD),("dwYCountChars",wintypes.DWORD),("dwFillAttribute",wintypes.DWORD),("dwFlags",wintypes.DWORD),("wShowWindow",wintypes.WORD),("cbReserved2",wintypes.WORD),("lpReserved2",ctypes.POINTER(wintypes.BYTE)),("hStdInput",wintypes.HANDLE),("hStdOutput",wintypes.HANDLE),("hStdError",wintypes.HANDLE)]
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_=[("hProcess",wintypes.HANDLE),("hThread",wintypes.HANDLE),("dwProcessId",wintypes.DWORD),("dwThreadId",wintypes.DWORD)]
class CONTEXT(ctypes.Structure):
    _fields_=[("P1Home",ctypes.c_uint64),("P2Home",ctypes.c_uint64),("P3Home",ctypes.c_uint64),("P4Home",ctypes.c_uint64),("P5Home",ctypes.c_uint64),("P6Home",ctypes.c_uint64),("ContextFlags",wintypes.DWORD),("MxCsr",wintypes.DWORD),("SegCs",wintypes.WORD),("SegDs",wintypes.WORD),("SegEs",wintypes.WORD),("SegFs",wintypes.WORD),("SegGs",wintypes.WORD),("SegSs",wintypes.WORD),("EFlags",wintypes.DWORD),("Dr0",ctypes.c_uint64),("Dr1",ctypes.c_uint64),("Dr2",ctypes.c_uint64),("Dr3",ctypes.c_uint64),("Dr6",ctypes.c_uint64),("Dr7",ctypes.c_uint64),("Rax",ctypes.c_uint64),("Rcx",ctypes.c_uint64),("Rdx",ctypes.c_uint64),("Rbx",ctypes.c_uint64),("Rsp",ctypes.c_uint64),("Rbp",ctypes.c_uint64),("Rsi",ctypes.c_uint64),("Rdi",ctypes.c_uint64),("R8",ctypes.c_uint64),("R9",ctypes.c_uint64),("R10",ctypes.c_uint64),("R11",ctypes.c_uint64),("R12",ctypes.c_uint64),("R13",ctypes.c_uint64),("R14",ctypes.c_uint64),("R15",ctypes.c_uint64),("Rip",ctypes.c_uint64)]
k32=ctypes.windll.kernel32
class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_=[("hFile",wintypes.HANDLE),("hProcess",wintypes.HANDLE),("hThread",wintypes.HANDLE),("lpBaseOfImage",wintypes.LPVOID),("dwDebugInfoFileOffset",wintypes.DWORD),("nDebugInfoSize",wintypes.DWORD),("lpThreadLocalBase",wintypes.LPVOID),("lpStartAddress",wintypes.LPVOID),("lpImageName",wintypes.LPVOID),("fUnicode",wintypes.WORD)]
class DEBUG_EVENT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_=[("CreateProcessInfo",CREATE_PROCESS_DEBUG_INFO)]
    _fields_=[("dwDebugEventCode",wintypes.DWORD),("dwProcessId",wintypes.DWORD),("dwThreadId",wintypes.DWORD),("u",_U)]
CREATE_PROCESS_DEBUG_EVENT=3; EXCEPTION_DEBUG_EVENT=1; EXIT_PROCESS_DEBUG_EVENT=5
EXCEPTION_BREAKPOINT=0x80000003

class MBI(ctypes.Structure):
    _fields_=[("BaseAddress",wintypes.LPVOID),("AllocationBase",wintypes.LPVOID),("AllocationProtect",wintypes.DWORD),("RegionSize",ctypes.c_size_t),("State",wintypes.DWORD),("Protect",wintypes.DWORD),("Type",wintypes.DWORD)]
def dumpmem(h, pid):
    a=0; m=MBI(); out=set()
    while a<0x7fffffffffff:
        if k32.VirtualQueryEx(h,ctypes.c_void_p(a),ctypes.byref(m),ctypes.sizeof(m))==0: break
        if m.State==0x1000 and m.Protect&0xff not in (0,1) and 0<m.RegionSize<0x1000000:
            b=ctypes.create_string_buffer(m.RegionSize); rd=ctypes.c_size_t(0)
            if k32.ReadProcessMemory(h,ctypes.c_void_p(m.BaseAddress),b,m.RegionSize,ctypes.byref(rd)):
                d=b.raw[:rd.value]
                i=0
                while True:
                    i=d.find(b'PTITCTF',i)
                    if i<0: break
                    out.add(d[i:i+120].split(b'\x00')[0].split(b'\n')[0].split(b'\r')[0])
                    i+=1
        a+=m.RegionSize
    return out

# run 4mCnFu.exe (ping)
shutil.copy(r"C:\Windows\System32\ping.exe","4mCnFu.exe")
pp=subprocess.Popen(["4mCnFu.exe","-t","127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.3)

si=STARTUPINFO(); si.cb=ctypes.sizeof(si); pi=PROCESS_INFORMATION()
k32.CreateProcessW(None, os.path.abspath("live_chall.exe"), None,None,False,DEBUG_ONLY_THIS_PROCESS|CREATE_SUSPENDED,None,None,ctypes.byref(si),ctypes.byref(pi))
hProc,hThread=pi.hProcess,pi.hThread
base=None; ctx=CONTEXT(); ctx.ContextFlags=0x100010
BP=0x14000264d-0x140000000  # message puts
k32.ResumeThread(hThread)
hits=[]
while True:
    de=DEBUG_EVENT()
    if not k32.WaitForDebugEvent(ctypes.byref(de),4000): break
    code=de.dwDebugEventCode
    if code==CREATE_PROCESS_DEBUG_EVENT:
        base=de.u.CreateProcessInfo.lpBaseOfImage
        a=base+BP
        rb=ctypes.create_string_buffer(1); rr=ctypes.c_size_t(0)
        k32.ReadProcessMemory(hProc,ctypes.c_void_p(a),rb,1,ctypes.byref(rr))
        k32.WriteProcessMemory(hProc,ctypes.c_void_p(a),ctypes.byref(ctypes.c_byte(0xCC)),1,None)
    if code==EXCEPTION_DEBUG_EVENT:
        exc=ctypes.c_uint32.from_buffer_copy(de.u,0).value
        if exc==EXCEPTION_BREAKPOINT:
            k32.GetThreadContext(hThread,ctypes.byref(ctx))
            if base and ctx.Rip==base+BP:
                hits.append(ctx.Rip-base)
                print("BP hit at message!")
                flags=dumpmem(hProc,pi.dwProcessId)
                print("FLAGS IN MEMORY:", [f.decode(errors='replace') for f in flags])
                break
            # continue (initial breakpoint or other)
    if code==EXIT_PROCESS_DEBUG_EVENT: 
        print("exited before BP"); break
    k32.ContinueDebugEvent(de.dwProcessId,de.dwThreadId,0x2)
k32.TerminateProcess(hProc,0)
pp.terminate()
print("done hits",hits)
