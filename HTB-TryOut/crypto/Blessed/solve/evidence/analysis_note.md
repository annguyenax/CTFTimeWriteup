# Blessed — deferred analysis notes

- Category: crypto, difficulty HARD, author makelaris. Requires remote TCP oracle
  (target.txt: 154.57.164.66:31963). No offline flag in files — flag is only in
  flag.txt on server, read via solve of the scheme.
- Scheme: BLS12-381 signatures (py_ecc) + a P-256 ECC custom RNG.
  `rng()`: seed=randbelow(curve_order); builds P-256 point G and random B;
  W0=G*seed+B; each step Wn+=G, leaks Wn.x>>32 and Wn.y>>32 (top 32 bits of
  x and y of successive points).
- Robot: each verified robot has random BLS sk, pk=SkToPk. SuperComputer creates
  n robots and (presumably) signs a challenge with each; leak of per-signature
  nonce = top bits of P-256 point coordinates => Hidden Number Problem (HNP).
- Progress: reduced multivariate polynomial over Z; m=2 confirmed (leading rows
  vanish at root mod curve_order). Was extracting (u0,v0) via resultant +
  integer roots when time budget hit.
- Defeferred: needs lattice/HNP solve + live remote oracle connection; off-batch.
