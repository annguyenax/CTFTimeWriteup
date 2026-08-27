#!/usr/bin/env python3
import ctypes, struct, time
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
CREATE_SUSPENDED=0x4; DEBUG_ONLY_THIS_PROCESS=0x2
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
EXCEPTION_BREAKPOINT=0x80000003; EXCEPTION_SINGLE_STEP=0x80000004

def run_trace(exe, stdin_data):
    si=STARTUPINFO(); si.cb=ctypes.sizeof(si); pi=PROCESS_INFORMATION()
    k32.CreateProcessW(None, exe, None,None,False, DEBUG_ONLY_THIS_PROCESS|CREATE_SUSPENDED, None,None, ctypes.byref(si), ctypes.byref(pi))
    hProc,hThread=pi.hProcess,pi.hThread
    k32.ResumeThread(hThread)
    base=None
    # breakpoints: input-init, comparison, decode, message
    bps={0x14000183f-0x140000000,0x140001bfd-0x140000000,0x140001cd9-0x140000000,0x140002643-0x140000000}
    orig={}
    ctx=CONTEXT(); ctx.ContextFlags=0x100010
    count=0; hits=[]
    while count<5000:
        de=DEBUG_EVENT()
        if not k32.WaitForDebugEvent(ctypes.byref(de),3000): break
        code=de.dwDebugEventCode
        if code==CREATE_PROCESS_DEBUG_EVENT:
            base=de.u.CreateProcessInfo.lpBaseOfImage
            for off in bps:
                a=base+off
                rb=ctypes.create_string_buffer(1); r=ctypes.c_size_t(0)
                k32.ReadProcessMemory(hProc, ctypes.c_void_p(a), rb,1,ctypes.byref(r))
                orig[a]=rb.raw[0]
                k32.WriteProcessMemory(hProc, ctypes.c_void_p(a), ctypes.byref(ctypes.c_byte(0xCC)),1,None)
        if code==EXCEPTION_DEBUG_EVENT:
            exc=ctypes.c_uint32.from_buffer_copy(de.u,0).value
            if exc==EXCEPTION_BREAKPOINT:
                k32.GetThreadContext(hThread, ctypes.byref(ctx))
                addr=ctx.Rip
                rel=addr-base
                print("BP hit at rel", hex(rel), "rcx=%x rdx=%x r8=%x r9=%x"%(ctx.Rcx,ctx.Rdx,ctx.R8,ctx.R9))
                hits.append(rel)
                if rel==0x14000183f-0x140000000:
                    # dump input buffer at rcx
                    buf=ctypes.create_string_buffer(0x50); r=ctypes.c_size_t(0)
                    k32.ReadProcessMemory(hProc, ctypes.c_void_p(ctx.Rcx), buf,0x50,ctypes.byref(r))
                    print("  input buf:", buf.raw[:r.value].hex())
                if rel==0x140001cd9-0x140000000:
                    print("  >>> DECODE reached")
                if rel==0x140002643-0x140000000:
                    print("  >>> MESSAGE path reached")
                # restore byte, set RIP, single-step
                if addr in orig:
                    k32.WriteProcessMemory(hProc, ctypes.c_void_p(addr), ctypes.byref(ctypes.c_byte(orig[addr])),1,None)
                ctx.Rip=addr
                ctx.EFlags |= 0x100  # TF single-step
                k32.SetThreadContext(hThread, ctypes.byref(ctx))
            elif exc==EXCEPTION_SINGLE_STEP:
                k32.GetThreadContext(hThread, ctypes.byref(ctx))
                # re-set breakpoint if we stepped onto one
                for off in bps:
                    if ctx.Rip==base+off:
                        k32.WriteProcessMemory(hProc, ctypes.c_void_p(ctx.Rip), ctypes.byref(ctypes.c_byte(0xCC)),1,None)
                k32.SetThreadContext(hThread, ctypes.byref(ctx))
        if code==EXIT_PROCESS_DEBUG_EVENT:
            print("process exited"); break
        k32.ContinueDebugEvent(de.dwProcessId,de.dwThreadId,0x2)
        count+=1
    print("BP hits:", [hex(h) for h in hits])
    k32.TerminateProcess(hProc,0)

# try with stdin "4mCnFu"
import subprocess, os, threading
def feed():
    time.sleep(0.3)
    try:
        p=subprocess.Popen("live_chall_patched.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(b'4mCnFu\n'); p.stdin.flush()
    except Exception as e:
        print("feed",e)
t=threading.Thread(target=feed); t.start()
run_trace("live_chall_patched.exe", b'4mCnFu\n')
