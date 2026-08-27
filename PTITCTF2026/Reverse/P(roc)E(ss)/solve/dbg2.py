#!/usr/bin/env python3
import ctypes
from ctypes import wintypes
PROCESS_ALL_ACCESS=0x1F0FFF
CREATE_SUSPENDED=0x4; DEBUG_ONLY_THIS_PROCESS=0x2
class STARTUPINFO(ctypes.Structure):
    _fields_=[("cb",wintypes.DWORD),("lpReserved",wintypes.LPWSTR),("lpDesktop",wintypes.LPWSTR),("lpTitle",wintypes.LPWSTR),
              ("dwX",wintypes.DWORD),("dwY",wintypes.DWORD),("dwXSize",wintypes.DWORD),("dwYSize",wintypes.DWORD),
              ("dwXCountChars",wintypes.DWORD),("dwYCountChars",wintypes.DWORD),("dwFillAttribute",wintypes.DWORD),
              ("dwFlags",wintypes.DWORD),("wShowWindow",wintypes.WORD),("cbReserved2",wintypes.WORD),
              ("lpReserved2",ctypes.POINTER(wintypes.BYTE)),("hStdInput",wintypes.HANDLE),("hStdOutput",wintypes.HANDLE),("hStdError",wintypes.HANDLE)]
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_=[("hProcess",wintypes.HANDLE),("hThread",wintypes.HANDLE),("dwProcessId",wintypes.DWORD),("dwThreadId",wintypes.DWORD)]
class CONTEXT(ctypes.Structure):
    _fields_=[("P1Home",ctypes.c_uint64),("P2Home",ctypes.c_uint64),("P3Home",ctypes.c_uint64),("P4Home",ctypes.c_uint64),("P5Home",ctypes.c_uint64),("P6Home",ctypes.c_uint64),
              ("ContextFlags",wintypes.DWORD),("MxCsr",wintypes.DWORD),
              ("SegCs",wintypes.WORD),("SegDs",wintypes.WORD),("SegEs",wintypes.WORD),("SegFs",wintypes.WORD),("SegGs",wintypes.WORD),("SegSs",wintypes.WORD),("EFlags",wintypes.DWORD),
              ("Dr0",ctypes.c_uint64),("Dr1",ctypes.c_uint64),("Dr2",ctypes.c_uint64),("Dr3",ctypes.c_uint64),("Dr6",ctypes.c_uint64),("Dr7",ctypes.c_uint64),
              ("Rax",ctypes.c_uint64),("Rcx",ctypes.c_uint64),("Rdx",ctypes.c_uint64),("Rbx",ctypes.c_uint64),("Rsp",ctypes.c_uint64),("Rbp",ctypes.c_uint64),
              ("Rsi",ctypes.c_uint64),("Rdi",ctypes.c_uint64),("R8",ctypes.c_uint64),("R9",ctypes.c_uint64),("R10",ctypes.c_uint64),("R11",ctypes.c_uint64),
              ("R12",ctypes.c_uint64),("R13",ctypes.c_uint64),("R14",ctypes.c_uint64),("R15",ctypes.c_uint64),("Rip",ctypes.c_uint64)]
k32=ctypes.windll.kernel32
class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_=[("hFile",wintypes.HANDLE),("hProcess",wintypes.HANDLE),("hThread",wintypes.HANDLE),("lpBaseOfImage",wintypes.LPVOID),("dwDebugInfoFileOffset",wintypes.DWORD),("nDebugInfoSize",wintypes.DWORD),("lpThreadLocalBase",wintypes.LPVOID),("lpStartAddress",wintypes.LPVOID),("lpImageName",wintypes.LPVOID),("fUnicode",wintypes.WORD)]
class DEBUG_EVENT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_=[("CreateProcessInfo",CREATE_PROCESS_DEBUG_INFO)]
    _fields_=[("dwDebugEventCode",wintypes.DWORD),("dwProcessId",wintypes.DWORD),("dwThreadId",wintypes.DWORD),("u",_U)]
CREATE_PROCESS_DEBUG_EVENT=3; EXCEPTION_DEBUG_EVENT=1; EXIT_PROCESS_DEBUG_EVENT=5
EXCEPTION_BREAKPOINT=0x80000003

import subprocess, os, sys
# breakpoints (offsets from image base)
BPS=[0x14000183f-0x140000000, 0x140001bfd-0x140000000, 0x140001cd9-0x140000000, 0x140001d42-0x140000000, 0x140002643-0x140000000]
si=STARTUPINFO(); si.cb=ctypes.sizeof(si); pi=PROCESS_INFORMATION()
cmd="live_chall_patched.exe"
k32.CreateProcessW(None, cmd, None,None,False, DEBUG_ONLY_THIS_PROCESS|CREATE_SUSPENDED, None,None, ctypes.byref(si), ctypes.byref(pi))
hProc=pi.hProcess; hThread=pi.hThread
k32.ResumeThread(hThread)
base=None; ctx=CONTEXT(); ctx.ContextFlags=0x100010; count=0
# feed stdin
try:
    si_pipe=subprocess.STARTUPINFO()
    p=subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(0.2); p.stdin.write(b'4mCnFu.exe\n'); p.stdin.flush()
except Exception as e:
    print("pipe",e)
import time
while count<3000:
    de=DEBUG_EVENT()
    if not k32.WaitForDebugEvent(ctypes.byref(de),3000): break
    code=de.dwDebugEventCode
    if code==CREATE_PROCESS_DEBUG_EVENT:
        base=de.u.CreateProcessInfo.lpBaseOfImage
        print("base",hex(base))
        for off in BPS:
            b=ctypes.c_byte(0xCC); k32.WriteProcessMemory(hProc, ctypes.c_void_p(base+off), ctypes.byref(b),1,None)
    if code==EXCEPTION_DEBUG_EVENT:
        exc=ctypes.c_uint32.from_buffer_copy(de.u,0).value
        if exc==EXCEPTION_BREAKPOINT:
            k32.GetThreadContext(hThread, ctypes.byref(ctx))
            rel=ctx.Rip-base
            print("BP at", hex(ctx.Rip), "rel", hex(rel), "rcx=%x rdx=%x r8=%x"%(ctx.Rcx,ctx.Rdx,ctx.R8))
            # restore byte at rip and re-execute (step: set single step)
            k32.WriteProcessMemory(hProc, ctypes.c_void_p(ctx.Rip), ctypes.byref(ctypes.c_byte(0x00)),1,None)  # will patch later; just continue
            # read memory at rcx if it's a pointer
            if rel in (0x14000183f-0x140000000, 0x140001bfd-0x140000000):
                try:
                    buf=ctypes.create_string_buffer(0x60); r=ctypes.c_size_t(0)
                    k32.ReadProcessMemory(hProc, ctypes.c_void_p(ctx.Rcx), buf,0x60,ctypes.byref(r))
                    print("   mem rcx:", buf.raw[:r.value].hex())
                except Exception as e: print("  rmem",e)
    if code==EXIT_PROCESS_DEBUG_EVENT:
        print("process exited"); break
    k32.ContinueDebugEvent(de.dwProcessId,de.dwThreadId,0x2)
    count+=1
k32.TerminateProcess(hProc,0)
