# The Eye — BushBash 2026

## Result

`bushbash{happy-MAT4RlKI,k1-a-k0E-e-HiW4!}`

The flag is verified by decrypting the supplied 192-byte `prayer.enc` with the supplied AES-ECB implementation and obtaining a valid UTF-8 Māori karakia followed by the flag.

## Identification

The poem describes the eight children of Matariki (the Pleiades):

| Poem clue | Māori star | Greek star | Image code |
|---|---|---|---|
| springs and ponds | Waitī | Maia | `F02E` |
| tides of sea | Waitā | Taygeta | `029F` |
| eldest / departed | Pōhutukawa | Sterope/Asterope | `2358` |
| youngest / visions | Hiwa-i-te-rangi | Celaeno | `2DC8` |
| fertile earth | Tupu-ā-nuku | Pleione | `29F0` |
| wind / breeze | Ururangi | Merope | `3468` |
| storms / drizzle | Waipuna-ā-rangi | Electra | `1057` |
| birds and trees | Tupu-ā-rangi | Atlas | `B7A8` |

The title is another Matariki clue: the name is commonly connected with the “eyes” of Tāwhirimātea. The ninth principal star, Alcyone/Matariki, is useful as a geometric anchor but is not one of the eight key parts.

## Recovering the key

`dots.png` is a dense star field with red four-hex-digit labels. A similarity-transform search places the nine-star Pleiades template over the image. Eight of the nine fitted locations have residuals around 1–4 pixels; Taygeta is affected by two merged bright halos but its correct label is visually `029F`.

The main trap is associating a nearby label with the wrong centroid. In particular, `D957` is visually close to the fitted Electra region, but the correct Waipuna-ā-rangi/Electra label is `1057`. A nearest-centroid-only pipeline therefore produces a plausible-looking but invalid AES key.

Concatenating the codes in poem order gives the 16-byte AES key:

```text
F02E029F23582DC829F034681057B7A8
```

## Verification

The provided `decrypt.py` concatenates eight inputs, converts the 32 hex characters with `bytes.fromhex`, decrypts `prayer.enc` using AES-ECB, and removes PKCS#7 padding. The recovered plaintext is:

```text
Ōna mano tāngata
Kiri whero, kiri mā,
Iwi Māori, Pākehā,
Rūpeke katoa,
Nei ka tono ko ngā hē
Māu e whakaahu kē,
Kia ora mārire
Aotearoa

bushbash{happy-MAT4RlKI,k1-a-k0E-e-HiW4!}
```

Reproduction:

```powershell
python .\solve\solve.py
```

Artifact SHA-256: `1A972E6AFB92C293C741ECCEA5FE861E8DDA31FFBB28E8A86A34A2BB9A29DA23`.
