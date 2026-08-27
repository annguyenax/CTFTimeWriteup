# Young Cryptography — UIUCTF 2026

## Challenge Info
- **Category:** Crypto
- **Points:** 117
- **File:** `chal.py`
- **Output file:** ❌ Not available (need server connection)

## Description
DH-style key exchange using a custom RSK (Robinson-Schensted-Knuth) product `my_prod` over the plactic monoid of symmetric integer matrices.

### Protocol
```
N=64, n=256
G = random_matrix()   # 64x64 symmetric matrix, entries 0/1/2
A = random_matrix()
B = random_matrix()
AG = my_prod(A, G)    # public
GB = my_prod(G, B)    # public
AGB = my_prod(A, GB)  # shared secret
key = SHA256(str(AGB))[:128]  # = all 32 bytes (AES-256-CBC key)
```

## Analysis

### `my_prod` is the RSK Plactic Monoid Product
- `my_prod(A, B)` computes the **Viennot shadow construction** (RSK product of biwords)
- It is **associative**: `my_prod(A, my_prod(G, B)) = my_prod(my_prod(A, G), B)`  
- Identity element: **zero matrix** (not I) — `my_prod(Z, A) = A`
- Sum property: `sum(my_prod(A, B)) = sum(A) + sum(B)`
- **Collisions exist**: A1 ≠ A2 but `my_prod(A1, G) = my_prod(A2, G)` is possible

### Critical Lemma (Verified)
> If `A1 * G = A2 * G`, then `A1 * (G*B) = A2 * (G*B)` for **all** B.

This means: finding **any** A' such that `my_prod(A', G) = AG` is sufficient — the resulting `AGB = my_prod(A', GB)` will be the correct shared secret.

## Attack: Inverse RSK (Plactic Division)

### Algorithm
1. Recover the RSK forward state `r_AG` after processing `[A rows] + [G rows]`
2. **Peel off G rows in reverse** using inverse row update
3. Obtain `r_A'` (state before G rows, possibly different from true `r_A`)
4. Process `GB rows` from `r_A'` to compute `r_AGB`
5. Run backward decode on `r_AGB` to get `AGB`
6. Decrypt: `SHA256(str(AGB))` → AES-256-CBC key

### Inverse Row Update (single row)
Given: `s_new` (state after row), `x_row` (row values)  
Recover: `r_old` (state before row)

```
r[0] = z (invariant)
For j = 1..n:
  M0 = s_new[j][0] - x_row[j-1]
  if s[j-1][0] < M0: r[j][0] = M0  # unique
  if s[j-1][0] = M0: r[j][0] = M0  # canonical (might not be exact A, but gives same AGB)
```

### Status
- ❌ **No output file** — cannot run attack without server data
- 🔑 **Theory complete** — attack is algebraically sound
- To get output: `nc young-cryptography.chal.uiuc.tf [PORT]` or download from challenge server

## Code
- Attack script: `D:\download\ctf-scratch\uiuctf2026_young_crypto\inverse_rsk.py`
- Analysis: `D:\download\ctf-scratch\uiuctf2026_young_crypto\analysis.py`
