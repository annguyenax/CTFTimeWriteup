import contextlib
import io
import itertools
import sys

import cv2
import numpy as np
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scipy.spatial import cKDTree
from skimage.transform import AffineTransform


with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc


image = cv2.imread("dots.png")
b, g, r = cv2.split(image)
red = (r > 90) & (r > g * 1.35) & (r > b * 1.35)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray[cv2.dilate(red.astype("uint8"), np.ones((7, 7), np.uint8)) > 0] = 0
n, labels, stats, _ = cv2.connectedComponentsWithStats((gray > 15).astype("uint8"))
flat = labels.ravel()
weights = gray.ravel().astype(float)
yy, xx = np.indices(gray.shape)
flux = np.bincount(flat, weights=weights, minlength=n)
sx = np.bincount(flat, weights=weights * xx.ravel(), minlength=n)
sy = np.bincount(flat, weights=weights * yy.ravel(), minlength=n)
valid = np.array([i for i in range(1, n) if stats[i, 4] >= 3 and flux[i] > 0])
valid = valid[np.argsort(flux[valid])[::-1]]
image_stars = np.array([[sx[i] / flux[i], sy[i] / flux[i]] for i in valid])

gaia = pd.read_csv("gaia_pleiades.csv").sort_values("phot_g_mean_mag")
catalog = gaia[["ra", "dec"]].to_numpy()


def triangles(points, count):
    rows = []
    for ids in itertools.combinations(range(min(count, len(points))), 3):
        tri = points[list(ids)]
        d01 = np.linalg.norm(tri[0] - tri[1])
        d02 = np.linalg.norm(tri[0] - tri[2])
        d12 = np.linalg.norm(tri[1] - tri[2])
        sides = np.sort([d01, d02, d12])
        if sides[0] < 1e-9 or sides[0] / sides[2] < 0.12:
            continue
        # Canonical vertex order: shortest to longest opposite side.
        opposite = np.array([d12, d02, d01])
        order = np.argsort(opposite)
        rows.append((sides[:2] / sides[2], np.array(ids)[order]))
    return rows


cat_tri = triangles(catalog, 90)
img_tri = triangles(image_stars, 90)
cat_desc = np.array([row[0] for row in cat_tri])
desc_tree = cKDTree(cat_desc)

# Keep only globally strongest shape matches before the more expensive
# whole-catalog consensus scoring.
shortlist = []
for desc, ids in img_tri:
    dist, ci = desc_tree.query(desc, k=2)
    for d, j in zip(np.atleast_1d(dist), np.atleast_1d(ci)):
        shortlist.append((float(d), cat_tri[int(j)][1], ids))
shortlist.sort(key=lambda row: row[0])

img_eval = image_stars[:700]
img_tree = cKDTree(img_eval)
results = []
seen = set()
for shape_error, cat_ids, img_ids in shortlist[:10000]:
    signature = (tuple(cat_ids), tuple(img_ids))
    if signature in seen:
        continue
    seen.add(signature)
    # Try both orientations because triangle side ratios discard handedness.
    for perm in (img_ids, img_ids[[0, 2, 1]]):
        model = AffineTransform()
        if not model.estimate(catalog[cat_ids], image_stars[perm]):
            continue
        projected = model(catalog[:700])
        d, nearest_rank = img_tree.query(projected)
        inside = (
            (projected[:, 0] >= 0) & (projected[:, 0] < image.shape[1])
            & (projected[:, 1] >= 0) & (projected[:, 1] < image.shape[0])
        )
        # Bright stars should land within a few pixels; score both strict and
        # loose consensus to tolerate centroid saturation.
        strict = int(np.sum(inside & (d < 4)))
        loose = int(np.sum(inside & (d < 10)))
        matched = inside & (d < 8)
        rank_delta = np.abs(np.log1p(nearest_rank) - np.log1p(np.arange(len(projected))))
        rank_score = float(np.sum(np.exp(-rank_delta[matched])))
        top_hits = int(np.sum(matched[:40] & (nearest_rank[:40] < 80)))
        results.append((top_hits, rank_score, strict, loose, -shape_error, model.params.copy()))

results.sort(key=lambda row: row[:5], reverse=True)
word_points = np.array([[w[0], w[1]] for w in oc.words])
word_tree = cKDTree(word_points)
target = np.array([
    [56.4567958643, 24.3675414247],  # Maia
    [56.3021628561, 24.4670639573],  # Taygeta
    [56.4770850000, 24.5543050000],  # Sterope
    [56.2009920000, 24.2892680000],  # Celaeno
    [57.2968310000, 24.1364980000],  # Pleione
    [56.5816714492, 23.9481438102],  # Merope
    [56.2190045645, 24.1131330436],  # Electra
    [57.2906889329, 24.0532118300],  # Atlas
])
ciphertext = open("prayer.enc", "rb").read()

for rank, (top_hits, rank_score, strict, loose, negerr, params) in enumerate(results[:30], 1):
    model = AffineTransform(matrix=params)
    pred = model(target)
    wd, wi = word_tree.query(pred)
    codes = [oc.codes[int(i)] for i in wi]
    keyhex = "".join(codes) if all(codes) else None
    sd, si = img_tree.query(pred)
    print("MODEL", rank, "top_hits", top_hits, "rank_score", rank_score, "strict", strict, "loose", loose, "shape_error", -negerr)
    print("params", params.tolist())
    print("target_xy", np.round(pred, 2).tolist())
    print("target_star_dist", np.round(sd, 2).tolist(), "target_star_rank", (si + 1).tolist())
    print("word_dist", np.round(wd, 2).tolist(), "indices", wi.tolist())
    print("codes", codes, "key", keyhex)
    if keyhex:
        try:
            plain = unpad(AES.new(bytes.fromhex(keyhex), AES.MODE_ECB).decrypt(ciphertext), 16)
            printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
            if b"bushbash{" in plain.lower() or printable > 0.85:
                print("AES HIT", repr(plain))
        except ValueError:
            pass
