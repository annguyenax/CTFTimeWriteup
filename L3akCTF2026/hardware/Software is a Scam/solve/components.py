#!/usr/bin/env python3
"""Connected-component analysis of black pixels in auth.png.
Prints component bboxes (sorted), and flags small dense clusters (candidate text).
"""
from PIL import Image
import numpy as np
from collections import deque

PATH = r"D:\download\CTFTimeWriteup\L3akCTF2026\hardware\Software is a Scam\files\auth.png"
im = Image.open(PATH).convert("L")
a = np.asarray(im, dtype=np.uint8)
dark = a < 128
h, w = dark.shape

visited = np.zeros_like(dark, dtype=bool)
comps = []
for y0 in range(h):
    for x0 in range(w):
        if dark[y0, x0] and not visited[y0, x0]:
            # BFS
            q = deque([(x0, y0)])
            visited[y0, x0] = True
            xs, ys = [], []
            while q:
                x, y = q.popleft()
                xs.append(x); ys.append(y)
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h and dark[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        q.append((nx, ny))
            comps.append((min(xs), min(ys), max(xs), max(ys), len(xs)))

comps.sort(key=lambda c: (c[1], c[0]))
print(f"total components: {len(comps)}")
# stats
import statistics
sizes = sorted(c[4] for c in comps)
print("size percentiles:", sizes[len(sizes)//100], sizes[len(sizes)//10], sizes[len(sizes)//2], sizes[-1])

# candidate text: component width between 3 and 60, height between 4 and 40, not super wide
print("\n--- candidate text glyphs (w<=60,h<=40) grouped by row ---")
text = [c for c in comps if 3 <= (c[2]-c[0]) <= 60 and 4 <= (c[3]-c[1]) <= 40 and c[4] >= 6]
# group by row: sort by y
text.sort(key=lambda c: (c[1]//30, c[0]))
cur = None
for c in text:
    row = c[1] // 30
    if cur != row:
        print(f"\nrow~{row*30}: ", end="")
        cur = row
    print(f"({c[0]},{c[1]},{c[2]},{c[3]},s{c[4]}) ", end="")
print()

# big components (blocks/wires) summary
print("\n--- large components (w>60 or h>60) ---")
big = [c for c in comps if (c[2]-c[0]) > 60 or (c[3]-c[1]) > 60]
for c in sorted(big, key=lambda c: (c[1], c[0]))[:80]:
    print(f"  x{c[0]}-{c[2]} y{c[1]}-{c[3]} size={c[4]}")
