import contextlib
import io
import itertools
import sys

import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

im = cv2.imread("dots.png")
b, g, r = cv2.split(im)
red = (r > 90) & (r > g * 1.35) & (r > b * 1.35)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"), np.ones((7, 7), np.uint8)) > 0] = 0

# Associate each rendered four-hex label with the compact light source above it.
n, lab, stats, cen = cv2.connectedComponentsWithStats((gray > 15).astype("uint8"))
flat = lab.ravel()
wt = gray.ravel().astype(float)
yy, xx = np.indices(gray.shape)
flux = np.bincount(flat, weights=wt, minlength=n)
sx = np.bincount(flat, weights=wt * xx.ravel(), minlength=n)
sy = np.bincount(flat, weights=wt * yy.ravel(), minlength=n)
valid = np.array([i for i in range(1, n) if stats[i, 4] >= 2 and flux[i] > 0])
src = np.array([[sx[i] / flux[i], sy[i] / flux[i]] for i in valid])
src_flux = flux[valid]
src_tree = cKDTree(src)

words = np.array([[w[0], w[1]] for w in oc.words])
obs = []
obs_flux = []
for x, y in words:
    cand = src_tree.query_ball_point([x, y - 18], 38)
    cand = [j for j in cand if 4 <= y - src[j, 1] <= 40 and abs(x - src[j, 0]) <= 28]
    if cand:
        j = min(cand, key=lambda q: np.linalg.norm(src[q] - [x, y - 18]))
        obs.append(src[j])
        obs_flux.append(src_flux[j])
    else:
        obs.append([x, y - 18])
        obs_flux.append(0)
obs = np.asarray(obs, float)
obs_flux = np.asarray(obs_flux)
tree = cKDTree(obs)

# Maia, Taygeta, Asterope, Celaeno, Pleione, Merope, Electra, Atlas, Alcyone.
radec = np.array([
    [56.4567958643, 24.3675414247], [56.3021628561, 24.4670639573],
    [56.4770850000, 24.5543050000], [56.2009920000, 24.2892680000],
    [57.2968310000, 24.1364980000], [56.5816714492, 23.9481438102],
    [56.2190045645, 24.1131330436], [57.2906889329, 24.0532118300],
    [56.8712508473, 24.1049344752],
])
p = np.c_[(radec[:, 0] - 56.7) * np.cos(np.deg2rad(24.2)), radec[:, 1] - 24.2]

# The maximum-area template triangle gives the most stable affine basis.
areas = []
for tri in itertools.combinations(range(9), 3):
    q = p[list(tri)]
    areas.append((abs(np.cross(q[1] - q[0], q[2] - q[0])), tri))
anchors = max(areas)[1]
base = np.c_[p[list(anchors)], np.ones(3)]
# bary[i] maps the three anchor image points to template point i.
bary = np.c_[p, np.ones(9)] @ np.linalg.inv(base)
print("anchors", anchors, "bary", bary.tolist())

# Brightness is only used as a bounded candidate whitelist.  Deduplicate stars
# because close/overlapping labels can otherwise refer to the same source.
order = np.argsort(obs_flux)[::-1]
bright = []
for i in order:
    if obs_flux[i] <= 0:
        continue
    if all(np.linalg.norm(obs[i] - obs[j]) > 2 for j in bright):
        bright.append(int(i))
    if len(bright) == 130:
        break
bright = np.asarray(bright)

ciphertext = open("prayer.enc", "rb").read()
best = []
tested = set()
batch = []

def process(rows):
    if not rows:
        return
    ids = np.asarray(rows, int)
    q = obs[bright[ids]]  # candidate, three anchors, xy
    pred = np.einsum("ij,njk->nik", bary, q)
    dist, ind = tree.query(pred.reshape(-1, 2))
    dist = dist.reshape(-1, 9)
    ind = ind.reshape(-1, 9)
    # Affine scale proxy and distortion derived from anchor edge matrices.
    src_edges = np.stack([p[anchors[1]] - p[anchors[0]], p[anchors[2]] - p[anchors[0]]], axis=1)
    inv_src = np.linalg.inv(src_edges)
    dst_edges = np.stack([q[:, 1] - q[:, 0], q[:, 2] - q[:, 0]], axis=2)
    mats = dst_edges @ inv_src
    sv = np.linalg.svd(mats, compute_uv=False)
    scale = np.sqrt(sv[:, 0] * sv[:, 1])
    ratio = sv[:, 0] / np.maximum(sv[:, 1], 1e-9)
    rms = np.sqrt(np.mean(dist * dist, axis=1))
    unique = np.array([len(set(x)) == 9 for x in ind])
    keep = unique & (scale > 40) & (scale < 1500) & (ratio < 8) & (rms < 35)
    for k in np.flatnonzero(keep):
        sig = tuple(ind[k, :8])
        if sig in tested:
            continue
        tested.add(sig)
        codes = [oc.codes[int(x)] for x in ind[k, :8]]
        if all(codes):
            keyhex = "".join(codes)
            try:
                plain = unpad(AES.new(bytes.fromhex(keyhex), AES.MODE_ECB).decrypt(ciphertext), 16)
                printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
                if b"bushbash{" in plain.lower() or printable > .85:
                    print("AES HIT", keyhex, repr(plain))
                    print("indices", ind[k].tolist(), "codes", codes, "dist", dist[k].tolist())
            except ValueError:
                pass
        best.append((float(rms[k]), float(ratio[k]), float(scale[k]), ind[k].copy(), dist[k].copy(), codes))

for row in itertools.permutations(range(len(bright)), 3):
    batch.append(row)
    if len(batch) == 20000:
        process(batch)
        batch = []
process(batch)

best.sort(key=lambda z: (z[0], z[1]))
print("tested", len(tested), "bright", len(bright))
for z in best[:50]:
    rms, ratio, scale, ind, dist, codes = z
    print("candidate", rms, ratio, scale, ind.tolist(), codes, np.round(dist, 2).tolist())
