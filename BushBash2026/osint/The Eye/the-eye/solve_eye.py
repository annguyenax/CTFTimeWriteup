import cv2
import numpy as np
from scipy.spatial import cKDTree
from itertools import combinations

IMG = cv2.imread("dots.png")
b, g, r = cv2.split(IMG)
red = ((r > 90) & (r > g * 1.35) & (r > b * 1.35)).astype(np.uint8) * 255
dil = cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 2)))
n, labels, stats, centers = cv2.connectedComponentsWithStats(dil)
words = []
for x, y, w, h, area in stats[1:]:
    if 12 <= w <= 42 and 6 <= h <= 18 and area >= 25:
        words.append((x + w / 2, y + h / 2, x, y, w, h))

# Every code is printed immediately beneath its star.  Locate the brightest
# compact source above/near each code instead of treating text coordinates as
# star coordinates.
gray = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
gray[red > 0] = 0
stars = []
for cx, cy, x, y, w, h in words:
    x0, x1 = max(0, int(cx - 15)), min(gray.shape[1], int(cx + 16))
    y0, y1 = max(0, int(cy - 36)), min(gray.shape[0], int(cy - 6))
    roi = gray[y0:y1, x0:x1]
    # Score peaks by intensity and preference for being about 16 px above text.
    blur = cv2.GaussianBlur(roi, (3, 3), 0)
    candidates = np.argwhere(blur >= max(35, int(blur.max() * .7)))
    if len(candidates) == 0:
        stars.append((cx, cy - 18))
        continue
    scores = []
    for yy, xx in candidates:
        gx, gy = x0 + xx, y0 + yy
        dist = ((gx - cx) / 1.2) ** 2 + (gy - (cy - 17)) ** 2
        scores.append(float(blur[yy, xx]) - .10 * dist)
    yy, xx = candidates[int(np.argmax(scores))]
    stars.append((x0 + float(xx), y0 + float(yy)))

# Associate each label with a globally segmented source.  Using the closest
# centroid to the expected label offset is robust even for faint stars.
clean=gray.copy(); clean[cv2.dilate((red>0).astype('uint8'),np.ones((5,5),np.uint8))>0]=0
nn,slab,sstats,scen=cv2.connectedComponentsWithStats((clean>15).astype('uint8'))
src=[]
for si in range(1,nn):
    if sstats[si,4]>=2: src.append(scen[si])
src=np.asarray(src); stree=cKDTree(src)
obs=[]
for w in words:
    expected=np.array([w[0],w[1]-17])
    cand=stree.query_ball_point(expected,32)
    cand=[j for j in cand if 5 <= w[1]-src[j,1] <= 38 and abs(w[0]-src[j,0])<=24]
    if cand:
        j=min(cand,key=lambda j:np.linalg.norm(src[j]-expected));obs.append(src[j])
    else: obs.append(expected)
obs=np.asarray(obs)
tree = cKDTree(obs)

# J2000 coordinates for the eight children, in the order specified by the poem:
# Maia, Taygeta, Asterope, Celaeno, Pleione, Merope, Electra, Atlas.
ra_dec = np.array([
    [56.4567, 24.3678], [56.3021, 24.4672], [56.4771, 24.5547],
    [56.2008, 24.2894], [57.2967, 24.1367], [56.5817, 23.9483],
    [56.21875, 24.1133], [57.2904, 24.0533],
    [56.87125, 24.1050],
])
template = np.c_[(ra_dec[:, 0] - ra_dec[:, 0].mean()) * np.cos(np.deg2rad(24.2)),
                 ra_dec[:, 1] - ra_dec[:, 1].mean()]

def transform_from_pairs(a, b, u, v, reflected=False):
    p = template.copy()
    if reflected:
        p[:, 0] *= -1
    dp, dq = p[b] - p[a], obs[v] - obs[u]
    scale = np.linalg.norm(dq) / np.linalg.norm(dp)
    ang = np.arctan2(dq[1], dq[0]) - np.arctan2(dp[1], dp[0])
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return (p - p[a]) @ R.T * scale + obs[u], scale

