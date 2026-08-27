from pathlib import Path
import struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM

out = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\solve")
base = Path(r"D:\download\CTFTimeWriteup\PTITCTF2026\Reverse\Winux\files\_extracted")


def get_section(pe, name):
    n = name.encode()
    for s in pe.sections:
        raw = s.Name.split(b"\x00")[0]
        if raw == n or raw.startswith(n):
            return s
    return None


def rva_to_off(pe, rva):
    return pe.get_offset_from_rva(rva)


def collect_strings(pe):
    img = pe.OPTIONAL_HEADER.ImageBase
    strs = {}
    for secname in (b".rdata", b".data"):
        for s in pe.sections:
            if s.Name.startswith(secname):
                data = s.get_data()
                va = img + s.VirtualAddress
                cur = bytearray()
                start = 0
                for i, b in enumerate(data):
                    if 32 <= b < 127:
                        if not cur:
                            start = i
                        cur.append(b)
                    else:
                        if len(cur) >= 4:
                            strs[va + start] = cur.decode()
                        cur = bytearray()
    return strs


def pdata_funcs(pe):
    img = pe.OPTIONAL_HEADER.ImageBase
    pdata = get_section(pe, ".pdata")
    data = pdata.get_data()
    funcs = []
    for i in range(0, len(data) - 11, 12):
        begin, end, unwind = struct.unpack_from("<III", data, i)
        if begin == 0:
            continue
        funcs.append((img + begin, img + end, unwind))
    return funcs


def disasm_pe(pe_path, out_name, extra_starts=None):
    pe = pefile.PE(str(pe_path))
    img = pe.OPTIONAL_HEADER.ImageBase
    text = get_section(pe, ".text")
    code = text.get_data()
    text_va = img + text.VirtualAddress
    strs = collect_strings(pe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    funcs = pdata_funcs(pe)
    print(pe_path.name, "functions from pdata:", len(funcs))
    for a, b, u in funcs:
        print(f"  {a:016x}-{b:016x} size={b-a}")

    lines = []
    # map rva of imports
    imports = {}
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.address:
                    name = imp.name.decode() if imp.name else f"ord{imp.ordinal}"
                    imports[imp.address] = f"{entry.dll.decode()}:{name}"

    def comment_for(insn):
        notes = []
        for op in insn.operands:
            if op.type == CS_OP_IMM:
                v = op.imm & 0xFFFFFFFFFFFFFFFF
                if v in strs:
                    notes.append(repr(strs[v]))
                elif v in imports:
                    notes.append(imports[v])
            elif op.type == CS_OP_MEM:
                disp = op.mem.disp
                if insn.reg_name(op.mem.base) in ("rip",):
                    tgt = insn.address + insn.size + disp
                    if tgt in strs:
                        notes.append(repr(strs[tgt]))
                    elif tgt in imports:
                        notes.append(imports[tgt])
        return " ; " + ", ".join(notes) if notes else ""

    for start, end, _ in funcs:
        off = start - text_va
        size = end - start
        if off < 0 or off >= len(code):
            continue
        blob = code[off : off + size]
        lines.append(f"\n; ===== FUNC {start:016x} size={size} =====")
        for insn in md.disasm(blob, start):
            lines.append(f"{insn.address:016x}: {insn.mnemonic:8s} {insn.op_str}{comment_for(insn)}")
    (out / out_name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    pe.close()
    print("wrote", out_name, "lines", len(lines))


disasm_pe(base / "lib" / "winuxsvc.dll", "winuxsvc_disasm.txt")
disasm_pe(base / "lib" / "libpam_w32.dll", "libpam_disasm.txt")
disasm_pe(base / "winux.exe", "winux_disasm.txt")
