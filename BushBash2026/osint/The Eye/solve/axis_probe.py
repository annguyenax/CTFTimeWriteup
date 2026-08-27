import contextlib
import io
import sys
from itertools import combinations

import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from scipy.spatial import cKDTree


with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc


# Poem order, then Alcyone as an unused geometric anchor.
p = np.array([
    [56.4567, 24.3678], [56.3021, 24.4672], [56.4771, 24.5547],
    [56.2008, 24.2894], [57.2967, 24.1367], [56.5817, 23.9483],
    [56.21875, 24.1133], [57.2904, 24.0533], [56.87125, 24.1050],
])
points = np.array([[w[0], w[1]] for w in oc.words])
tree = cKDTree(points)
u0, v0 = np.triu_indices(len(points), 1)
u_all, v_all = np.r_[u0, v0], np.r_[v0, u0]
q = points[v_all] - points[u_all]
ciphertext = open("prayer.enc", "rb").read()

best = []
tried = set()
for a, b in combinations(range(9), 2):
    dp = p[b] - p[a]
    if np.min(np.abs(dp)) < 1e-5:
        continue
    scales = q / dp
    keep = (
        (np.abs(scales[:, 0]) > 20) & (np.abs(scales[:, 0]) < 5000)
        & (np.abs(scales[:, 1]) > 20) & (np.abs(scales[:, 1]) < 5000)
    )
    uu, ss = u_all[keep], scales[keep]
    pred = (p[None, :, :] - p[a]) * ss[:, None, :] + points[uu, None, :]
    dist, idx = tree.query(pred.reshape(-1, 2))
    dist, idx = dist.reshape(-1, 9), idx.reshape(-1, 9)
    unique = np.array([len(set(row)) == 9 for row in idx])
    norm = np.sqrt(np.abs(ss[:, 0] * ss[:, 1]))
    score = np.sqrt(np.mean(dist ** 2, axis=1)) / norm
    for ci in np.flatnonzero(unique & (score < 0.03)):
        signature = tuple(idx[ci, :8])
        if signature in tried:
            continue
        tried.add(signature)
        codes = [oc.codes[int(i)] for i in idx[ci, :8]]
        if all(codes):
            keyhex = "".join(codes)
            try:
                plain = unpad(AES.new(bytes.fromhex(keyhex), AES.MODE_ECB).decrypt(ciphertext), 16)
                printable = sum(c in b"\r\n\t" or 32 <= c < 127 for c in plain) / len(plain)
                if b"bushbash{" in plain.lower() or printable > 0.85:
                    print("AES HIT", keyhex, repr(plain))
                    print("indices", idx[ci].tolist())
                    print("codes", codes)
                    print("dist", np.round(dist[ci], 3).tolist())
                    print("scales", ss[ci].tolist(), "score", float(score[ci]))
            except ValueError:
                pass
        best.append((float(score[ci]), float(np.max(dist[ci])), idx[ci].copy(), ss[ci].copy(), dist[ci].copy(), codes))

best.sort(key=lambda row: (row[0], row[1]))
for score, maxdist, idx, scales, dist, codes in best[:30]:
    print("candidate", score, maxdist, "indices", idx.tolist())
    print("codes", codes, "key", "".join(codes) if all(codes) else None)
    print("scales", scales.tolist(), "dist", np.round(dist, 3).tolist())
