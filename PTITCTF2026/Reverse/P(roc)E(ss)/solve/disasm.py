#!/usr/bin/env python3
import pefile, capstone, sys
pe=pefile.PE('live_chall.exe')
data=open('live_chall.exe','rb').read()
base=pe.OPTIONAL_HEADER.ImageBase
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def dis(va, n):
    off = 0x400 + (va - (base+0x1000))  # .text VA=0x1000 raw=0x400
    for ins in md.disasm(data[off:off+n], va):
        print('0x%x:'%ins.address, ins.mnemonic, ins.op_str)
if __name__=='__main__':
    va=int(sys.argv[1],16); n=int(sys.argv[2],16) if len(sys.argv)>2 else 0x100
    dis(va,n)
