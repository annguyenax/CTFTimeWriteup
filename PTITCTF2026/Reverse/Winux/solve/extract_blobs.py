from pathlib import Path
import struct
import hashlib
import pefile

base = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted")
out = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\solve")

pe = pefile.PE(str(base / "lib" / "winuxsvc.dll"))
img = pe.OPTIONAL_HEADER.ImageBase


def read_va(va, n):
    rva = va - img
    return pe.get_data(rva, n)


# SHA IV used by hash_multi
# 0x48b3 lea/movdqu [rip+0x38e5] -> 0x81A0
iv = read_va(0x3665F81A0, 32)
print("hash IV", iv.hex())
print("sha256 iv", bytes.fromhex("67e6096a85ae67bb72f36e3c3af54fa57f520e518c68059babd9831f19cde05b").hex())

iv2 = read_va(0x3665F81C0, 32)
print("iv2/lens?", iv2.hex())

# char lengths at 0x8060
print("lens 8060", read_va(0x3665F8060, 32).hex())
print("const 8040", read_va(0x3665F8040, 32).hex())
print("xor key 7F40", read_va(0x3665F7F40, 64).hex())
print("type table 7F80", read_va(0x3665F7F80, 192).hex())

# WUX2
wux = (base / "rootfs.wux").read_bytes()
print("\nWUX2 header")
print("magic", wux[0:4], "ver", struct.unpack_from("<H", wux, 4)[0], "hsz", struct.unpack_from("<H", wux, 6)[0])
print("u32s", [hex(struct.unpack_from("<I", wux, i)[0]) for i in range(8, 0x1C, 4)])
print("hdr 1c", wux[0x1C:0x5C].hex())
count = struct.unpack_from("<I", wux, 0x10)[0]
off = struct.unpack_from("<I", wux, 0x14)[0]
print("count", count, "off", hex(off))
types = {0: "real", 1: "fake1", 2: "fake2", 3: "fake3", 4: "fake4", 5: "fake5"}
for i in range(count):
    e = wux[off + i * 0x64 : off + (i + 1) * 0x64]
    t = struct.unpack_from("<I", e, 0)[0]
    print(f"entry {i} type={t} {types.get(t,'?')} data={e[4:].hex()}")

# dump 64 expected hashes and salts
hashes = read_va(0x3665F7340, 64 * 32)
salts = read_va(0x3665F7B40, 64 * 16)
(out / "char_hashes.bin").write_bytes(hashes)
(out / "char_salts.bin").write_bytes(salts)
(out / "char_xorkey.bin").write_bytes(read_va(0x3665F7F40, 64))
print("wrote blobs")

# check standard sha256 IV byte order
std = hashlib.sha256()
print("empty sha256", std.digest().hex())
pe.close()
