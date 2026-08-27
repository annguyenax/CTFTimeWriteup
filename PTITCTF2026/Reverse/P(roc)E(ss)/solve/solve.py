import angr
import sys

proj = angr.Project('/data/chall.exe', auto_load_libs=False)

# The decoy branch is at 14000243c. We want to avoid it!
# Also there's another decoy at 14000245b.
# The good branch seems to go to 140002467, and then maybe it prints the real flag?
# Let's just find the state that reaches the end of the good block or a puts call inside the good block!

simgr = proj.factory.simgr()
# We want to find a state that does NOT go to 14000243c, 14000245b, 140002492
# And reaches 1400024c7 (which is the puts call for the real flag!)
# Oh wait, 1400024c7 is a call to puts!
# Let's find 0x1400024c7.

simgr.explore(find=0x1400024c7, avoid=[0x14000243c, 0x14000245b, 0x140002492])

if simgr.found:
    print('Found path!')
    s = simgr.found[0]
    # Evaluate stdout
    print(s.posix.dumps(1))
else:
    print('No path found')
