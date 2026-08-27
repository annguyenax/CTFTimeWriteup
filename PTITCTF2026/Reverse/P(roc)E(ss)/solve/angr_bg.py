#!/usr/bin/env python3
import angr, sys, logging
logging.getLogger('angr').setLevel('ERROR')
logging.getLogger('pyvex').setLevel('ERROR')
logging.getLogger('cle').setLevel('ERROR')

p = angr.Project('live_chall.exe', auto_load_libs=False)
# hook puts to capture all printed strings
puts_addr = 0x140003798
class PutHook(angr.SimProcedure):
    def run(self, s):
        try:
            data = self.state.mem[s].string.concrete
            print("PUTS:", data)
        except Exception:
            pass
        # return len
        try:
            return self.state.solver.eval(self.state.mem[s].string.concrete_length)
        except Exception:
            return 0
try:
    p.hook(puts_addr, PutHook())
except Exception as e:
    print("hook err", e)

state = p.factory.entry_state(args=['live_chall.exe'])
sm = p.factory.simulation_manager(state)
seen=set()
# run with a budget; capture any stdout that's not the decoy
decoy=b'PTITCTF{75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43}'
flags=set()
count=0
while sm.active and count<200000:
    sm.step()
    count+=1
    if count%2000==0:
        print("active",len(sm.active),"stepped",count, flush=True)
    for s in list(sm.active):
        out=s.posix.dumps(1)
        if b'PTITCTF' in out:
            idx=out.find(b'PTITCTF')
            f=out[idx:idx+120]
            if f!=decoy:
                print("FLAG:", f, flush=True)
                flags.add(f)
            sm.active.remove(s)
    if count>50000 and sm.active:
        # try to find any state reaching main region
        pass
print("done, flags:", list(flags))
for f in flags:
    print("REAL FLAG:", f)
