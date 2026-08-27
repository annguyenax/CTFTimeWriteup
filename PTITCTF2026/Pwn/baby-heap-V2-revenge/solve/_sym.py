from pwn import *
context.log_level="error"
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge\files\_ex\public\chall"
e=ELF(B)
print(e.checksec())
print("== symbols (funcs) ==")
for s,v in sorted(e.symbols.items()):
    if isinstance(v,int) and 0x1000<=v<0x3000:
        print(f"  {v:#x} {s}")
print("== got ==")
for k,v in sorted(e.got.items()):
    print(f"  {k}: {v:#x}")
print("== plt ==")
for f in ["malloc","free","read","write","puts","printf","open","exit","signal","alarm","fgets","strtoull"]:
    try: print(f"  {f}: plt={e.plt[f]:#x} got={e.got[f]:#x}")
    except: pass
