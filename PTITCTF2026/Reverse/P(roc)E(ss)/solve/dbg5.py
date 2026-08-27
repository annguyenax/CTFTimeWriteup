#!/usr/bin/env python3
import ctypes, os
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

def trace(exe, bps):
    si=STARTUPINFO(); si.cb=ctypes.sizeof(si); pi=PROCESS_INFORMATION()
    r=k32.CreateProcessW(None, os.path.abspath(exe), None,None,False,DEBUG_ONLY_THIS_PROCESS|CREATE_SUSPENDED,None,None,ctypes.byref(si),ctypes.byref(pi))
    hProc,hThread=pi.hProcess,pi.hThread
    base=None; orig={}; ctx=CONTEXT(); ctx.ContextFlags=0x100010; hits=[]; initial=True
    k32.ResumeThread(hThread)
    while True:
        de=DEBUG_EVENT()
        if not k32.WaitForDebugEvent(ctypes.byref(de),4000): print("timeout"); break
        code=de.dwDebugEventCode
        if code==CREATE_PROCESS_DEBUG_EVENT:
            base=de.u.CreateProcessInfo.lpBaseOfImage
            print("base",hex(base))
            for off in bps:
                a=base+off
                rb=ctypes.create_string_buffer(1); rr=ctypes.c_size_t(0)
                ok=k32.ReadProcessMemory(hProc,ctypes.c_void_p(a),rb,1,ctypes.byref(rr))
                if ok:
                    orig[a]=rb.raw[0]
                    k32.WriteProcessMemory(hProc,ctypes.c_void_p(a),ctypes.byref(ctypes.c_byte(0xCC)),1,None)
                    print("  bp set at",hex(a),"orig",rb.raw.hex())
        if code==EXCEPTION_DEBUG_EVENT:
            exc=ctypes.c_uint32.from_buffer_copy(de.u,0).value
            if exc==EXCEPTION_BREAKPOINT:
                k32.GetThreadContext(hThread,ctypes.byref(ctx))
                if ctx.Rip-base in bps:  # our breakpoint
                    print("HIT",hex(ctx.Rip-base),"rcx=%x rdx=%x r8=%x r9=%x"%(ctx.Rcx,ctx.Rdx,ctx.R8,ctx.R9))
                    hits.append(ctx.Rip-base)
                    if ctx.Rip in orig: k32.WriteProcessMemory(hProc,ctypes.c_void_p(ctx.Rip),ctypes.byref(ctypes.c_byte(orig[ctx.Rip])),1,None)
                    ctx.Rip=ctx.Rip; ctx.EFlags|=0x100; k32.SetThreadContext(hThread,ctypes.byref(ctx))
                else:
                    # initial/system breakpoint: just continue (skip)
                    k32.ContinueDebugEvent(de.dwProcessId,de.dwThreadId,0x2); continue
            # single-step continue
        if code==EXIT_PROCESS_DEBUG_EVENT: print("exit"); break
        k32.ContinueDebugEvent(de.dwProcessId,de.dwThreadId,0x2)
    print("hits:",[hex(h) for h in hits])
    k32.TerminateProcess(hProc,0)

print("=== PATCHED, input-read 0x14000183f + compare 0x140001bfd ===")
trace("live_chall_patched.exe",[0x14000183f-0x140000000, 0x140001bfd-0x140000000, 0x140001cd9-0x140000000])
