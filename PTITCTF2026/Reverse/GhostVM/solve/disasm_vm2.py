#!/usr/bin/env python3
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "g", Path(__file__).with_name("solve_ghostvm.py")
)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

data = g.EXE.read_bytes()
va = g.pe_va_to_off(data)


def read_va(a, n):
    return data[va(a) : va(a) + n]


t1 = read_va(0x140009280, 256)
t2 = read_va(0x140009380, 256)
blob = read_va(0x1400073A0, 0x1E5C)
table = read_va(0x140007420, 0x1E5C)
out, _, _ = g.run_vm1(blob, t1, t2, table)
Path(__file__).with_name("vm2_bytecode.bin").write_bytes(out)

t1b = read_va(0x140009480, 256)
t2b = read_va(0x140009580, 256)
SEED2 = 0x0BADC0FFEE0DDF00
st = g.Stream(bytes(out), SEED2)

NAMES = {
    0: "nop",
    1: "ldi",
    2: "mov",
    3: "ldin",
    4: "xor",
    5: "xori",
    6: "add",
    7: "addi",
    8: "sub",
    9: "mul",
    10: "muli",
    11: "roli",
    12: "rori",
    13: "rolr",
    14: "shri",
    15: "shli",
    16: "andi",
    17: "or",
    18: "sboxxor",
    19: "sboxld",
    20: "seq",
    21: "sne",
    22: "jnz",
    23: "jz",
    24: "jmp",
    25: "swap",
    26: "not",
    27: "cmovnz",
    28: "ret1",
    29: "ret0",
    30: "mix",
}

lines = []
while st.pc < len(out) and not st.err:
    pc = st.pc
    op = g.decode_op(st.fetch(), t1b, t2b)
    if op > 30:
        lines.append(f"{pc:04x}: INVALID {op}")
        break
    name = NAMES[op]
    args = ""
    if op in (1, 5, 7, 10, 16):
        r = st.fetch()
        imm = st.fetch_u64()
        args = f"r{r}, 0x{imm:016x}"
    elif op in (2, 4, 6, 8, 9, 13, 17, 20, 21, 25, 27):
        a, b = st.fetch(), st.fetch()
        args = f"r{a}, r{b}"
    elif op == 3:
        a, b = st.fetch(), st.fetch()
        args = f"r{a}, in[{b}]"
    elif op in (11, 12, 14, 15):
        a, n = st.fetch(), st.fetch()
        args = f"r{a}, {n}"
    elif op == 18:
        d, s, sh1, sh2 = st.fetch(), st.fetch(), st.fetch(), st.fetch()
        args = f"r{d}, r{s}, >>{sh1} <<{sh2}"
    elif op == 19:
        d, s, sh = st.fetch(), st.fetch(), st.fetch()
        args = f"r{d}, r{s}, >>{sh}"
    elif op in (22, 23, 24):
        off = st.fetch_i32()
        args = f"{off:+d} -> {st.pc + off:04x}"
    elif op == 26:
        r = st.fetch()
        args = f"r{r}"
    elif op == 30:
        d, s = st.fetch(), st.fetch()
        imm1 = st.fetch_u64()
        rot = st.fetch()
        imm2 = st.fetch_u64()
        args = f"r{d}, r{s}, +0x{imm1:x} rol {rot} *0x{imm2:x}"
    lines.append(f"{pc:04x}: {name:8s} {args}")
    if op in (28, 29) and st.pc > 0x100:
        # continue; may be more after? halt
        pass

text = "\n".join(lines)
Path(__file__).with_name("vm2.asm").write_text(text, encoding="utf-8")
print(text)
print("----")
print("insns", len(lines), "end_pc", st.pc, "err", st.err)
