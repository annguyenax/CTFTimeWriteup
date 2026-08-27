# Bliss I — BushBash 2026

> **Correction:** This rune/CSS extraction is the chained Bliss II stage. The
> resulting media-query flag was rejected when submitted to Bliss I. Treat the
> material below as Bliss II analysis, not a verified Bliss I solution.

## Goal

Recover the flag from `bliss.png`, described as “one very strange cloud”.

## Environment and evidence

- Original artifact: `../bliss.png`
- Rune clue image: `../runes.png`
- Archived route component: `../solve/evidence/route_node_22.js`
- Archived stylesheet: `../solve/evidence/app.css`
- Deterministic solver: `../solve/solve.py`

SHA-256 values:

```text
8D1EB94E1980B94481732D36BC87F1E02ACF1738470B5FC0A67CC47AEE7B24FE  bliss.png
5CFF6CD46ACEFFD0EF5F5D4B40CFC94BD1BB82A8539B9A1B38977273159B9F8F  runes.png
E9FB92BD0BF8661800356740AC89E85DEB3E5FEB813CB3F812D20CC4C9A03C00  route_node_22.js
9418CBA42416B6798F56AFE2A54641EE2F48B7CF210C4ADCFE088974BA7CA641  app.css
```

## Enumeration

Treating the cloud as a QR/Data Matrix was a false lead. The decisive clue was
the public Svelte route named `atmospherically-questionable-runes`. Its compiled
node contains 64 one-character cells, `square-1` through `square-64`. The global
stylesheet contains five unusual media queries which highlight selected cells.
The pictograms in `runes.png` give the order in which those conditions are read.

## Extraction

Mapping each selector ID to the character in the route node gives:

| Media condition | Selected IDs | Text |
|---|---|---|
| `screen and (aspect-ratio: 6/7)` | 6, 20, 23, 36, 44, 52, 55, 60 | `bushbash` |
| `screen and (pointer: coarse)` | 22, 28, 49, 52, 58, 61 | `alWaY$` |
| `print and (orientation: landscape)` | 2, 9, 17, 23, 31, 34, 47, 50 | `quEsTi0N` |
| `(monochrome)` | 12, 33, 59, 63 | `yoUR` |
| `screen and (-webkit-device-pixel-ratio: 3)` | 7, 21, 24, 38, 52, 64 | `m3d1a!` |

The braces drawn in the clue separate the event prefix from the four payload
segments. Crucially, the clue also draws a literal hyphen between each pair of
payload pictograms. Joining with those delimiters yields:

```text
bushbash{alWaY$-quEsTi0N-yoUR-m3d1a!}
```

## Verification

Running `python solve/solve.py` parses both archived assets, asserts that all 64
cells exist, prints every selector-to-text mapping, and emits the same flag. The
captured stdout is stored as `solve/evidence/solver_stdout.txt` and mirrored in
the stack output under `raw/`.

## Failed paths and lessons

- QR/Data Matrix reconstruction, border repair, rotation and traversal brute
  force failed because the cloud was a clue to another presentation layer, not
  a machine-readable matrix.
- Metadata, bit-plane inspection and background subtraction did not expose the
  payload.
- When an image challenge visually points to browser/device concepts, inspect
  client routes and CSS before committing to expensive steganography pipelines.
- Unusual media queries are executable selectors: extract their element IDs and
  join the corresponding DOM text in clue order.

Two viable solve paths are manual browser emulation of each media condition, or
static parsing of the compiled DOM and CSS. Static parsing is faster and fully
reproducible.
