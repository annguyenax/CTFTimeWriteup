#!/usr/bin/env python3
"""
ricochet robots — L3akCTF 2026 (koth)

Offline solver / PoC bot for the KoTH sandbox.

The handout gives us the full game engine (game.py), the sandbox (sandbox.py)
and the Dockerfile. The KoTH server (dead) constructs a Game, hex-sends
g.to_bytes() (6 bytes: 4 robot positions + target robot index + target cell),
then hex-sends your Python source which is `exec`'d with `state` available.
Your program must print a space-separated list of legal moves that solve the
board; `run_solution` replays them and measures wall-clock time.

Because START, the wall layout and the 17 targets are FIXED in the handout, the
whole puzzle space is locally determinable:
  * BFS over the 4-robot sliding state space yields shortest solutions for ANY
    state (also handles server-side randomisation if it ever existed).
  * A precomputed optimal-move table for the 17 fixed targets makes the in-sandbox
    bot a pure lookup -> instant answer (fastest possible for this KoTH).

Outputs (relative to this file):
  evidence/states_hex.txt          - the 17 fixed states as hex (as sent to sandbox)
  evidence/solutions.txt           - optimal move count + solution per target
  evidence/verify.txt              - replay verification results
  evidence/bot_source.py           - the bot source we would submit
  evidence/bot_source.hex          - hex-encoded bot source (submission payload)
"""

import os
import sys
import time
from collections import deque

UP, DOWN, LEFT, RIGHT = 1, 2, 4, 8

SIZE = 16

DIRECTIONS = {
    "U": (-1, 0, UP),
    "D": (1, 0, DOWN),
    "L": (0, -1, LEFT),
    "R": (0, 1, RIGHT),
}

COLORS = ("red", "green", "blue", "yellow")
SHAPES = ("circle", "triangle", "diamond", "ring")
SYMBOLS = {4 * i + j + 1: f"{c} {s}" for i, c in enumerate(COLORS) for j, s in enumerate(SHAPES)}
SYMBOLS[17] = "wild"

NORTH_WALLS = [
    (1, 4), (1, 14), (2, 1), (3, 11), (4, 6), (4, 15), (6, 0), (7, 3),
    (7, 7), (7, 8), (7, 10), (7, 13), (8, 5), (9, 7), (9, 8), (10, 1),
    (10, 13), (12, 0), (12, 9), (12, 15), (13, 5), (13, 14), (14, 3), (14, 10),
]

WEST_WALLS = [
    (0, 2), (0, 10), (1, 4), (1, 14), (2, 2), (2, 11), (3, 7), (6, 3),
    (6, 14), (7, 7), (7, 9), (8, 6), (8, 7), (8, 9), (9, 2), (9, 13),
    (11, 10), (13, 6), (13, 15), (14, 3), (14, 10), (15, 7), (15, 12),
]

TARGETS = {
    (15, 6): 1, (1, 14): 2, (2, 11): 3, (9, 1): 4,
    (9, 13): 5, (6, 3): 6, (14, 10): 7, (8, 5): 8,
    (11, 0): 9, (13, 5): 10, (2, 1): 11, (6, 13): 12,
    (11, 9): 13, (1, 4): 14, (14, 3): 15, (3, 6): 16,
    (13, 14): 17,
}

ROBOTS = "RGBY"

START = {"R": (14, 2), "G": (13, 11), "B": (3, 7), "Y": (1, 3)}

