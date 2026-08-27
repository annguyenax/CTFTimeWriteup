#!/usr/bin/env python3
"""
Stranger Papers — monoalphabetic substitution cracker v2.
Correct simulated annealing (accept vs current), frequency-seeded init,
unused-letter swaps (26-letter space, 22 cipher symbols), many restarts.
"""
import math, random, sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCRATCH = Path(r"D:\download\ctf-scratch\ptitctf2026_stranger_papers")
CT = Path(BASE, "notes", "seq.txt").read_text().splitlines()[0].strip()
QUADFILE = SCRATCH / "english_quadgrams.txt"

quads = {}
total = 0
for line in QUADFILE.read_text().splitlines():
    q, c = line.split(); c = int(c)
    quads[q] = c; total += c
for q in quads:
    quads[q] = math.log10(quads[q] / total)
FLOOR = math.log10(0.01 / total)

def score(text):
    return sum(quads.get(text[i:i+4], FLOOR) for i in range(len(text)-3))

SYMS = sorted(set(CT))
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EFREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def decrypt(key):
    return "".join(key[c] for c in CT)

def frequency_key(rng):
    cf = Counter(CT)
    order = [c for c, _ in cf.most_common()]
    key = {s: EFREQ[i] for i, s in enumerate(order)}
    return key

def anneal(seed, iters=40000):
    rng = random.Random(seed)
    key = frequency_key(rng)
    cur = score(decrypt(key))
    best_key, best = dict(key), cur
    unused = [ch for ch in ALPHA if ch not in key.values()]
    T0 = 10.0
    for it in range(iters):
        T = T0 * (0.5 ** (it / 8000))
        # move type: mostly swap two symbols, occasionally swap with unused letter
        if unused and rng.random() < 0.03:
            s = rng.choice(SYMS)
            nu = rng.choice(unused)
            old = key[s]
            key[s] = nu
            unused.remove(nu); unused.append(old)
            new = score(decrypt(key))
            if new > cur or rng.random() < math.exp((new - cur) / max(T, 1e-9)):
                cur = new
                if new > best:
                    best, best_key = new, dict(key)
            else:
                key[s] = old
                unused.remove(old); unused.append(nu)
        else:
            a, b = rng.sample(SYMS, 2)
            key[a], key[b] = key[b], key[a]
            new = score(decrypt(key))
            if new > cur or rng.random() < math.exp((new - cur) / max(T, 1e-9)):
                cur = new
                if new > best:
                    best, best_key = new, dict(key)
            else:
                key[a], key[b] = key[b], key[a]
    # final greedy hill-climb
    improved = True
    while improved:
        improved = False
        for i in range(len(SYMS)):
            for j in range(i+1, len(SYMS)):
                a, b = SYMS[i], SYMS[j]
                key[a], key[b] = key[b], key[a]
                new = score(decrypt(key))
                if new > cur:
                    cur = new; improved = True
                    if new > best:
                        best, best_key = new, dict(key)
                else:
                    key[a], key[b] = key[b], key[a]
    return best_key, best

def main():
    restarts = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    seen = {}
    for i in range(restarts):
        k, s = anneal(seed=31337 + i * 101)
        pt = decrypt(k)
        print(f"[{i}] score={s:.1f}  head={pt[:50]}")
        seen.setdefault(pt, s)
    # sort distinct decryptions by score
    ranked = sorted(seen.items(), key=lambda x: -x[1])
    print("\n===== TOP 5 DISTINCT =====")
    for pt, s in ranked[:5]:
        print(f"\n--- score {s:.1f} ---")
        print(pt)
        # key
        print("key:", " ".join(f"{c}={pt[CT.index(c)]}" for c in SYMS) if False else "")

if __name__ == "__main__":
    main()
