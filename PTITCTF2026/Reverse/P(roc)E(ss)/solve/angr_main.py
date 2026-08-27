#!/usr/bin/env python3
import angr, logging
logging.getLogger('angr').setLevel('ERROR')
logging.getLogger('pyvex').setLevel('ERROR')

p = angr.Project('live_chall_patched.exe', auto_load_libs=False)
# start at main 0x14000255d of patched binary; provide stdin
state = p.factory.entry_state(args=['live_chall_patched.exe'], stdin=angr.SimFileStream(name='stdin', content=b'4mCnFu.exe\n'))
# hook VirtualProtect (imported)
class VPH(angr.SimProcedure):
    def run(self, lpAddress, dwSize, flNewProtect, lpflOldProtect):
        print("VirtualProtect called on", hex(lpAddress), "size", hex(dwSize))
        self.state.mem[lpflOldProtect].dword = 0x04
        return 1
try:
    p.hook_symbol('VirtualProtect', VPH())
except Exception as e:
    print("hook err", e)
sm = p.factory.simulation_manager(state)
# explore to message print (real-flag path)
sm.explore(find=0x14000264d, timeout=300)
print("found:", len(sm.found))
for s in sm.found[:3]:
    print("stdout:", s.posix.dumps(1))
    # scan memory
    for off in range(0,0x30000,0x1000):
        try: mem=s.memory.load(0x140000000+off, 0x1000)
        except Exception: continue
        if b'PTITCTF' in mem:
            i=mem.find(b'PTITCTF'); print("FLAG:", hex(0x140000000+off+i), mem[i:i+80])
    # also scan heap-ish
    for base in [0x000000, 0x100000000, 0x700000000000]:
        pass
