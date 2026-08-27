import contextlib
import io
import sys
from itertools import combinations

import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

im = cv2.imread("dots.png")
b0, g0, r0 = cv2.split(im)
red = (r0 > 90) & (r0 > g0 * 1.35) & (r0 > b0 * 1.35)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"), np.ones((7, 7), np.uint8)) > 0] = 0
n, labels, stats, _ = cv2.connectedComponentsWithStats((gray > 15).astype("uint8"))
flat = labels.ravel()
wt = gray.ravel().astype(float)
yy, xx = np.indices(gray.shape)
flux = np.bincount(flat, weights=wt, minlength=n)
sx = np.bincount(flat, weights=wt * xx.ravel(), minlength=n)
sy = np.bincount(flat, weights=wt * yy.ravel(), minlength=n)
valid = np.array([i for i in range(1, n) if stats[i, 4] >= 3 and flux[i] > 0])
valid = valid[np.argsort(flux[valid])[::-1]]
stars = np.array([[sx[i] / flux[i], sy[i] / flux[i]] for i in valid])
star_tree = cKDTree(stars)

radec = np.array([
    [56.4567958643, 24.3675414247], [56.3021628561, 24.4670639573],
    [56.4770850000, 24.5543050000], [56.2009920000, 24.2892680000],
    [57.2968310000, 24.1364980000], [56.5816714492, 23.9481438102],
    [56.2190045645, 24.1131330436], [57.2906889329, 24.0532118300],
    [56.8712508473, 24.1049344752],
])
p = np.c_[(radec[:, 0] - radec[:, 0].mean()) * np.cos(np.deg2rad(24.2)), radec[:, 1] - radec[:, 1].mean()]
expected_rank = np.array([4, 6, 9, 8, 7, 5, 3, 2, 1])

anchor = stars[:120]
u0, v0 = np.triu_indices(len(anchor), 1)
u_all, v_all = np.r_[u0, v0], np.r_[v0, u0]
q = anchor[v_all] - anchor[u_all]
qlen = np.linalg.norm(q, axis=1)
qang = np.arctan2(q[:, 1], q[:, 0])
word_points = np.array([[w[0], w[1]] for w in oc.words])
word_tree = cKDTree(word_points)
ciphertext = open("prayer.enc", "rb").read()

best = []
tried = set()
for a, b in combinations(range(9), 2):
    for reflected in (False, True):
        pp = p.copy()
        if reflected:
            pp[:, 0] *= -1
        dp = pp[b] - pp[a]
        scales = qlen / np.linalg.norm(dp)
        keep = (scales > 100) & (scales < 3500)
        uu, ss = u_all[keep], scales[keep]
        angle = qang[keep] - np.arctan2(dp[1], dp[0])
        ca, sa = np.cos(angle), np.sin(angle)
        base = pp - pp[a]
        px = (base[:, 0][None] * ca[:, None] - base[:, 1][None] * sa[:, None]) * ss[:, None] + anchor[uu, 0, None]
        py = (base[:, 0][None] * sa[:, None] + base[:, 1][None] * ca[:, None]) * ss[:, None] + anchor[uu, 1, None]
        pred = np.stack([px, py], axis=2)
        dist, idx = star_tree.query(pred.reshape(-1, 2))
        dist, idx = dist.reshape(-1, 9), idx.reshape(-1, 9)
        unique = np.array([len(set(row)) == 9 for row in idx])
        geom = np.sqrt(np.mean((dist / ss[:, None]) ** 2, axis=1))
        # Compare log ranks because flux-to-magnitude is exponential and exact
        # ranks can shift through saturation/cropping.
        rank_cost = np.mean(np.abs(np.log1p(idx + 1) - np.log1p(expected_rank)), axis=1)
        for ci in np.flatnonzero(unique & (geom < 0.035)):
            sig = tuple(idx[ci])
            if sig in tried:
                continue
            tried.add(sig)
            # Associate each predicted source with its label below it.
            # Read labels from the actual matched source centroids, not the
            # approximate projected positions (which may be tens of pixels off).
            wd, wi = word_tree.query(stars[idx[ci]] + [0, 18])
            codes = [oc.codes[int(i)] for i in wi[:8]]
            keyhex = "".join(codes) if all(codes) else None
            if keyhex and np.max(wd[:8]) < 45:
                try:
                    plain = unpad(AES.new(bytes.fromhex(keyhex), AES.MODE_ECB).decrypt(ciphertext), 16)
                    printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
                    if b"bushbash{" in plain.lower() or printable > 0.85:
                        print("AES HIT", keyhex, repr(plain))
                        print("star_ranks", (idx[ci] + 1).tolist(), "codes", codes, "word_dist", wd.tolist())
                except ValueError:
                    pass
            best.append((float(rank_cost[ci] + 20 * geom[ci]), float(geom[ci]), float(rank_cost[ci]), idx[ci].copy(), codes, wd.copy(), dist[ci].copy(), float(ss[ci]), reflected))

best.sort(key=lambda z: z[0])
for z in best[:40]:
    score, geom, rank_cost, idx, codes, wd, dist, scale, reflected = z
    print("candidate score", score, "geom", geom, "rank_cost", rank_cost, "scale", scale, "reflection", reflected)
    print("star_ranks", (idx + 1).tolist(), "codes", codes, "word_dist", np.round(wd, 2).tolist(), "star_dist", np.round(dist, 2).tolist())
