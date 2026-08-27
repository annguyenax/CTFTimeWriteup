#!/usr/bin/env python3
import angr, sys
import logging
logging.getLogger('angr').setLevel('ERROR')

def main():
    p = angr.Project('live_chall.exe', auto_load_libs=False)
    state = p.factory.entry_state()
    sm = p.factory.simulation_manager(state)
    # explore with a cap
    sm.run(n=5000)
    print("done exploring, stash sizes:", {k:len(v) for k,v in sm.stashes.items()})
    flags=set()
    for s in sm.deadended:
        out=s.posix.dumps(1)
        if b'PTITCTF' in out:
            flags.add(out.decode(errors='replace'))
    for f in flags:
        print("FLAG:", f)
    if not flags:
        print("no flag in deadended stdout")

if __name__=='__main__':
    main()
