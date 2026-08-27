# D-Side — UIUCTF 2026

## Challenge Info
- **Category:** Crypto
- **Points:** 453
- **Files:** `chal.sage`, `util.sage`, `out` (but there are TWO out files — `out` and `out (1)`)

## Output Data (`out (1)` is the correct, smaller one)
```
steps = 32
isogeny_degree = 64
j = <Puiseux series in GF(16)[u]>
iv = 08b3e31e10d3e4f35aa3265a2516f142
ct = 8f964b3d26b49ebfc0abe1762d66922e5b206eb1a3bd9b229aba585bac9185f2
```

## Mathematical Setup
- `q = 4`, `k = GF(16)`, Puiseux series ring with 800 terms precision
- **State:** `(g, a)` where `g` is a Puiseux series, `a` is a "leading edge direction"
- **j-invariant:** `j(g) = g^(q+1) = g^5`
- **Initial edge:** `a₀ = u^(1/5)`, `g₀ = (0 + a₀*(T^q - T)) * a₀^(q-1)`
- **Forward walk:**
  - Each step: compute `forward_edges(g, a, exclude_escape=True)` → `q-1 = 3` edges
  - Sort by j-invariant string representation → choose index `secrets.randbelow(q-1)` ∈ {0,1,2}
  - Alternate: even steps use `secrets.choice(all_forward_edges)` (including escape)
  
## Walk Pattern (32 steps total)
```python
for i in range(32):
    # ODD steps (i=0,1,...): choose from 3 non-escape edges
    edges = sorted(forward_edges(g, a, exclude_escape=True), key=str(j_invariant))
    g, a = edges[secrets.randbelow(q - 1)]  # index in {0,1,2}
    path.append(serialize_j(j(g)))
    
    if i + 1 < 32:
        # EVEN steps: choose from all forward edges (including escape)
        g, a = secrets.choice(forward_edges(g, a))  # uniformly random
        path.append(serialize_j(j(g)))
```
So path has: initial j, then 32 pairs of (non-escape choice, all-choice) = 64 j-values + initial = 65 values? Actually:
- Start: 1 j-value (initial)
- Per step i: 1 j-value after choice
- Plus: if i+1 < 32: 1 more j-value
= 1 + 32 + 31 = 64 j-values in path

The key = SHA256 of concatenated serialized j-invariants.

## Key: Only Final j-invariant is Known
We know the FINAL j (after step 31 ends, after the non-escape choice).
We need to reconstruct the ENTIRE PATH.

## Attack Analysis

### Bruhat-Tits Tree Structure
- This is a walk on the **Bruhat-Tits tree** of PGL₂(k((T))) where k=GF(4)
- The tree is q+1 = 5 regular (5 edges at each vertex)
- "Forward" edges: all except the backward edge (4 edges)
- "Non-escape" forward edges: 3 edges (exclude the one going to lower depth)
- The "secret" is the sequence of choices at each step

### Path Recovery
At each non-escape step: 3 choices → 1 bit+ of entropy
At each escape-allowed step: 4 choices → 2 bits of entropy
Total entropy: ~32*2 bits = 64 bits? No...

Actually: 32 steps × log₂(3) + 31 steps × log₂(4) ≈ 32*1.58 + 31*2 = 50.7 + 62 ≈ 113 bits

This is too much for brute force.

### Constraint: Final j-invariant Known
We know where we end up. The BFS/DFS backward from the final node might work if the tree is small enough. But with 113 bits of path space, it's infeasible.

### Hidden Structure?
The `out` file (37420 bytes) contains 6 lines which look like:
- Line 1-3: Large matrices (unrelated to D-Side?)
- Line 4: ct bytes
- Line 5: iv bytes
- Actually `out` might be for a DIFFERENT challenge (Young Cryptography?)

Wait: the `out` file in D-Side folder has matrices like Young Cryptography format.
And `out (1)` has the proper D-Side format.

**CONFUSION:** `out (1)` IS the D-Side output. The `out` file may be misplaced Young Crypto output!

### Re-analysis of True D-Side Output
```
steps = 32
isogeny_degree = 64
j = (c^2 + c + 1)*u^6 + ... + O(u^76)
iv = 08b3e31e10d3e4f35aa3265a2516f142
ct = 8f964b3d26b49ebfc0abe1762d66922e5b206eb1a3bd9b229aba585bac9185f2
```

The j-invariant starts at `u^6` (valuation 6 = q+1+1? = 6 for q=4? or 6 = starting depth).

## Status
- 🔬 **Deep math required** — Bruhat-Tits tree, isogeny walks, Newton-Puiseux
- ❌ **Not yet solved** — need to understand the specific vulnerability
- **Hypothesis:** The sorting by j-invariant string + small step count may allow enumeration

## Notes
- This is category 453 points (very hard)
- May require SageMath to run
- The "out" file (37420 bytes, matrix format) may actually be for Young Cryptography misplaced here
