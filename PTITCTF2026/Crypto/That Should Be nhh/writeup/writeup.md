# That Should Be nhh

- **Event:** PTITCTF2026
- **Category:** Crypto / RSA / Howgrave-Graham
- **Status:** solved
- **Attachment:** `enc.sage`

## Construction

1024-bit `N=pq` with `p=A+s`, `A` a 512-bit integer that is `2^k` times ~16 primes from `[2^31,2^32)`, `|s|<2^80`.  
`K=A(q-r)` (`|r|<2^80`), `e=(K v + u//2)//u` with primes `u≈96-bit`, `v≈88-bit`.  
AES-CBC, key `sha256(str(p))`, `m=int((iv||ct).hex())`, `c=m^e mod N`.

## Attack

1. Continued fraction `e/N ≈ v/u` recovers the primes `u,v`.
2. Invert the rounding: `K=(e u - u//2 + ρ0 + t v)/v` for `t < u/v ≈ 200`.
3. The correct `t` (`40` here) has `K` with many 31–32-bit factors. Brent ρ (c=1,2,…) peels them off. `A` is the product of the sixteen 32-bit primes times `2^9` (bit length 512).
4. Howgrave-Graham / Coppersmith on `f(x)=x+A` modulo `N`, `X=2^80`, `β=0.5`. Sympy `Matrix.lll` on the 7×7 lattice. `s` is 78-bit; `p=A+s` divides `N`.
5. `d=e^{-1} mod φ(N)`, AES-CBC decrypt.

## Flag

```
PTITCTF{7h47_5h0uld_b3_nhh,_h0ld1n9_y0ur_h4nd}
```

## Verification

`p | N` (otherwise AES path is not reached) and plaintext is `PTITCTF{...}`. Solver: `solve/hg_sympy.py` / the 16-prime reconstruction in `solve/`.

## Pitfalls

- `A`’s primes are **31–32 bit**, so trial division to `2^16`/`2^20` barely touches them; need ρ/ECM.
- Extra 22/25-bit factors can stick to `A` and must be moved back to `q-r`.
- Home-rolled LLL on Python `Fraction` does not finish; use `sympy.Matrix.lll`.
