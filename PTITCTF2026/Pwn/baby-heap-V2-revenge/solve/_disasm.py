from capstone import *
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge\files\_ex\public\chall"
data=open(B,"rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
for off in range(0x12c0, 0x1d00):
    insns=list(md.disasm(data[off:off+8],off))
    if insns:
        i=insns[0]
        print(f"{i.address:#x}: {i.mnemonic}\t{i.op_str}")
