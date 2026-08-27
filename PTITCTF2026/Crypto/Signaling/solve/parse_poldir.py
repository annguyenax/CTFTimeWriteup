# Parse the per-frame polar-direction extraction and reconstruct hold sequence
import re

PATH = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\frames\poldir.txt"
with open(PATH, "r", encoding="utf-16") as f:
    text = f.read()

# lines look like: "0 p1=307 p2=232"
rows = []
for line in text.splitlines():
    m = re.match(r"\s*(\d+)\s+p1=(-?\d+)\s+p2=(-?\d+)", line.strip())
    if m:
        rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

print("rows:", len(rows), "first:", rows[0], "last:", rows[-1])

# Direction mapping used by the user: 0=SE(51), 1=SW(127), 2=NW(232), 3=NE(307)
ang2dir = {51: 0, 127: 1, 232: 2, 307: 3}

# Run-length encode the (p1,p2) pair
runs = []
cur = None
for f, p1, p2 in rows:
    key = (p1, p2)
    if key != cur:
        runs.append([f, p1, p2, 1])
        cur = key
    else:
        runs[-1][3] += 1

print("\n=== runs of (p1,p2): frame, p1, p2, dur ===")
for r in runs:
    print(r)

# Now extract 'beam direction per hold' as the user did.
# p1/p2 are the two opposite lobes. The beam axis = the pair {p1,p2}.
# Show also which of the 4 directions appear.
allang = sorted({p for _, p, q in rows for p in (p, q)})
print("\nall distinct angles:", allang)
