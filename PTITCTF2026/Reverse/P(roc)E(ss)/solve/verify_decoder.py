#!/usr/bin/env python3
import angr, struct, logging
logging.getLogger('angr').setLevel('ERROR')
logging.getLogger('pyvex').setLevel('ERROR')
logging.getLogger('cle').setLevel('ERROR')

p = angr.Project('live_chall.exe', auto_load_libs=False)

def call_decoder(ciphertext, length, arg3):
    state = p.factory.blank_state(addr=0x140002379)
    # stack with return address
    rsp = 0x700000000000
    state.regs.rsp = rsp
    state.memory.store(rsp, struct.pack('<Q', 0x140002800))  # ret -> xor eax,eax;ret
    # args
    buf = 0x700000010000
    state.regs.rcx = buf
    state.regs.rdx = length
    state.regs.r8 = arg3
    state.memory.store(buf, ciphertext)
    sm = p.factory.simulation_manager(state)
    sm.explore(find=0x140002800, num_find=1)
    if not sm.found:
        print("no found state; errored:", sm.errored[:1])
        return None
    s = sm.found[0]
    out = s.memory.load(buf, length)
    return bytes(s.solver.eval(out, cast_to=bytes))

# test with known ciphertext (decoy content hex-decoded) arg3=0xa
ct = bytes.fromhex('75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43')
for arg3 in [0xa, 0, 0x39]:
    out = call_decoder(ct, 24, arg3)
    print(f'angr arg3={arg3:#x}: {out.hex() if out else None}')

# also test 22-byte blob and block3
d = open('live_chall.exe','rb').read()
b22 = d[0x3046:0x3046+22]
b3 = d[0x3095:0x3095+39]
for name, blob in [('blob22', b22), ('block3', b3)]:
    out = call_decoder(blob, len(blob), 0xa)
    print(f'angr {name} arg3=0xa: {out.hex() if out else None}')
    print(f'        ascii: {out!r}' if out else '')
