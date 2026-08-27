# That Should Be nhh — session

## Restate
`enc.sage`: 1024-bit RSA, AES-CBC key `sha256(str(p))`, `m=int((iv+ct).hex())`, `c=m^e mod N`.
`p = A + s` with A 512-bit **32-bit-smooth**, `s` 80-bit odd.
`K = A*(q-r)`, `r` 80-bit, `e ≈ K*v/u` with `u`~96-bit prime, `v`~88-bit prime.

Title ≈ Howgrave-Graham / Coppersmith known-MSBs of `p`.

## Recovered
- `e/N ≈ v/u` continued fraction: **exact primes** `u` 96-bit, `v` 88-bit.
- Toy generator confirms CF recovers `u,v` and `K` is `t`-indexed: `K=(e*u - u//2 + rho0 + t*v)/v`, `t < u/v ≈ 200`.

## Stuck
Stripping 32-bit factors from the ~200 `K` candidates never yields a 512-bit smooth `A` (best ~108 bits of small factors with weak rho). Need **p-1 / ECM** aimed at 32-bit factors (`solve/pm1.py`).

Once `A` is known: Howgrave-Graham on `f(x)=x+A` mod `N`, `X=2^80`, `beta=0.5` (since `2^80 << N^{1/4}=2^{256}`). Then AES decrypt.

## Public numbers
Parsed from comments at the bottom of `files/enc.sage` (`n`,`e`,`c`).
