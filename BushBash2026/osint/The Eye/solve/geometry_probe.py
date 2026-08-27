import contextlib
import io
from itertools import combinations

import numpy as np
from scipy.spatial import cKDTree


with contextlib.redirect_stdout(io.StringIO()):
    import sys
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc


# Greek Pleiades coordinates corresponding to the eight poem lines, followed
# by Alcyone/Matariki as a ninth geometric anchor.
radec = np.array([
    [56.4567, 24.3678],   # Maia / Waiti
    [56.3021, 24.4672],   # Taygeta / Waita
    [56.4771, 24.5547],   # Sterope / Pohutukawa
    [56.2008, 24.2894],   # Celaeno / Hiwa-i-te-rangi
    [57.2967, 24.1367],   # Pleione / Tupu-a-nuku
    [56.5817, 23.9483],   # Merope / Ururangi
    [56.21875, 24.1133],  # Electra / Waipuna-a-rangi
    [57.2904, 24.0533],   # Atlas / Tupu-a-rangi
    [56.87125, 24.1050],  # Alcyone / Matariki
])
template = np.c_[
    (radec[:, 0] - radec[:, 0].mean()) * np.cos(np.deg2rad(24.2)),
    radec[:, 1] - radec[:, 1].mean(),
]

points = np.array([[w[0], w[1]] for w in oc.words])
gray = oc.cv2.cvtColor(oc.im, oc.cv2.COLOR_BGR2GRAY)
gray[oc.mask.astype(bool)] = 0
brightness = []
for cx, cy, *_ in oc.words:
    x0, x1 = max(0, int(cx - 22)), min(gray.shape[1], int(cx + 23))
    y0, y1 = max(0, int(cy - 42)), max(0, int(cy - 5))
    brightness.append(float(gray[y0:y1, x0:x1].sum()))
brightness = np.array(brightness)
brightness_rank = np.empty(len(brightness), dtype=int)
brightness_rank[np.argsort(brightness)[::-1]] = np.arange(1, len(brightness) + 1)
tree = cKDTree(points)
u0, v0 = np.triu_indices(len(points), 1)
u_all = np.r_[u0, v0]
v_all = np.r_[v0, u0]
q = points[v_all] - points[u_all]
qlen = np.linalg.norm(q, axis=1)
qang = np.arctan2(q[:, 1], q[:, 0])

candidates = []
for a, b in combinations(range(9), 2):
    for reflected in (False, True):
        p = template.copy()
        if reflected:
            p[:, 0] *= -1
        dp = p[b] - p[a]
        scales = qlen / np.linalg.norm(dp)
        keep = (scales > 20) & (scales < 3000)
        uu, ss = u_all[keep], scales[keep]
        angles = qang[keep] - np.arctan2(dp[1], dp[0])
        ca, sa = np.cos(angles), np.sin(angles)
        base = p - p[a]
        px = (
            base[:, 0][None, :] * ca[:, None]
            - base[:, 1][None, :] * sa[:, None]
        ) * ss[:, None] + points[uu, 0, None]
        py = (
            base[:, 0][None, :] * sa[:, None]
            + base[:, 1][None, :] * ca[:, None]
        ) * ss[:, None] + points[uu, 1, None]
        pred = np.stack([px, py], axis=2)
        dist, idx = tree.query(pred.reshape(-1, 2))
        dist, idx = dist.reshape(-1, 9), idx.reshape(-1, 9)
        unique = np.array([len(set(row)) == 9 for row in idx])
        norm_rms = np.sqrt(np.mean((dist / ss[:, None]) ** 2, axis=1))
        for ci in np.flatnonzero(unique & (norm_rms < 0.03)):
            candidates.append((
                float(norm_rms[ci]), float(np.max(dist[ci])), reflected,
                float(ss[ci]), idx[ci].copy(), dist[ci].copy(), pred[ci].copy(),
            ))

candidates.sort(key=lambda row: (row[0], row[1]))
seen = set()
for rms, maxdist, reflected, scale, idx, dist, pred in candidates:
    signature = tuple(idx)
    if signature in seen:
        continue
    seen.add(signature)
    codes = [oc.codes[int(i)] for i in idx]
    print(
        "candidate",
        "normalized_rms=", round(rms, 7),
        "maxdist=", round(maxdist, 3),
        "reflection=", reflected,
        "scale=", round(scale, 3),
    )
    print("indices", idx.tolist())
    print("codes", codes)
    print("brightness_rank", brightness_rank[idx].tolist())
    print("dist", np.round(dist, 3).tolist())
    print("key", "".join(codes[:8]) if all(codes[:8]) else None)
    if len(seen) >= 30:
        break
