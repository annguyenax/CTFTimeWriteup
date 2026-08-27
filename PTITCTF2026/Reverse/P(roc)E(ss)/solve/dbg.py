#!/usr/bin/env python3
import ctypes, struct
from ctypes import wintypes

PROCESS_ALL_ACCESS=0x1F0FFF
CREATE_SUSPENDED=0x4; DEBUG_ONLY_THIS_PROCESS=0x2; CREATE_NEW_CONSOLE=0x10
TH32CS_SNAPMODULE=0x8

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
              ("R12",ctypes.c_uint64),("R13",ctypes.c_uint64),("R14",ctypes.c_uint64),("R15",ctypes.c_uint64),
              ("Rip",ctypes.c_uint64)]

k32=ctypes.windll.kernel32
# Debug events
class LOAD_DLL_DEBUG_INFO(ctypes.Structure):
    _fields_=[("hFile",wintypes.HANDLE),("lpBaseOfDll",wintypes.LPVOID),("dwDebugInfoFileOffset",wintypes.DWORD),("nDebugInfoSize",wintypes.DWORD),("lpImageName",wintypes.LPVOID),("fUnicode",wintypes.WORD)]
class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_=[("hFile",wintypes.HANDLE),("hProcess",wintypes.HANDLE),("hThread",wintypes.HANDLE),("lpBaseOfImage",wintypes.LPVOID),("dwDebugInfoFileOffset",wintypes.DWORD),("nDebugInfoSize",wintypes.DWORD),("lpThreadLocalBase",wintypes.LPVOID),("lpStartAddress",wintypes.LPVOID),("lpImageName",wintypes.LPVOID),("fUnicode",wintypes.WORD)]
class DEBUG_EVENT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_=[("CreateProcessInfo",CREATE_PROCESS_DEBUG_INFO),("LoadDll",LOAD_DLL_DEBUG_INFO)]
    _fields_=[("dwDebugEventCode",wintypes.DWORD),("dwProcessId",wintypes.DWORD),("dwThreadId",wintypes.DWORD),("u",_U)]

EXCEPTION_BREAKPOINT=0x80000003
EXCEPTION_DEBUG_EVENT=1; CREATE_PROCESS_DEBUG_EVENT=3; EXIT_PROCESS_DEBUG_EVENT=5

base_addr=None  # runtime module base

si=STARTUPINFO(); si.cb=ctypes.sizeof(si)
pi=PROCESS_INFORMATION()
cmd="live_chall.exe"
res=k32.CreateProcessW(None, cmd, None, None, False, DEBUG_ONLY_THIS_PROCESS|CREATE_SUSPENDED, None, None, ctypes.byref(si), ctypes.byref(pi))
print("CreateProcess res", res, "pid", pi.dwProcessId)
hProc=pi.hProcess
# patch breakpoint at VirtualProtect PLT using runtime base (will set after we learn base in event loop)
bp_va=None
# initially, resume and wait for CREATE_PROCESS_DEBUG_EVENT to get base
k32.ResumeThread(pi.hThread)

ctx=CONTEXT(); ctx.ContextFlags=0x100010  # full
found=[]
count=0
patched=False
while count<3000:
    de=DEBUG_EVENT()
    if not k32.WaitForDebugEvent(ctypes.byref(de), 3000):
        break
    code=de.dwDebugEventCode
    if code==CREATE_PROCESS_DEBUG_EVENT:
        base_addr=de.u.CreateProcessInfo.lpBaseOfImage
        print("module base =", hex(base_addr or 0))
        if base_addr:
            bp_va=base_addr + 0x3888  # VirtualProtect PLT
            # read original and patch int3
            readbuf=ctypes.create_string_buffer(1); r2=ctypes.c_size_t(0)
            k32.ReadProcessMemory(hProc, ctypes.c_void_p(bp_va), readbuf, 1, ctypes.byref(r2))
            print("orig byte at bp:", readbuf.raw.hex())
            b=ctypes.c_byte(0xCC)
            k32.WriteProcessMemory(hProc, ctypes.c_void_p(bp_va), ctypes.byref(b), 1, None)
            patched=True
    if code==EXCEPTION_DEBUG_EVENT:
        exc=ctypes.c_uint32.from_buffer_copy(de.u, 0).value
        if exc==EXCEPTION_BREAKPOINT and patched:
            k32.GetThreadContext(pi.hThread, ctypes.byref(ctx))
            if ctx.Rip==bp_va:
                print("=== VirtualProtect hit, addr=0x%x size=0x%x prot=0x%x"%(ctx.Rcx,ctx.Rdx,ctx.R8))
                buf=ctypes.create_string_buffer(0x100)
                r=ctypes.c_size_t(0)
                if k32.ReadProcessMemory(hProc, ctypes.c_void_p(ctx.Rcx), buf, 0x100, ctypes.byref(r)):
                    data=buf.raw[:r.value]
                    print("  buffer:", data[:64].hex())
                    idx=data.find(b'PTITCTF')
                    if idx!=-1:
                        print("  FLAG:", data[idx:idx+100]); found.append(data[idx:idx+100])
                # restore byte, continue at bp
                k32.WriteProcessMemory(hProc, ctypes.c_void_p(bp_va), ctypes.byref(ctypes.c_byte(0xff)), 1, None)
                ctx.Rip=bp_va
                k32.SetThreadContext(pi.hThread, ctypes.byref(ctx))
    if code==EXIT_PROCESS_DEBUG_EVENT:
        break
    k32.ContinueDebugEvent(de.dwProcessId, de.dwThreadId, 0x2)
    count+=1
print("found flags:", found)
k32.TerminateProcess(hProc, 0)
