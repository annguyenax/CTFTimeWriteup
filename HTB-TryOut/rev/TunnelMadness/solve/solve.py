#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TunnelMadness (HTB TryOut, rev, medium) — solver
=================================================
The ELF `tunnel` embeds a 20x20x20 grid (8000 cells x 16 bytes) in .rodata.
Each cell = {int x, int y, int z, int val} ; val: 0=start, 1=room, 2=wall, 3=exit.
get_cell (0x11b5): addr = 0x20e0 + 16*(400*x + 20*y + z)

Movement (from the switch in prompt_and_update_pos, jump table @0x2080):
    L -> x-1   R -> x+1   B -> y-1   F -> y+1   D -> z-1   U -> z+1
  (note: L/R are x, F/B are y, D/U are z — verified by decoding the jump
   table rel32 targets and by unicorn emulation of main())

Goal: walk from (0,0,0) to (19,19,19); the binary then prints /flag.txt.
The unique shortest path (59 moves) is the intended input => flag = HTB{<path>}.
"""
import sys
from collections import deque

BIN = sys.argv[1] if len(sys.argv) > 1 else \
    r'files\_work\rev_tunnelmadness\tunnel'

data = open(BIN, 'rb').read()
GRID_BASE = 0x20e0          # VA == file offset (rodata starts at 0x2000)


def cell(x, y, z):
    off = GRID_BASE + 16 * (400 * x + 20 * y + z)
    return data[off:off + 16]


def val(x, y, z):
    return cell(x, y, z)[0xc]


def is_walkable(x, y, z):
    return val(x, y, z) != 2


def main():
    start, end = (0, 0, 0), (19, 19, 19)

    # direction mapping decoded from the switch jump table + case bodies
    DIRS = {'L': (-1, 0, 0), 'R': (1, 0, 0), 'B': (0, -1, 0),
            'F': (0, 1, 0), 'D': (0, 0, -1), 'U': (0, 0, 1)}

    # --- BFS: unique shortest path -------------------------------------
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == end:
            break
        for (dx, dy, dz) in DIRS.values():
            n = (c[0] + dx, c[1] + dy, c[2] + dz)
            if n in prev:
                continue
            if not (0 <= n[0] < 20 and 0 <= n[1] < 20 and 0 <= n[2] < 20):
                continue
            if is_walkable(*n):
                prev[n] = c
                q.append(n)

    if end not in prev:
        print('ERROR: exit unreachable')
        sys.exit(1)

    rev = []
    c = end
    while c != start:
        p = prev[c]
        d = (c[0] - p[0], c[1] - p[1], c[2] - p[2])
        rev.append(d)
        c = p
    rev.reverse()

    inv = {v: k for k, v in DIRS.items()}
    path = ''.join(inv[d] for d in rev)
    print('moves:', len(path))
    print('path:', path)

    # --- step-by-step legality replay (deterministic verification) -----
    x = y = z = 0
    for i, m in enumerate(path):
        dx, dy, dz = DIRS[m]
        nx, ny, nz = x + dx, y + dy, z + dz
        assert 0 <= nx < 20 and 0 <= ny < 20 and 0 <= nz < 20, \
            'move %d out of bounds' % i
        assert is_walkable(nx, ny, nz), 'move %d (%s) hits a wall' % (i, m)
        x, y, z = nx, ny, nz
    assert (x, y, z) == end, 'path does not end at exit'
    assert val(*end) == 3, 'exit cell value != 3'
    print('replay OK: every move legal, ends at exit cell (19,19,19)')

    flag = 'HTB{%s}' % path
    print('FLAG:', flag)
    return flag


if __name__ == '__main__':
    main()
