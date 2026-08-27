import sys
UP,DOWN,LEFT,RIGHT=1,2,4,8
SIZE=16
DIRS={'U':(-1,0,UP),'D':(1,0,DOWN),'L':(0,-1,LEFT),'R':(0,1,RIGHT)}
NORTH=[(1,4),(1,14),(2,1),(3,11),(4,6),(4,15),(6,0),(7,3),(7,7),(7,8),(7,10),(7,13),(8,5),(9,7),(9,8),(10,1),(10,13),(12,0),(12,9),(12,15),(13,5),(13,14),(14,3),(14,10)]
WEST=[(0,2),(0,10),(1,4),(1,14),(2,2),(2,11),(3,7),(6,3),(6,14),(7,7),(7,9),(8,6),(8,7),(8,9),(9,2),(9,13),(11,10),(13,6),(13,15),(14,3),(14,10),(15,7),(15,12)]
ROBOTS='RGBY'
# sandbox.py exec's this with `state` (the 6-byte game state) already in scope
pos=[divmod(b,SIZE) for b in state[:4]]
tr=state[4]; tp=divmod(state[5],SIZE)
walls=[[0]*SIZE for _ in range(SIZE)]
for i in range(SIZE):
    walls[0][i]|=UP; walls[SIZE-1][i]|=DOWN; walls[i][0]|=LEFT; walls[i][SIZE-1]|=RIGHT
for r,c in NORTH:
    walls[r][c]|=UP; walls[r-1][c]|=DOWN
for r,c in WEST:
    walls[r][c]|=LEFT; walls[r][c-1]|=RIGHT
def dest(p,d):
    dr,dc,w=DIRS[d]; r,c=p; occ=set(pos)
    while not walls[r][c]&w and (r+dr,c+dc) not in occ:
        r,c=r+dr,c+dc
    return (r,c)
import collections
start=tuple(pos)
if tr<4:
    def win(s): return s[tr]==tp
else:
    def win(s): return tp in s
if win(start):
    print(''); sys.exit()
q=collections.deque([start]); par={start:None}; order=list(range(4))
while q:
    cur=q.popleft()
    for i in order:
        p=cur[i]; occ=set(cur)
        for d in DIRS:
            dr,dc,w=DIRS[d]; r,c=p
            while not walls[r][c]&w and (r+dr,c+dc) not in occ:
                r,c=r+dr,c+dc
            nd=(r,c)
            if nd==p: continue
            nxt=list(cur); nxt[i]=nd; nxt=tuple(nxt)
            if nxt in par: continue
            par[nxt]=(cur,i,d)
            if win(nxt):
                path=[]; node=nxt
                while par[node] is not None:
                    prev,i,d=par[node]; path.append(ROBOTS[i]+d); node=prev
                print(' '.join(reversed(path))); sys.exit()
            q.append(nxt)
print('')
