import base64, heapq, itertools
import numpy as np

grid = np.array([list(x) for x in [
    "xuElolW1", "qVNbisNY", "$jjmWa8U", "Hyulhbah",
    "JG30xXd$", "bla715XZ", "mvsTY0sR", "dbd9mZJ!",
]])

def d2xy(n, d):
    x = y = 0; s = 1
    while s < n:
        rx = 1 & (d // 2); ry = 1 & (d ^ rx)
        if ry == 0:
            if rx: x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx; y += s * ry; d //= 4; s *= 2
    return x, y

row = [(r,c) for r in range(8) for c in range(8)]
paths = [("row", row), ("col", [(r,c) for c in range(8) for r in range(8)]),
         ("hilbert", [(y,x) for x,y in (d2xy(8,d) for d in range(64))]),
         ("snake", [(r, c if r % 2 == 0 else 7-c) for r in range(8) for c in range(8)])]
paths.append(("z", sorted(row, key=lambda q: sum((((q[1]>>i)&1) << (2*i)) | (((q[0]>>i)&1) << (2*i+1)) for i in range(3)))))

best = []
for name, path in paths:
    for transform in range(8):
        a = np.rot90(grid, transform % 4)
        if transform >= 4: a = np.fliplr(a)
        for reverse in (False, True):
            use = path[::-1] if reverse else path
            text = "".join(a[r,c] for r,c in use)
            for dollar, bang in itertools.product("+/=", repeat=2):
                encoded = text.replace("$", dollar).replace("!", bang)
                for shift in range(4):
                    try: decoded = base64.b64decode(encoded[shift:] + "===")
                    except Exception: continue
                    printable = sum(32 <= c < 127 or c in (10,13) for c in decoded) / max(1, len(decoded))
                    score = printable + (1 if b"bush" in decoded.lower() else 0)
                    heapq.heappush(best, (score, name, transform, reverse, dollar, bang, shift, repr(decoded)))
                    if len(best) > 30: heapq.heappop(best)
for item in sorted(best, reverse=True): print(item)
