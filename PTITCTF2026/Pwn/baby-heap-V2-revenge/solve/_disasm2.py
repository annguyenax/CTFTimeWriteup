from capstone import *
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge\files\_ex\public\chall"
data=open(B,"rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
# disassemble text linearly from 0x12c0 (main area) to 0x1b00
for ins in md.disasm(data[0x12c0:0x1b00], 0x12c0):
    print(f"{ins.address:#x}: {ins.mnemonic}\t{ins.op_str}")
