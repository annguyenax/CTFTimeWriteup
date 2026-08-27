import contextlib
import io
import sys

import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, "../the-eye")
    import ocr_codes as oc

indices = [211, 209, 203, 277, 140, 330, 115, 81, 302]
for idx in indices:
    word = oc.words[idx]
    glyphs = oc.glyphs(word[0], word[1])
    print("WORD", idx, "ocr", oc.codes[idx], "xy", (word[0], word[1]), "glyph_count", len(glyphs))
    for gi, (_, arr, width, height, area) in enumerate(glyphs):
        by_char = {}
        for train_arr, train_width, train_height, char, *_ in oc.samples:
            score = oc.gd(arr, train_arr) + 2 * abs(width - train_width) + abs(height - train_height)
            by_char[char] = min(by_char.get(char, 10**9), score)
        nearest = sorted(by_char.items(), key=lambda row: row[1])[:8]
        print("GLYPH", gi, "size", (width, height, area), "nearest", nearest)
        for row in arr:
            print("".join("##" if value else "  " for value in row))
    print()
