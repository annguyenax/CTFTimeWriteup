import cv2
import numpy as np
import reedsolo
import zxingcpp


IMAGE = r"D:\download\CTFTimeWriteup\BushBash2026\misc\Bliss I\bliss.png"


def placement(rows, cols):
    out = -np.ones((rows, cols, 2), dtype=int)
    pos = 0

    def module(r, c, p, bit):
        if r < 0:
            r += rows
            c += 4 - ((rows + 4) % 8)
        if c < 0:
            c += cols
            r += 4 - ((cols + 4) % 8)
        out[r, c] = p, bit

    def utah(r, c, p):
        points = ((r-2,c-2),(r-2,c-1),(r-1,c-2),(r-1,c-1),
                  (r-1,c),(r,c-2),(r,c-1),(r,c))
        for bit, (rr, cc) in enumerate(points, 1):
            module(rr, cc, p, bit)

    corners = (
        ((rows-1,0),(rows-1,1),(rows-1,2),(0,cols-2),(0,cols-1),(1,cols-1),(2,cols-1),(3,cols-1)),
        ((rows-3,0),(rows-2,0),(rows-1,0),(0,cols-4),(0,cols-3),(0,cols-2),(0,cols-1),(1,cols-1)),
        ((rows-3,0),(rows-2,0),(rows-1,0),(0,cols-2),(0,cols-1),(1,cols-1),(2,cols-1),(3,cols-1)),
        ((rows-1,0),(rows-1,cols-1),(0,cols-3),(0,cols-2),(0,cols-1),(1,cols-3),(1,cols-2),(1,cols-1)),
    )

    def corner(which, p):
        for bit, (r, c) in enumerate(corners[which], 1):
            module(r, c, p, bit)

    r, c = 4, 0
    while True:
        if r == rows and c == 0:
            corner(0, pos); pos += 1
        if r == rows - 2 and c == 0 and cols % 4:
            corner(1, pos); pos += 1
        if r == rows - 2 and c == 0 and cols % 8 == 4:
            corner(2, pos); pos += 1
        if r == rows + 4 and c == 2 and cols % 8 == 0:
            corner(3, pos); pos += 1
        while True:
            if r < rows and c >= 0 and out[r, c, 0] < 0:
                utah(r, c, pos); pos += 1
            r -= 2; c += 2
            if not (r >= 0 and c < cols): break
        r += 1; c += 3
        while True:
            if r >= 0 and c < cols and out[r, c, 0] < 0:
                utah(r, c, pos); pos += 1
            r += 2; c -= 2
            if not (r < rows and c >= 0): break
        r += 3; c += 1
        if not (r < rows or c < cols): break
    return out, pos


def border_and_prefix(size):
    known = np.zeros((size, size), dtype=bool)
    value = np.zeros((size, size), dtype=np.uint8)
    known[:, 0] = True; value[:, 0] = 1
    known[-1, :] = True; value[-1, :] = 1
    known[0, :] = True; value[0, :] = np.arange(size) % 2 == 0
    known[:, -1] = True; value[:, -1] = np.arange(size) % 2 == 1
    place, count = placement(size - 2, size - 2)
    prefix = bytes(x + 1 for x in b"bushbash{")
    for r in range(size - 2):
        for c in range(size - 2):
            pos, bit = place[r, c]
            if 0 <= pos < len(prefix):
                known[r + 1, c + 1] = True
                value[r + 1, c + 1] = (prefix[pos] >> (8 - bit)) & 1
    return known, value, place, count


def main():
    image = cv2.imread(IMAGE)
    sat = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1].astype(float)
    rng = np.random.default_rng(20260731)
    configs = {18: 14, 20: 18, 22: 20, 24: 24, 26: 28}
    winners = []
    for size, nsym in configs.items():
        known, value, place, count = border_and_prefix(size)
        rc = np.argwhere(known)
        sign = np.where(value[known], 1.0, -1.0)
        total = 120000
        p = np.column_stack((
            rng.uniform(940, 1000, total), rng.uniform(695, 760, total),
            rng.uniform(390/size, 490/size, total), rng.uniform(-.2, 1.5, total),
            rng.uniform(-2, 1, total), rng.uniform(195/size, 290/size, total),
            rng.uniform(-.03, .03, total), rng.uniform(-.03, .03, total)))
        best = []
        for lo in range(0, total, 2000):
            q = p[lo:lo+2000]
            r, c = rc[:, 0], rc[:, 1]
            x = np.rint(q[:,0,None]+c*q[:,2,None]+r*q[:,4,None]+c*r*q[:,6,None]).astype(int)
            y = np.rint(q[:,1,None]+c*q[:,3,None]+r*q[:,5,None]+c*r*q[:,7,None]).astype(int)
            a = sat[y, x]; a -= a.mean(axis=1, keepdims=True)
            score = (a*sign).sum(axis=1) / np.sqrt((a*a).sum(axis=1)*(sign*sign).sum()+1e-9)
            ix = np.argpartition(score, -8)[-8:]
            best.extend((float(score[i]), q[i].copy()) for i in ix)
        best.sort(key=lambda item: item[0], reverse=True)
        print(size, best[0][0], np.round(best[0][1], 3), flush=True)
        winners.extend((score, size, nsym, known, value, place, count, q) for score, q in best[:30])

    winners.sort(key=lambda item: item[0], reverse=True)
    for score, size, nsym, known, value, place, count, p in winners[:100]:
        raw = np.empty((size, size), dtype=float)
        for r in range(size):
            for c in range(size):
                vals = []
                for rf in (-.3, 0, .3):
                    for cf in (-.3, 0, .3):
                        x = p[0]+(c+cf)*p[2]+(r+rf)*p[4]+(c+cf)*(r+rf)*p[6]
                        y = p[1]+(c+cf)*p[3]+(r+rf)*p[5]+(c+cf)*(r+rf)*p[7]
                        vals.append(sat[round(y), round(x)])
                raw[r, c] = np.mean(vals)
        for threshold in np.linspace(25, 145, 121):
            matrix = (raw > threshold).astype(np.uint8)
            matrix[known] = value[known]
            codewords = np.zeros(count, dtype=np.uint8)
            reliability = np.full(count, 1e9)
            for r in range(size - 2):
                for c in range(size - 2):
                    pos, bit = place[r, c]
                    if pos >= 0:
                        if matrix[r+1, c+1]: codewords[pos] |= 1 << (8-bit)
                        reliability[pos] = min(reliability[pos], abs(raw[r+1,c+1]-threshold))
            codec = reedsolo.RSCodec(nsym, fcr=1, prim=0x12d)
            order = np.argsort(reliability)
            for erased in range(nsym + 1):
                try:
                    decoded, corrected, _ = codec.decode(bytes(codewords), erase_pos=order[:erased].tolist())
                except reedsolo.ReedSolomonError:
                    continue
                if b"bushbash{" not in bytes(decoded).lower():
                    continue
                print("FLAG CODEWORDS", bytes(decoded))
                return
    print("No flag candidate")


if __name__ == "__main__":
    main()
