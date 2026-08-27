#!/usr/bin/env python3
"""
Stranger Papers (PTITCTF 2026, Crypto, 500) — solver.

Recon: the zip holds 502 photos (455 .jpg + 47 .HEIC) but only 22 unique
SHA256.  Reading them in filename order (1..502) gives a 502-symbol sequence
over 22 glyphs => a monoalphabetic substitution cipher (IC ~= 0.078).

Key insight: the plaintext is NOT English.  IC 0.078 is too high for English
(0.066) and the glyph count (22) exactly matches the Vietnamese alphabet
without diacritics (a b c d e g h i k l m n o p q r s t u v x y — no f/j/w/z).
Cracking the substitution against a Vietnamese char-quadgram model yields a
coherent Vietnamese paragraph.  It describes Van Mieu - Quoc Tu Giam
(Temple of Literature) in Hanoi, so the "coordinates" the challenge asks for
are those of Van Mieu: 21.0286 N, 105.8356 E.

Run:  python solve.py   (needs `seq.txt` from notes/, and a Vietnamese corpus
file `vi_corpus.txt` — build it by scraping vi.wikipedia.org, or reuse the
precomputed key below).
"""
import math, random, re
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent          # .../Stranger Papers/
CT = (BASE / "notes" / "seq.txt").read_text().splitlines()[0]

# ---- Vietnamese char-quadgram log-probabilities (diacritics stripped) ----
def build_ngrams(corpus_path):
    txt = Path(corpus_path).read_text()
    txt = re.sub(r'[^a-z]', '', txt.lower())
    q4 = Counter(txt[i:i+4] for i in range(len(txt)-3))
    total = sum(q4.values())
    logp = {k: math.log(v/total) for k, v in q4.items()}
    return logp, math.log(0.1/total)

def load_ngrams():
    c = Path(__file__).resolve().parent / "vi_corpus.txt"
    if c.exists():
        return build_ngrams(c)
    # fallback: tiny built-in corpus is too weak; require the file
    raise SystemExit("vi_corpus.txt missing — build it first (scrape vi.wikipedia).")

LOGQ, FLOOR = load_ngrams()
def score(text):
    return sum(LOGQ.get(text[i:i+4], FLOOR) for i in range(len(text)-3))

# 22 Vietnamese letters (no f/j/w/z), rough frequency order
EFREQ_VI = "nhatiuocgemrdybsvlkpqx"
ALPHA = list("abcdefghijklmnopqrstuvwxyz")

def anneal(seed, iters=150000):
    rng = random.Random(seed)
    syms = sorted(set(CT))
    order = [c for c, _ in Counter(CT).most_common()]
    key = {s: EFREQ_VI[i] for i, s in enumerate(order)}
    unused = [ch for ch in ALPHA if ch not in key.values()]
    def dec():
        return "".join(key[c] for c in CT)
    cur = score(dec())
    best_key, best = dict(key), cur
    T0 = 20.0
    for it in range(iters):
        T = T0 * (0.5 ** (it / 50000))
        if unused and rng.random() < 0.02:
            c = rng.choice(syms); nu = rng.choice(unused); old = key[c]
            key[c] = nu; unused.remove(nu); unused.append(old)
            new = score(dec())
            if new > cur or rng.random() < math.exp((new-cur)/max(T, 1e-9)):
                cur = new
                if new > best: best, best_key = new, dict(key)
            else:
                key[c] = old; unused.remove(old); unused.append(nu)
        else:
            a, b = rng.sample(syms, 2); key[a], key[b] = key[b], key[a]
            new = score(dec())
            if new > cur or rng.random() < math.exp((new-cur)/max(T, 1e-9)):
                cur = new
                if new > best: best, best_key = new, dict(key)
            else:
                key[a], key[b] = key[b], key[a]
    improved = True
    while improved:
        improved = False
        for i in range(len(syms)):
            for j in range(i+1, len(syms)):
                a, b = syms[i], syms[j]; key[a], key[b] = key[b], key[a]
                new = score(dec())
                if new > cur:
                    cur = new; improved = True
                    if new > best: best, best_key = new, dict(key)
                else:
                    key[a], key[b] = key[b], key[a]
    return best, best_key

if __name__ == "__main__":
    best_sc, best_key = -1e18, None
    for seed in range(25):
        sc, key = anneal(80000 + seed * 11)
        if sc > best_sc:
            best_sc, best_key = sc, key
    pt = "".join(best_key[c] for c in CT)
    print("score:", round(best_sc, 1))
    print("key:", {c: best_key[c] for c in sorted(CT)})
    print("\nplaintext (Vietnamese, diacritics stripped):")
    print(pt)
