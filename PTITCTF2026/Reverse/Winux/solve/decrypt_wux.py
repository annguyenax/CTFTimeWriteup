#!/usr/bin/env python3
"""Try to decrypt rootfs.wux records with recovered package key."""
import hashlib, struct, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
key = b"PTITCTF{1_7h1nk_y0u_kn0w_h0w_70_cr4ck_p1r473d_50f7w4r3_R19H7???}"
wux = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted\rootfs.wux").read_bytes()
assert wux[:4] == b"WUX2"
count = struct.unpack_from("<I", wux, 0x10)[0]
off = struct.unpack_from("<I", wux, 0x14)[0]
size = struct.unpack_from("<I", wux, 0x18)[0]
hdr64 = wux[0x1C:0x5C]
print("count", count, "off", off, "size", size, "hdr64", hdr64.hex())
data = wux[off:off+size]
names = {0: "?", 1: "real", 2: "fake1", 3: "fake2", 4: "fake3", 5: "fake4"}
# jump table: id 0..5 -> real, fake1, ...  from earlier: cmp ecx,5 then jmp table
# lea rcx paths: 1950 fake? let's just dump

recs = []
for i in range(count):
    rid = struct.unpack_from("<I", data, i * 100)[0]
    blob = data[i * 100 + 4 : i * 100 + 100]
    recs.append((rid, blob))
    print("rec", rid, "blob96", blob.hex())

k32 = hashlib.sha256(key).digest()
k64 = hashlib.sha256(key).digest() + hashlib.sha256(key[::-1]).digest()
print("sha256(key)", k32.hex())

# xor with repeating sha256
for rid, blob in recs:
    x = bytes(a ^ b for a, b in zip(blob, (k32 * 4)[:96]))
    print("xor sha256 rec", rid, x[:80])

# try AES
try:
    from Crypto.Cipher import AES
    for mode_name, mk in [("ECB", None)]:
        c = AES.new(k32, AES.MODE_ECB)
        for rid, blob in recs:
            # 96 bytes not multiple of 16? 96=6*16 yes
            pt = c.decrypt(blob)
            print("AES-ECB rec", rid, pt[:80])
            iv, ct = blob[:16], blob[16:]
            c2 = AES.new(k32, AES.MODE_CBC, iv)
            print("AES-CBC rec", rid, c2.decrypt(ct)[:80])
except Exception as e:
    print("AES err", e)

# xor with key itself
for rid, blob in recs:
    x = bytes(blob[j] ^ key[j % len(key)] for j in range(96))
    print("xor key rec", rid, x[:80])
