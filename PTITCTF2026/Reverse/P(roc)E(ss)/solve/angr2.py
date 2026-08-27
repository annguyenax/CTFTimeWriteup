#!/usr/bin/env python3
import angr, sys
import logging
logging.getLogger('angr').setLevel('ERROR')
logging.getLogger('pyvex').setLevel('ERROR')

p = angr.Project('live_chall.exe', auto_load_libs=False)
# provide stdin "4mCnFu.exe"
state = p.factory.entry_state(args=['live_chall.exe'], stdin=angr.SimFileStream(name='stdin', content=b'4mCnFu.exe\n'))
sm = p.factory.simulation_manager(state)
# explore to the message print
sm.explore(find=0x14000264d)
print("found:", len(sm.found))
for s in sm.found[:3]:
    print("stdout:", s.posix.dumps(1))
    # dump memory looking for PTITCTF
    try:
        for addr in range(0x140000000, 0x140010000, 0x1000):
            try:
                mem = s.memory.load(addr, 0x1000)
                if b'PTITCTF' in mem or b'sealed' in mem:
                    idx = mem.find(b'PTITCTF') if b'PTITCTF' in mem else mem.find(b'sealed')
                    print("found at", hex(addr+idx), mem[max(0,idx-4):idx+80])
            except Exception:
                pass
    except Exception as e:
        print("mem err", e)
