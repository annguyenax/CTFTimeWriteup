#!/usr/bin/env python3
import angr, sys, logging
logging.getLogger('angr').setLevel('ERROR')
logging.getLogger('pyvex').setLevel('ERROR')

p = angr.Project('live_chall_patched.exe', auto_load_libs=False)
# symbolic stdin to solve for the correct input
state = p.factory.entry_state(args=['live_chall_patched.exe'])
sm = p.factory.simulation_manager(state)
sm.explore(find=0x14000264d, timeout=600)
print("found:", len(sm.found))
for s in sm.found[:5]:
    print("stdout:", s.posix.dumps(1))
    inp = s.posix.dumps(0)
    print("stdin:", inp)
    try:
        for off in range(0,0x10000,0x1000):
            try:
                mem = s.memory.load(0x140000000+off, 0x1000)
            except Exception:
                continue
            if b'PTITCTF' in mem:
                idx=mem.find(b'PTITCTF')
                print("FLAG in mem:", hex(0x140000000+off+idx), mem[idx:idx+80])
    except Exception as e:
        print("mem err", e)