best = []
# Vectorize all observed endpoint pairs.  This avoids millions of tiny tree calls.
u0, v0 = np.triu_indices(len(obs), 1)
u_all = np.r_[u0, v0]
v_all = np.r_[v0, u0]
q = obs[v_all] - obs[u_all]
qlen = np.linalg.norm(q, axis=1)
qang = np.arctan2(q[:, 1], q[:, 0])
for a, b in combinations(range(len(template)), 2):
    for refl in (False, True):
        p = template.copy()
        if refl:
            p[:, 0] *= -1
        dp = p[b] - p[a]
        dplen = np.linalg.norm(dp)
        scale_all = qlen / dplen
        keep = (scale_all > 25) & (scale_all < 1200)
        uu, vv, scales = u_all[keep], v_all[keep], scale_all[keep]
        ang = qang[keep] - np.arctan2(dp[1], dp[0])
        ca, sa = np.cos(ang), np.sin(ang)
        base = p - p[a]
        # [candidate, template-point, xy]
        px = (base[:, 0][None, :] * ca[:, None] - base[:, 1][None, :] * sa[:, None]) * scales[:, None] + obs[uu, 0, None]
        py = (base[:, 0][None, :] * sa[:, None] + base[:, 1][None, :] * ca[:, None]) * scales[:, None] + obs[uu, 1, None]
        preds = np.stack((px, py), axis=2)
        dists, inds = tree.query(preds.reshape(-1, 2))
        dists, inds = dists.reshape(-1, len(template)), inds.reshape(-1, len(template))
        tols = np.maximum(5.0,scales*.05)
        counts = (dists < tols[:, None]).sum(axis=1)
        for ci in np.flatnonzero(counts >= 8):
            mask = dists[ci] < tols[ci]
            if len(set(inds[ci, mask])) != int(counts[ci]):
                continue
            rms = float(np.sqrt(np.mean(dists[ci, mask] ** 2)))
            best.append((int(counts[ci]), -rms, float(scales[ci]), refl,
                         preds[ci], inds[ci], dists[ci]))

best.sort(key=lambda z: (z[0], z[1] / z[2]), reverse=True)
try:
    import ocr_codes as oc
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    ciphertext=open('prayer.enc','rb').read()
    tried=set()
    for z in best[:200000]:
        count,nrms,scale,refl,pred,ind,dist=z
        tol=max(5.0,scale*.05)
        if not np.all(dist[:8] < tol) or len(set(ind[:8])) < 8:
            continue
        cs=[oc.codes[int(i)] for i in ind[:8]]
        if any(c is None for c in cs): continue
        keyhex=''.join(cs)
        if keyhex in tried: continue
        tried.add(keyhex)
        try:
            plain=unpad(AES.new(bytes.fromhex(keyhex),AES.MODE_ECB).decrypt(ciphertext),16)
            printable=sum(x in b'\n\r\t' or 32<=x<127 for x in plain)/max(1,len(plain))
            if b'bushbash{' in plain.lower() or printable>.85:
                print('AES HIT',keyhex,plain,'indices',ind[:8].tolist(),'scale',scale,'reflection',refl,'printable',printable)
        except ValueError: pass
    print('AES keys tried',len(tried),'geometric hypotheses',len(best))
except Exception as e:
    print('AES search error',repr(e))
seen = []
for z in best:
    count, nrms, scale, refl, pred, ind, dist = z
    sig = tuple(sorted(ind[dist < max(5.0, scale * .08)]))
    if any(len(set(sig) & set(old)) >= 5 for old in seen):
        continue
    seen.append(sig)
    print("match", count, "rms", -nrms, "scale", scale, "reflection", refl)
    for i, name in enumerate(("Maia", "Taygeta", "Asterope", "Celaeno", "Pleione", "Merope", "Electra", "Atlas", "Alcyone")):
        print(name, "pred", np.round(pred[i], 1), "obs", np.round(obs[ind[i]], 1), "word", np.round(words[ind[i]][:2], 1), "d", round(dist[i], 2))
    print()
    if len(seen) >= 15:
        break
