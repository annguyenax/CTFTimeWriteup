from capstone import *
B=r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge\files\_ex\public\chall"
data=open(B,"rb").read()
md=Cs(CS_ARCH_X86,CS_MODE_64)
for name,start,end in [("SIGALRM handler",0x1cd0,0x1d00),("sub_1c00 heap",0x1c00,0x1d00),("sub_1d00 read_input",0x1d00,0x1da0),("0x1ae4",0x1ae4,0x1c00)]:
    print(f"===== {name} {start:#x} =====")
    for ins in md.disasm(data[start:end], start):
        print(f"{ins.address:#x}: {ins.mnemonic}\t{ins.op_str}")
