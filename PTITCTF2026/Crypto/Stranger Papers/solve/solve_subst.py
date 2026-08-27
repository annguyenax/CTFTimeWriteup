#!/usr/bin/env python3
"""
Stranger Papers — monoalphabetic substitution cracker.
Uses English quadgram log-probabilities + simulated annealing with restarts.
Ciphertext: notes/seq.txt line 1 (labels A..V, 22 symbols).
"""
import math
import random
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # .../Stranger Papers/
SCRATCH = Path(r"D:\download\ctf-scratch\ptitctf2026_stranger_papers")

CT = Path(BASE, "notes", "seq.txt").read_text().splitlines()[0].strip()
QUADFILE = SCRATCH / "english_quadgrams.txt"

# ---- load quadgram log-probs ----
quads = {}
total = 0
for line in QUADFILE.read_text().splitlines():
    q, c = line.split()
    c = int(c)
    quads[q] = c
    total += c
for q in quads:
    quads[q] = math.log10(quads[q] / total)
FLOOR = math.log10(0.01 / total)  # unseen quadgram penalty

def score(text):
    s = 0.0
    for i in range(len(text) - 3):
        s += quads.get(text[i:i+4], FLOOR)
    return s

SYMS = sorted(set(CT))
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# order letters by English frequency for a good initial guess
FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def decrypt(key):
    return "".join(key[c] for c in CT)

def initial_key():
    # map 22 symbols to the top-22 English letters (by frequency)
    used = list(FREQ_ORDER[:len(SYMS)])
    random.shuffle(used)
    return dict(zip(SYMS, used))

def sa(seed):
    rng = random.Random(seed)
    key = initial_key()
    best_key = dict(key)
    best_score = score(decrypt(key))
    T = 20.0
    step = 0
    max_steps = 30000
    # letters not currently used
    used = set(key.values())
    unused = [ch for ch in ALPHA if ch not in used]

    for step in range(1, max_steps + 1):
        T = 20.0 * (0.5 ** (step / 10000))
        a, b = rng.sample(SYMS, 2)
        key[a], key[b] = key[b], key[a]
        sc = score(decrypt(key))
        if sc > best_score:
            best_score = sc
            best_key = dict(key)
        if sc > best_score or rng.random() < math.exp((sc - best_score) / max(T, 1e-9)):
            pass  # accept (already swapped)
        else:
            key[a], key[b] = key[b], key[a]  # revert

        # occasionally swap a used letter with an unused one
        if unused and rng.random() < 0.02:
            c = rng.choice(SYMS)
            nu = rng.choice(unused)
            old = key[c]
            key[c] = nu
            used.discard(old); unused.remove(nu); unused.append(old)
            sc = score(decrypt(key))
            if sc > best_score:
                best_score = sc
                best_key = dict(key)
            elif rng.random() >= math.exp((sc - best_score) / max(T, 1e-9)):
                key[c] = old
                unused.remove(old); unused.append(nu)

    return best_key, best_score

def main():
    best_k, best_s = None, -1e18
    restarts = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for i in range(restarts):
        k, s = sa(seed=1000 + i * 7)
        print(f"[restart {i}] best score = {s:.1f}")
        if s > best_s:
            best_s, best_k = s, k
    print("\n===== GLOBAL BEST =====")
    print(f"score = {best_s:.1f}")
    pt = decrypt(best_k)
    print(pt)
    print("\nkey (cipher symbol -> plaintext):")
    print(" ".join(f"{c}->{best_k[c]}" for c in SYMS))
    # freq check
    print("\nplaintext letter freqs:")
    print(Counter(pt).most_common())

if __name__ == "__main__":
    main()