TARGET_LIST = [(ROBOTS[(s - 1) // 4] if s < 17 else None, pos) for pos, s in TARGETS.items()]

HERE = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.join(HERE, "evidence")
os.makedirs(EVID, exist_ok=True)


# --------------------------------------------------------------------------
# game model (mirrors handout game.py exactly, self-contained)
# --------------------------------------------------------------------------
class Game:
    def __init__(self, target):
        self.walls = [[0] * SIZE for _ in range(SIZE)]
        for i in range(SIZE):
            self.walls[0][i] |= UP
            self.walls[SIZE - 1][i] |= DOWN
            self.walls[i][0] |= LEFT
            self.walls[i][SIZE - 1] |= RIGHT
        for r, c in NORTH_WALLS:
            self.walls[r][c] |= UP
            self.walls[r - 1][c] |= DOWN
        for r, c in WEST_WALLS:
            self.walls[r][c] |= LEFT
            self.walls[r][c - 1] |= RIGHT
        self.symbols = [[TARGETS.get((r, c), 0) for c in range(SIZE)] for r in range(SIZE)]
        self.robots = dict(START)
        self.target = target

    def cell(self, row, col):
        occupant = next((n for n, p in self.robots.items() if p == (row, col)), None)
        return (self.walls[row][col], self.symbols[row][col], occupant)

    def _destination(self, robot, direction):
        dr, dc, wall = DIRECTIONS[direction]
        r, c = self.robots[robot]
        occupied = set(self.robots.values())
        while not self.walls[r][c] & wall and (r + dr, c + dc) not in occupied:
            r, c = r + dr, c + dc
        return (r, c)

    def is_legal(self, move):
        if len(move) != 2 or move[0] not in self.robots or move[1] not in DIRECTIONS:
            return False
        return self._destination(move[0], move[1]) != self.robots[move[0]]

    def make_move(self, move):
        if not self.is_legal(move):
            raise ValueError(f"illegal move: {move!r}")
        self.robots[move[0]] = self._destination(move[0], move[1])

    def legal_moves(self):
        return [r + d for r in self.robots for d in DIRECTIONS if self.is_legal(r + d)]

    def is_win(self):
        robot, pos = self.target
        if robot is None:
            return pos in self.robots.values()
        return self.robots[robot] == pos

    def to_bytes(self):
        robot, (r, c) = self.target
        cells = [self.robots[n] for n in ROBOTS]
        return bytes(
            [r * SIZE + c for r, c in cells]
            + [ROBOTS.index(robot) if robot else len(ROBOTS), r * SIZE + c]
        )

    @classmethod
    def from_bytes(cls, data):
        robot = ROBOTS[data[4]] if data[4] < len(ROBOTS) else None
        game = cls((robot, divmod(data[5], SIZE)))
        game.robots = dict(zip(ROBOTS, (divmod(b, SIZE) for b in data[:4])))
        return game

    def copy(self):
        game = Game(self.target)
        game.robots = dict(self.robots)
        return game


# --------------------------------------------------------------------------
# BFS solver — shortest sequence of moves for an arbitrary state
# --------------------------------------------------------------------------
def solve_bfs(robots, target):
    """robots: dict name->(r,c); target: (robot|None, (r,c)). Returns list of moves."""
    g = Game(target)
    g.robots = dict(robots)

    start = tuple(robots[n] for n in ROBOTS)
    goal_robot, goal_pos = target

    if goal_robot is not None:
        def is_goal(s):
            return s[ROBOTS.index(goal_robot)] == goal_pos
    else:
        def is_goal(s):
            return goal_pos in s

    if is_goal(start):
        return []

    # precompute slide: for every cell + direction, the wall-stop position and
    # the cells passed through (used to find the stop when a robot blocks).
    # Simpler: inline slide simulation per move (SIZE is small, BFS is fine).
    frontier = deque([start])
    parent = {start: None}  # state -> (prev_state, move)
    order = list(ROBOTS)

    while frontier:
        cur = frontier.popleft()
        g.robots = dict(zip(ROBOTS, cur))
        for name in order:
            for d in DIRECTIONS:
                dest = g._destination(name, d)
                if dest == g.robots[name]:
                    continue  # illegal / no-op
                nxt = list(cur)
                nxt[order.index(name)] = dest
                nxt = tuple(nxt)
                if nxt not in parent:
                    parent[nxt] = (cur, name + d)
                    if is_goal(nxt):
                        # reconstruct
                        path = []
                        node = nxt
                        while parent[node] is not None:
                            prev, mv = parent[node]
                            path.append(mv)
                            node = prev
                        path.reverse()
                        return path
                    frontier.append(nxt)
    return None  # unsolvable


def solve_from_bytes(data):
    """Solve from the exact 6-byte wire format used by the KoTH server."""
    game = Game.from_bytes(data)
    return solve_bfs(game.robots, game.target)


# --------------------------------------------------------------------------
# precomputed table for the 17 fixed targets (fastest in-sandbox path)
# --------------------------------------------------------------------------
def build_table():
    table = {}
    for target in TARGET_LIST:
        t0 = time.perf_counter()
        sol = solve_bfs(START, target)
        dt = time.perf_counter() - t0
        table[target] = (sol, dt)
    return table


def state_hex(target):
    g = Game(target)
    return g.to_bytes().hex()


# --------------------------------------------------------------------------
# in-sandbox bot source (what we would submit)
# --------------------------------------------------------------------------
BOT_SOURCE = r'''import sys
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
'''


def make_bot_payload():
    return BOT_SOURCE.encode()


# --------------------------------------------------------------------------
# verification helpers
# --------------------------------------------------------------------------
def replay(robots, target, moves):
    """Replay a solution against the handout's rules; return (ok, final_game)."""
    g = Game(target)
    g.robots = dict(robots)
    for mv in moves:
        if not g.is_legal(mv):
            return False, g
        g.make_move(mv)
    return g.is_win(), g


def run_in_sandbox_style(hex_state, hex_src):
    """Emulate sandbox.py + run_solution() locally (no socket): exec src with
    `state` available, collect printed moves, replay and time them."""
    import io
    import contextlib
    buf = io.StringIO()
    src = bytes.fromhex(hex_src).decode()
    ns = {"state": bytes.fromhex(hex_state)}
    t0 = time.perf_counter()
    with contextlib.redirect_stdout(buf):
        exec(src, ns)
    dt = (time.perf_counter() - t0) * 1e9
    moves = buf.getvalue().split()
    game = Game.from_bytes(bytes.fromhex(hex_state))
    for mv in moves:
        if not game.is_legal(mv):
            return False, 0, moves
        game.make_move(mv)
    return game.is_win(), dt, moves


def main():
    print(f"[*] building optimal table for {len(TARGET_LIST)} fixed targets (BFS)...")
    table = build_table()
    table_sorted = sorted(table.items(), key=lambda kv: (kv[1][1], kv[0][1]))

    # --- evidence: states + solutions -------------------------------------
    with open(os.path.join(EVID, "states_hex.txt"), "w") as f:
        for target in TARGET_LIST:
            f.write(f"{target!r:40} {state_hex(target)}\n")

    with open(os.path.join(EVID, "solutions.txt"), "w") as f:
        for target, (sol, dt) in table_sorted:
            f.write(f"target={target!r:40} moves={len(sol):3d} bfs={dt*1000:7.1f}ms  {' '.join(sol)}\n")

    # --- evidence: replay verification -------------------------------------
    with open(os.path.join(EVID, "verify.txt"), "w") as f:
        all_ok = True
        for target, (sol, dt) in table_sorted:
            ok, g = replay(START, target, sol)
            all_ok &= ok
            f.write(f"target={target!r:40} replay_ok={ok} final_positions={g.robots}\n")
        f.write(f"\nALL_OK={all_ok}\n")

    # --- evidence: bot source + payload ------------------------------------
    bot = make_bot_payload()
    with open(os.path.join(EVID, "bot_source.py"), "w") as f:
        f.write(bot.decode())
    with open(os.path.join(EVID, "bot_source.hex"), "w") as f:
        f.write(bot.hex())

    # --- bot end-to-end test through sandbox-style exec ---------------------
    with open(os.path.join(EVID, "bot_test.txt"), "w") as f:
        f.write("bot sandbox-style test (state hex -> moves -> replay)\n")
        f.write("=" * 70 + "\n")
        n_ok = 0
        for target in TARGET_LIST:
            hs = state_hex(target)
            ok, dt_ns, moves = run_in_sandbox_style(hs, bot.hex())
            f.write(f"target={target!r:40} win={ok} t={dt_ns/1e6:8.1f}ms moves={len(moves)} {' '.join(moves)}\n")
            n_ok += ok
        f.write(f"\nBOT_WINS={n_ok}/{len(TARGET_LIST)}\n")

    print(f"[*] table built. optimal move counts per target:")
    for target, (sol, dt) in table_sorted:
        print(f"    {str(target):36} -> {len(sol):3d} moves ({dt*1000:6.1f} ms BFS)")
    print(f"[*] all replays OK: {all_ok}")
    print(f"[*] bot wins {n_ok}/{len(TARGET_LIST)} through sandbox-style exec")
    print(f"[*] evidence written to {EVID}")


if __name__ == "__main__":
    main()
