from pathlib import Path
import pefile

out = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\solve")
base = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted")


def get_section(pe, name):
    n = name.encode()
    for s in pe.sections:
        raw = s.Name.split(b"\x00")[0]
        if raw == n or raw.startswith(n):
            return s
    return None


def dump_rdata(pe_path, out_name):
    pe = pefile.PE(str(pe_path))
    img = pe.OPTIONAL_HEADER.ImageBase
    rdata = get_section(pe, ".rdata")
    data = rdata.get_data()
    va = img + rdata.VirtualAddress
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i : i + 16]
        hx = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{va + i:016x}  {hx:<48}  {asc}")
    (out / out_name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    strs = []
    cur = bytearray()
    start = 0
    for i, b in enumerate(data):
        if 32 <= b < 127:
            if not cur:
                start = i
            cur.append(b)
        else:
            if len(cur) >= 4:
                strs.append((va + start, cur.decode()))
            cur = bytearray()
    print(pe_path.name, "rdata strings:")
    for a, s in strs:
        print(f"  {a:016x} {s}")
    pe.close()


dump_rdata(base / "lib" / "winuxsvc.dll", "winuxsvc_rdata.txt")
print("--- pam ---")
dump_rdata(base / "lib" / "libpam_w32.dll", "libpam_rdata.txt")
print("--- exe ---")
dump_rdata(base / "winux.exe", "winux_rdata.txt")

pe = pefile.PE(str(base / "winux.exe"))
img = pe.OPTIONAL_HEADER.ImageBase
dsec = get_section(pe, ".data")
data = dsec.get_data()
print("exe .data VA", hex(img + dsec.VirtualAddress), "len", len(data))
print(data.hex())
pe.close()

pe = pefile.PE(str(base / "lib" / "winuxsvc.dll"))
img = pe.OPTIONAL_HEADER.ImageBase
dsec = get_section(pe, ".data")
data = dsec.get_data()
print("svc .data VA", hex(img + dsec.VirtualAddress), "len", len(data))
print(data.hex())
pe.close()
